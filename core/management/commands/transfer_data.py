"""Перелив данных из старой БД (dataedu, Next-версия) в текущую (dataedu_django).

Читает строки из исходной БД напрямую через psycopg и создаёт объекты Django ORM,
сохраняя исходные UUID-ключи и связи. Запускать на ПУСТЫХ таблицах назначения.
Чат (messages) сознательно не переносим.
"""

import psycopg
from django.conf import settings
from django.core.management.base import BaseCommand
from psycopg.rows import dict_row

from accounts.models import Role, User
from assessments.models import (
    AnswerOption,
    AnswerSubmission,
    Assignment,
    Question,
    Submission,
    Test,
    TestAttempt,
)
from courses.models import Course, CourseRating, CourseTopic, Lesson, Module, Topic
from gamification.models import Achievement, UserAchievement
from learning.models import Activity, Enrollment, LessonProgress, Reflection

SOURCE_DB = "dataedu"

# Порядок важен: родители раньше детей (FK).
PLAN = [
    ("roles", Role),
    ("users", User),
    ("topics", Topic),
    ("courses", Course),
    ("course_topics", CourseTopic),
    ("modules", Module),
    ("lessons", Lesson),
    ("course_ratings", CourseRating),
    ("tests", Test),
    ("questions", Question),
    ("answer_options", AnswerOption),
    ("test_attempts", TestAttempt),
    ("answer_submissions", AnswerSubmission),
    ("assignments", Assignment),
    ("submissions", Submission),
    ("enrollments", Enrollment),
    ("lesson_progress", LessonProgress),
    ("reflections", Reflection),
    ("activities", Activity),
    ("achievements", Achievement),
    ("user_achievements", UserAchievement),
]


def _source_dsn():
    db = settings.DATABASES["default"]
    return dict(
        host=db["HOST"], port=db["PORT"], user=db["USER"], password=db["PASSWORD"], dbname=SOURCE_DB
    )


class Command(BaseCommand):
    help = "Перелив данных из старой БД dataedu в текущую dataedu_django."

    def handle(self, *args, **options):
        dsn = _source_dsn()

        self.stdout.write("Перелив данных:")
        with psycopg.connect(row_factory=dict_row, **dsn) as src:
            for table, model in PLAN:
                rows = src.execute(f"SELECT * FROM {table}").fetchall()
                objs = []
                for r in rows:
                    if table == "users":
                        r.pop("password_hash", None)  # пароли пересоздадим штатно
                        obj = User(**r)
                        obj.set_unusable_password()
                        objs.append(obj)
                    elif table == "submissions":
                        r["graded_by_id"] = r.pop("graded_by", None)  # старая колонка без _id
                        objs.append(model(**r))
                    else:
                        objs.append(model(**r))

                if table == "course_topics":
                    # составной ключ — на всякий случай по одному
                    for o in objs:
                        o.save(force_insert=True)
                else:
                    model.objects.bulk_create(objs, batch_size=500)
                self.stdout.write(f"  {table}: {len(objs)}")

        # Сверка счётчиков источник/назначение
        self.stdout.write("")
        self.stdout.write("Сверка счётчиков (источник -> назначение):")
        all_ok = True
        with psycopg.connect(row_factory=dict_row, **dsn) as src:
            for table, model in PLAN:
                src_n = src.execute(f"SELECT count(*) AS n FROM {table}").fetchone()["n"]
                dst_n = model.objects.count()
                ok = src_n == dst_n
                all_ok = all_ok and ok
                self.stdout.write(f"  {'OK' if ok else 'XX'} {table}: {src_n} -> {dst_n}")

        if all_ok:
            self.stdout.write(self.style.SUCCESS("Все счётчики совпали."))
        else:
            self.stdout.write(self.style.ERROR("Есть расхождения — проверь вывод выше."))
