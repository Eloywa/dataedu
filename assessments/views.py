import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from courses.models import Lesson
from gamification import services

from . import projects, tasks
from .grading import diagnose
from .manual import read_answer
from .models import AnswerSubmission, Assignment, Submission, TestAttempt

# Какое поле сдачи хранит ответ: запрос показывается как SQL, остальное — как текст.
SQL_TASK_TYPES = ("sql", "ddl")


def _json_object(request):
    """Тело запроса как словарь или None, если там что-то другое.

    Проверка типа обязательна: корректный JSON — это ещё не объект, и на теле `[]`
    вызов `.get` дальше по коду превращался бы в ошибку сервера.
    """
    try:
        payload = json.loads(request.body)
    except (ValueError, TypeError):
        return None
    return payload if isinstance(payload, dict) else None


@login_required
def lesson_test(request, lesson_id):
    lesson = get_object_or_404(
        Lesson.objects.visible_to(request.user).select_related("module__course"), id=lesson_id
    )
    # Закрытая неделя и незаписанный студент уходят на страницу урока: там объяснено,
    # что делать дальше. Попытка теста завершает урок, поэтому правило то же, что у отметки.
    if not services.may_study(request.user, lesson):
        return redirect("courses:lesson_detail", lesson_id=lesson_id)

    test = lesson.tests.first()
    if test is None:
        return redirect("courses:lesson_detail", lesson_id=lesson_id)

    questions = list(test.questions.prefetch_related("options").all())

    if request.method == "POST":
        total_points = 0
        earned = 0
        results = []
        for q in questions:
            total_points += q.points
            options = list(q.options.all())
            option_ids = {str(o.id) for o in options}
            correct = next((o for o in options if o.is_correct), None)

            chosen_id = request.POST.get(f"q_{q.id}")
            if chosen_id not in option_ids:  # защита от подделки/пустого
                chosen_id = None
            is_correct = bool(correct and chosen_id and str(correct.id) == chosen_id)
            if is_correct:
                earned += q.points

            results.append(
                {
                    "question": q,
                    "options": options,
                    "chosen_id": chosen_id,
                    "correct_id": str(correct.id) if correct else None,
                    "is_correct": is_correct,
                }
            )

        score = round(earned * 100 / total_points) if total_points else 0
        is_passed = score >= test.pass_score

        attempt = TestAttempt.objects.create(
            user=request.user,
            test=test,
            score=score,
            is_passed=is_passed,
            started_at=timezone.now(),
            finished_at=timezone.now(),
        )
        AnswerSubmission.objects.bulk_create(
            [
                AnswerSubmission(
                    attempt=attempt,
                    question=r["question"],
                    answer_option_id=r["chosen_id"],
                    is_correct=r["is_correct"],
                )
                for r in results
            ]
        )

        # Событие, XP за первое прохождение, «Знаток тестов», отметка урока.
        services.finish_test(request.user, attempt, lesson)

        return render(
            request,
            "assessments/test_result.html",
            {
                "lesson": lesson,
                "test": test,
                "score": score,
                "is_passed": is_passed,
                "results": results,
            },
        )

    return render(
        request,
        "assessments/test.html",
        {"lesson": lesson, "test": test, "questions": questions},
    )


@login_required
def practice(request):
    """Список заданий: с автопроверкой отдельно от тех, что смотрит преподаватель.

    Условие автопроверки — не только `type="sql"`, но и наличие посчитанного эталона.
    Раньше в список попадало любое SQL-задание, и если у него не был посчитан эталон,
    студент получал editor, кнопка в котором отвечала ошибкой. Теперь такие задания
    сразу показываются как «проверяет преподаватель» — платформа не предлагает того,
    чего не умеет.
    """
    return render(
        request,
        "assessments/practice_list.html",
        {"groups": tasks.grouped_tasks(request.user)},
    )


def _visible_assignment(request, assignment_id):
    return get_object_or_404(
        Assignment.objects.visible_to(request.user).select_related(
            "course", "lesson__module__course", "opens_after"
        ),
        id=assignment_id,
    )


def _is_locked(user, assignment):
    """Задание закрытой недели закрыто вместе с уроком.

    Иначе экран «урок закрыт» обходился бы прямой ссылкой на его задание, а балл за него
    идёт в ведомость.
    """
    return assignment.lesson_id is not None and not services.lesson_unlocked(
        user, assignment.lesson
    )


def _last_submission(user, assignment):
    return (
        Submission.objects.filter(user=user, assignment=assignment)
        .order_by("-submitted_at")
        .first()
    )


def _may_submit_work(user, assignment, last):
    """Можно ли сдать работу преподавателю прямо сейчас.

    Нужна запись на курс: преподаватель оценивает своих студентов, и работа
    незаписанного попала бы в очередь, но не в ведомость. Оценённая работа закрыта:
    чтобы её пересдать, преподаватель возвращает её на доработку.
    """
    if assignment.is_autocheckable or user.is_teacher:
        return False
    if not services.may_track_progress(user, assignment.course):
        return False
    ticket = projects.ticket_state(user, assignment)
    if ticket and ticket["needs_draw"]:
        return False
    return last is None or last.status != "graded"


def _next_lesson(lesson):
    """Следующий урок курса по порядку или None, если этот последний."""
    ordered = list(
        Lesson.objects.filter(module__course=lesson.module.course_id).order_by(
            "module__order_index", "order_index"
        )
    )
    index = next((i for i, item in enumerate(ordered) if item.id == lesson.id), None)
    return ordered[index + 1] if index is not None and index + 1 < len(ordered) else None


def _render_assignment(request, assignment, answer_text="", answer_error=None):
    last = _last_submission(request.user, assignment)
    solved = Submission.objects.filter(
        user=request.user, assignment=assignment, score__gte=1
    ).exists()
    return render(
        request,
        "assessments/assignment_detail.html",
        {
            "assignment": assignment,
            "solved": solved,
            "next_lesson": _next_lesson(assignment.lesson) if assignment.lesson_id else None,
            "ticket": projects.ticket_state(request.user, assignment),
            "just_drawn": request.GET.get("drawn") == "1",
            "last_submission": last,
            "can_submit": _may_submit_work(request.user, assignment, last),
            "is_participant": services.may_track_progress(request.user, assignment.course),
            "is_sql_task": assignment.type in SQL_TASK_TYPES,
            "answer_text": answer_text,
            "answer_error": answer_error,
            "just_submitted": request.GET.get("submitted") == "1",
        },
    )


@login_required
def assignment_detail(request, assignment_id):
    assignment = _visible_assignment(request, assignment_id)
    if _is_locked(request.user, assignment):
        return render(
            request,
            "lessons/lesson_locked.html",
            {
                "course": assignment.course,
                "lesson": assignment.lesson,
                "prev_module": services.previous_module(assignment.lesson.module),
                "is_task": True,
            },
        )
    return _render_assignment(request, assignment)


@login_required
@require_POST
def draw_ticket(request, assignment_id):
    """Вытянуть билет итогового проекта. Тема выбирается здесь, на сервере."""
    assignment = _visible_assignment(request, assignment_id)
    target = reverse("assessments:assignment_detail", args=[assignment.pk])
    ticket = projects.ticket_state(request.user, assignment)
    if not ticket or not ticket["can_draw"]:
        return redirect(target)
    projects.draw_ticket(request.user, assignment)
    return redirect(f"{target}?drawn=1")


@login_required
@require_POST
def submit_work(request, assignment_id):
    """Сдать работу, которую проверяет преподаватель: DDL, файл или текст.

    Запись на пару «студент + задание» одна: пока работа не оценена, новая редакция
    заменяет прежнюю, а не копится рядом. Иначе очередь преподавателя показывала бы
    несколько версий одной работы, и все, кроме последней, пришлось бы разбирать зря.
    """
    assignment = _visible_assignment(request, assignment_id)
    target = reverse("assessments:assignment_detail", args=[assignment.pk])
    if _is_locked(request.user, assignment):
        return redirect(target)

    last = _last_submission(request.user, assignment)
    if not _may_submit_work(request.user, assignment, last):
        return redirect(target)

    raw_text = request.POST.get("answer", "")
    answer, error = read_answer(raw_text, request.FILES.get("upload"))
    if error:
        return _render_assignment(request, assignment, answer_text=raw_text, answer_error=error)

    submission = last or Submission(assignment=assignment, user=request.user)
    if assignment.type in SQL_TASK_TYPES:
        submission.sql_query = answer
    else:
        submission.text_answer = answer
    # Балл от прошлой редакции к новой не относится. Отзыв остаётся: преподаватель
    # увидит рядом с новой версией, что он просил поправить.
    submission.status = "submitted"
    submission.score = None
    submission.graded_by = None
    submission.graded_at = None
    submission.submitted_at = timezone.now()
    submission.save()

    services.record_submission(request.user, submission)
    return redirect(f"{target}?submitted=1")


@login_required
@require_POST
def check_assignment(request, assignment_id):
    assignment = _visible_assignment(request, assignment_id)
    if _is_locked(request.user, assignment):
        return JsonResponse(
            {"passed": False, "message": "Задание откроется вместе с уроком."}, status=403
        )
    if not assignment.is_autocheckable:
        return JsonResponse(
            {
                "passed": False,
                "message": "Это задание проверяет преподаватель — автопроверки у него нет.",
            },
            status=400,
        )

    payload = _json_object(request)
    sql = (payload or {}).get("sql") or ""
    columns = (payload or {}).get("columns") or []
    rows = (payload or {}).get("rows") or []
    if (
        payload is None
        or not isinstance(sql, str)
        or not isinstance(columns, list)
        or not isinstance(rows, list)
        or not all(isinstance(row, list) for row in rows)
    ):
        return JsonResponse({"passed": False, "message": "Некорректные данные."}, status=400)
    # Нулевой байт PostgreSQL в тексте не хранит, а в JSON он прийти может.
    sql = sql.replace("\x00", "").strip()

    expected = assignment.expected_result
    # Диагностика раскладывает итог на столбцы / число строк / состав строк.
    # `passed` берётся оттуда же, поэтому вердикт и подсказки не могут разойтись.
    report = diagnose(columns, rows, expected.get("columns", []), expected.get("rows", []))
    passed = report["passed"]

    # Сервер ставит итог независимо от браузера (целостность оценки).
    submission = Submission.objects.create(
        assignment=assignment,
        user=request.user,
        sql_query=sql,
        score=assignment.max_score if passed else 0,
        status="graded",
        feedback=_feedback_text(report),
        submitted_at=timezone.now(),
        graded_at=timezone.now(),
    )
    services.record_submission(request.user, submission)

    return JsonResponse({"passed": passed, "checks": report["checks"], "hint": report["hint"]})


@login_required
@require_POST
def report_error(request, assignment_id):
    """Класс ошибки SQL при решении задания.

    Отдельная точка, а не поле в `check`: ошибка происходит раньше проверки —
    запрос не выполнился, и сравнивать с эталоном нечего. Приходит только код
    класса (см. `learning/sqlerrors.py`), запрос и текст ошибки остаются в
    браузере.
    """
    assignment = _visible_assignment(request, assignment_id)
    payload = _json_object(request)
    if payload is None:
        return JsonResponse({"ok": False}, status=400)
    services.record_sql_error(request.user, payload.get("error"), assignment_id=assignment.id)
    return JsonResponse({"ok": True})


def _feedback_text(report):
    """Текст для `Submission.feedback` — чтобы преподаватель видел ту же картину.

    В отличие от ответа браузеру, здесь всё складывается в одну строку: поле хранит
    текст, и по нему потом строится выборка для дашборда (этап 11).
    """
    if report["passed"]:
        return "Автопроверка: верно"
    parts = [f"{c['label']}: {c['detail']}" for c in report["checks"] if not c["ok"]]
    if not parts:
        return "Автопроверка: неверно"
    return "Автопроверка: неверно — " + "; ".join(parts)
