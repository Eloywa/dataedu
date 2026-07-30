"""Дашборд преподавателя и аналитика (этап 11).

Всё под `teacher_required`, и каждый отчёт ограничен курсами этого преподавателя —
см. `reports.visible_courses`. Студент сюда не попадает.
"""

import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from accounts.decorators import teacher_required

from . import reports


def _selected_course(request, teacher):
    """Курс из строки запроса `?course=<slug>`, если он доступен преподавателю."""
    slug = request.GET.get("course")
    if not slug:
        return None
    return get_object_or_404(reports.visible_courses(teacher), slug=slug)


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
    """Трудность уроков, анализ вопросов, карта тем, активность."""
    teacher = request.user
    course = _selected_course(request, teacher)
    topics, topic_stats = reports.topic_mastery_rows(teacher)
    difficulty = reports.lesson_difficulty_rows(teacher, course)

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
            "items": reports.item_analysis_rows(teacher),
            "topics": topics,
            "topic_stats": topic_stats,
            "activity": reports.activity_breakdown(teacher),
            "courses": reports.visible_courses(teacher),
            "selected": course,
        },
    )


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
            "Логин", "Имя", "Курс", "Уроков пройдено", "Уроков всего",
            "Прогресс, %", "Средний балл", "Дней без активности", "Риск", "Зона",
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
            "Курс", "Неделя", "Урок", "Рефлексий", "Понятность (1-5)",
            "Субъективная трудность (0-100)", "Объективная трудность (0-100)",
            "Расхождение", "Оценка", "Средний балл теста", "Попыток в среднем",
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
