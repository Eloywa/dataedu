"""Привязка заданий курса «SQL с нуля» к их урокам.

Задания из `seed_practice` появились раньше, чем связь с уроками стала видна на сайте, и
остались без неё. Текст и эталоны заданий не меняются. Если курса или урока нет (база
пустая или из другого дампа), задание просто остаётся как было.
"""

from django.db import migrations

LINKS = {
    "Отличники (xp ≥ 300)": "Фильтрация строк: WHERE",
    "Студенты группы ПИ-101": "Объединение таблиц: JOIN",
    "Сколько студентов в каждой группе": "Группировка: GROUP BY и HAVING",
    "Средний XP": "Сортировка и агрегатные функции",
}


def link(apps, schema_editor):
    Assignment = apps.get_model("assessments", "Assignment")
    Lesson = apps.get_model("courses", "Lesson")
    for title, lesson_title in LINKS.items():
        for task in Assignment.objects.filter(title=title, lesson__isnull=True):
            lesson = Lesson.objects.filter(
                module__course_id=task.course_id, title=lesson_title
            ).first()
            if lesson:
                task.lesson = lesson
                task.save(update_fields=["lesson"])


class Migration(migrations.Migration):
    dependencies = [
        ("assessments", "0008_project_tickets"),
    ]

    operations = [
        migrations.RunPython(link, migrations.RunPython.noop),
    ]
