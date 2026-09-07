"""Дашборд преподавателя и аналитика (этап 11).

Всё под `teacher_required`, и каждый отчёт ограничен курсами этого преподавателя —
см. `reports.visible_courses`. Студент сюда не попадает.
"""

import csv

from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.decorators import teacher_required
from accounts.models import User
from assessments.models import Assignment, Submission
from gamification import services as gamification
from gamification.levels import level_progress

from . import grading, reports
from .cache import cached_report, report_key


def _selected_course(request, teacher):
    """Курс из строки запроса `?course=<slug>`, если он доступен преподавателю."""
    slug = request.GET.get("course")
    if not slug:
        return None
    return get_object_or_404(reports.visible_courses(teacher), slug=slug)


def _selected_group(request, teacher):
    """Группа из `?group=<id>` — только из числа своих.

    Фильтрация идёт по `visible_groups`, а не по всем группам: иначе чужую группу
    можно было бы подставить в строку запроса и увидеть её состав.
    """
    gid = request.GET.get("group")
    if not gid:
        return None
    return get_object_or_404(reports.visible_groups(teacher), pk=gid)


def _report_context(request, teacher):
    """Общее для страницы ведомости и обеих выгрузок: курс, группа, строки.

    Если курс не выбран, а он у преподавателя единственный — берём его: выбирать
    из одного варианта незачем.
    """
    course = _selected_course(request, teacher)
    if course is None:
        courses = list(reports.visible_courses(teacher))
        course = courses[0] if len(courses) == 1 else None

    group = _selected_group(request, teacher)
    rows = reports.gradebook_rows(course, group) if course is not None else []
    return course, group, rows


@teacher_required
def dashboard(request):
    """Зоны риска: кто отстаёт и почему."""
    teacher = request.user
    course = _selected_course(request, teacher)
    rows = reports.student_rows(teacher, course)
    return render(
        request,
        "teaching/dashboard.html",
        {
            "rows": rows,
            "summary": reports.summarize(rows),
            "courses": reports.visible_courses(teacher),
            "selected": course,
            "manual_queue": reports.manual_queue(teacher),
        },
    )


@teacher_required
def analytics(request):
    """Трудность уроков, ошибки в SQL, анализ вопросов, карта тем, активность."""
    teacher = request.user
    course = _selected_course(request, teacher)

    # Самая тяжёлая страница платформы: три отчёта по всем урокам, вопросам и темам.
    # Держим посчитанное в кэше — на паре преподаватель обновляет её несколько раз
    # подряд, и каждый раз собирать заново незачем (см. learning/cache.py).
    topics, topic_stats = cached_report(
        report_key("topics", teacher), lambda: reports.topic_mastery_rows(teacher)
    )
    difficulty = cached_report(
        report_key("difficulty", teacher, course),
        lambda: reports.lesson_difficulty_rows(teacher, course),
    )

    # Сводка по расхождениям — то, ради чего этот отчёт и нужен.
    def count_label(name):
        return sum(1 for r in difficulty if r["divergence"] and r["divergence"]["label"] == name)

    return render(
        request,
        "teaching/analytics.html",
        {
            "difficulty": difficulty,
            "div_summary": {
                "underestimate": count_label("недооценивают"),
                "overestimate": count_label("переоценивают"),
                "match": count_label("совпадает"),
            },
            "items": cached_report(
                report_key("items", teacher), lambda: reports.item_analysis_rows(teacher)
            ),
            "topics": topics,
            "topic_stats": topic_stats,
            "activity": cached_report(
                report_key("activity", teacher), lambda: reports.activity_breakdown(teacher)
            ),
            "sql_errors": cached_report(
                report_key("sqlerrors", teacher, course),
                lambda: reports.sql_error_rows(teacher, course),
            ),
            "courses": reports.visible_courses(teacher),
            "selected": course,
        },
    )


@teacher_required
def report(request):
    """Ведомость по группе — печатная форма (§17.11.5).

    Верстается как документ, а не как страница: печать идёт штатным Ctrl+P браузера
    (`@media print` в `terminal.css`). Библиотека генерации PDF сюда не заводится
    сознательно — она тянет системные зависимости и ломает простоту установки,
    ради которой делался этап 9.5.
    """
    teacher = request.user
    course, group, rows = _report_context(request, teacher)
    return render(
        request,
        "teaching/report.html",
        {
            "rows": rows,
            "summary": reports.gradebook_summary(rows),
            "courses": reports.visible_courses(teacher),
            "groups": reports.visible_groups(teacher),
            "selected": course,
            "group": group,
            "teacher": teacher,
            "today": timezone.now(),
        },
    )


@teacher_required
def submissions(request):
    """Очередь проверки работ: что сдали студенты по курсам этого преподавателя."""
    page = Paginator(reports.submission_queryset(request.user), settings.PAGE_SIZE).get_page(
        request.GET.get("page")
    )
    return render(
        request,
        "teaching/submissions.html",
        {
            "rows": reports.decorate_submissions(list(page.object_list)),
            "page": page,
            "summary": reports.submission_summary(request.user),
            "error": request.GET.get("error"),
        },
    )


@teacher_required
@require_POST
def grade(request, submission_id):
    """Выставить балл и отзыв за сдачу.

    Работа берётся из `visible_submissions`, а не из всех: иначе чужую сдачу можно
    было бы оценить, подставив её идентификатор в форму.
    """
    submission = get_object_or_404(
        reports.visible_submissions(request.user).select_related("assignment"), pk=submission_id
    )
    data, error = grading.clean_grade(
        request.POST.get("score"),
        request.POST.get("feedback"),
        request.POST.get("status"),
        submission.assignment.max_score,
    )
    target = reverse("teaching:submissions")
    if error:
        return redirect(f"{target}?error={error}#s-{submission.pk}")

    submission.score = data["score"]
    submission.feedback = data["feedback"]
    submission.status = data["status"]
    submission.graded_by = request.user
    submission.graded_at = timezone.now()
    submission.save(update_fields=["score", "feedback", "status", "graded_by", "graded_at"])
    return redirect(f"{target}#s-{submission.pk}")


@teacher_required
def student(request, user_id):
    """Карточка студента: что он прошёл по курсам этого преподавателя."""
    person = get_object_or_404(User, pk=user_id)
    if not reports.is_my_student(request.user, person):
        raise Http404("Студент не найден")

    achievements = gamification.get_achievements_for_user(person)
    return render(
        request,
        "teaching/student.html",
        {
            "person": person,
            "card": reports.student_card(request.user, person),
            "achievements": achievements,
            "earned_count": sum(1 for a in achievements if a["earned"]),
            "level": level_progress(person.xp or 0),
            "project_defended": any(
                a["code"] == "project_defender" and a["earned"] for a in achievements
            ),
            "final_assignment": Assignment.objects.filter(
                is_final=True, course__in=reports.visible_courses(request.user)
            ).first(),
            "error": request.GET.get("error"),
        },
    )


@teacher_required
@require_POST
def defend_project(request, user_id):
    """Зачесть защиту итогового проекта: оценённая сдача + достижение.

    Итоговое задание берётся только из курсов этого преподавателя — зачесть защиту
    по чужой дисциплине нельзя.
    """
    person = get_object_or_404(User, pk=user_id)
    target = reverse("teaching:student", args=[person.pk])
    if not reports.is_my_student(request.user, person):
        raise Http404("Студент не найден")

    assignment = Assignment.objects.filter(
        is_final=True, course__in=reports.visible_courses(request.user)
    ).first()
    if assignment is None:
        return redirect(f"{target}?error=Итоговое задание не найдено")

    Submission.objects.update_or_create(
        assignment=assignment,
        user=person,
        defaults={
            "score": assignment.max_score,
            "status": "graded",
            "graded_by": request.user,
            "graded_at": timezone.now(),
        },
    )
    gamification.award_achievement(person, "project_defender")
    return redirect(target)


def _csv_response(filename, header, rows):
    """CSV с BOM и разделителем `;` — чтобы Excel на русской локали открыл файл сразу.

    Без BOM Excel читает UTF-8 как cp1251 и показывает кракозябры; с запятой в роли
    разделителя он складывает всю строку в одну ячейку.
    """
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    stamp = timezone.now().strftime("%Y-%m-%d")
    response["Content-Disposition"] = f'attachment; filename="{filename}-{stamp}.csv"'
    response.write("﻿")
    writer = csv.writer(response, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)
    writer.writerows(rows)
    return response


@teacher_required
def export_students(request):
    """Выгрузка таблицы студентов с индексом риска."""
    teacher = request.user
    course = _selected_course(request, teacher)
    rows = reports.student_rows(teacher, course)
    return _csv_response(
        "dataedu-studenty",
        [
            "Логин",
            "Имя",
            "Курс",
            "Уроков пройдено",
            "Уроков всего",
            "Прогресс, %",
            "Средний балл",
            "Дней без активности",
            "Риск",
            "Зона",
        ],
        [
            [
                r["user"].username,
                r["user"].display_name,
                r["course"].title,
                r["lessons_done"],
                r["lessons_total"],
                r["completion"],
                "" if r["avg_score"] is None else r["avg_score"],
                "" if r["days_inactive"] is None else r["days_inactive"],
                r["risk"],
                r["zone"]["label"],
            ]
            for r in rows
        ],
    )


@teacher_required
def export_difficulty(request):
    """Выгрузка сопоставления объективной и субъективной трудности."""
    teacher = request.user
    course = _selected_course(request, teacher)
    rows = reports.lesson_difficulty_rows(teacher, course)
    return _csv_response(
        "dataedu-trudnost",
        [
            "Курс",
            "Неделя",
            "Урок",
            "Рефлексий",
            "Понятность (1-5)",
            "Субъективная трудность (0-100)",
            "Объективная трудность (0-100)",
            "Расхождение",
            "Оценка",
            "Средний балл теста",
            "Попыток в среднем",
            "Неверных решений, %",
        ],
        [
            [
                r["course"].title,
                r["week"] or "",
                r["lesson"].title,
                r["n_reflections"],
                "" if r["clarity"] is None else r["clarity"],
                "" if r["subjective"] is None else r["subjective"],
                "" if r["objective"] is None else r["objective"],
                r["divergence"]["delta"] if r["divergence"] else "",
                r["divergence"]["label"] if r["divergence"] else "",
                "" if r["avg_score"] is None else r["avg_score"],
                "" if r["avg_attempts"] is None else r["avg_attempts"],
                "" if r["failed_share"] is None else r["failed_share"],
            ]
            for r in rows
        ],
    )


@teacher_required
def export_vedomost(request):
    """Ведомость в CSV — для учебной части: та же таблица, что на печатной форме."""
    teacher = request.user
    course, group, rows = _report_context(request, teacher)
    return _csv_response(
        "dataedu-vedomost",
        [
            "№",
            "Код участника",
            "Имя",
            "Уроков пройдено",
            "Уроков всего",
            "Тестов сдано",
            "Тестов всего",
            "Результат тестов, %",
            "Заданий зачтено",
            "Заданий всего",
            "На проверке",
            "Итог (0-100)",
            "Отметка",
            "Зачёт",
        ],
        [
            [
                i,
                r["user"].username,
                r["user"].display_name,
                r["lessons_done"],
                r["lessons_total"],
                r["tests_taken"],
                r["tests_total"],
                "" if r["tests_pct"] is None else r["tests_pct"],
                r["assignments_done"],
                r["assignments_total"],
                r["pending"],
                "" if r["score"] is None else r["score"],
                r["grade"]["mark"] or "",
                r["verdict"]["label"],
            ]
            for i, r in enumerate(rows, start=1)
        ],
    )


@teacher_required
def export_moodle(request):
    """Выгрузка под импорт в журнал оценок Moodle.

    Формат намеренно отличается от остальных выгрузок платформы:

    - **без BOM.** Excel без него читает UTF-8 как cp1251, но мастер импорта Moodle
      приклеивает BOM к имени первого столбца, и `username` перестаёт опознаваться;
    - **разделитель `,`.** Значение по умолчанию в мастере импорта Moodle;
    - **латинские заголовки.** Столбцы сопоставляются вручную в мастере, и латиница
      снимает вопрос кодировки на этом шаге.

    Сопоставление студентов идёт по логину: у обезличенных учётных записей апробации
    email пуст (§17.14), поэтому «Определять пользователя по» нужно ставить в
    «Имя пользователя», а логины в Moodle и DataEdu должны совпадать.
    """
    teacher = request.user
    course, group, rows = _report_context(request, teacher)

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    stamp = timezone.now().strftime("%Y-%m-%d")
    response["Content-Disposition"] = f'attachment; filename="dataedu-moodle-{stamp}.csv"'
    writer = csv.writer(response, delimiter=",", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["username", "email", "grade", "feedback"])
    for r in rows:
        writer.writerow(
            [
                r["user"].username,
                r["user"].email or "",
                "" if r["score"] is None else r["score"],
                "Уроки {}/{}, тесты {}%, задания {}/{}".format(
                    r["lessons_done"],
                    r["lessons_total"],
                    0 if r["tests_pct"] is None else r["tests_pct"],
                    r["assignments_done"],
                    r["assignments_total"],
                ),
            ]
        )
    return response
