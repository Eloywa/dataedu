import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from courses.models import Lesson
from gamification import services

from .grading import diagnose
from .models import AnswerSubmission, Assignment, Submission, TestAttempt


@login_required
def lesson_test(request, lesson_id):
    lesson = get_object_or_404(Lesson.objects.select_related("module__course"), id=lesson_id)
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
            {"lesson": lesson, "test": test, "score": score, "is_passed": is_passed, "results": results},
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
    solved = set(
        Submission.objects.filter(user=request.user, score__gte=1).values_list("assignment_id", flat=True)
    )
    submitted = set(
        Submission.objects.filter(user=request.user).values_list("assignment_id", flat=True)
    )

    auto, manual = [], []
    for a in (
        Assignment.objects.select_related("course").order_by("course__title", "title")
    ):
        a.is_solved = a.id in solved
        a.is_submitted = a.id in submitted
        (auto if a.is_autocheckable else manual).append(a)

    return render(
        request,
        "assessments/practice_list.html",
        {"assignments": auto, "manual_assignments": manual},
    )


@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment.objects.select_related("course"), id=assignment_id)
    solved = Submission.objects.filter(
        user=request.user, assignment=assignment, score__gte=1
    ).exists()
    last = (
        Submission.objects.filter(user=request.user, assignment=assignment)
        .order_by("-submitted_at")
        .first()
    )
    return render(
        request,
        "assessments/assignment_detail.html",
        {"assignment": assignment, "solved": solved, "last_submission": last},
    )


@login_required
@require_POST
def check_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if not assignment.is_autocheckable:
        return JsonResponse(
            {
                "passed": False,
                "message": "Это задание проверяет преподаватель — автопроверки у него нет.",
            },
            status=400,
        )

    try:
        payload = json.loads(request.body)
        sql = (payload.get("sql") or "").strip()
        columns = payload.get("columns") or []
        rows = payload.get("rows") or []
    except (ValueError, TypeError):
        return JsonResponse({"passed": False, "message": "Некорректные данные."}, status=400)

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

    return JsonResponse(
        {"passed": passed, "checks": report["checks"], "hint": report["hint"]}
    )


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
