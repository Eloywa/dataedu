"""Демо-задания с автопроверкой: общая заготовка данных (students+groups) и
несколько SELECT-задач, где порядок строк не важен (фильтры, JOIN, агрегаты).
"""

from django.core.management.base import BaseCommand

from assessments.models import Assignment
from courses.models import Course

SETUP = """
CREATE TABLE groups (
  id integer PRIMARY KEY,
  name text NOT NULL,
  curator text
);
INSERT INTO groups (id, name, curator) VALUES
  (1, 'ПИ-101', 'Иванов И. И.'),
  (2, 'ПИ-102', 'Петрова О. И.'),
  (3, 'МО-201', 'Сидоров С. С.');
CREATE TABLE students (
  id integer PRIMARY KEY,
  full_name text NOT NULL,
  group_id integer REFERENCES groups(id),
  xp integer NOT NULL DEFAULT 0
);
INSERT INTO students (id, full_name, group_id, xp) VALUES
  (1,  'Анна Соколова',     1, 320),
  (2,  'Дмитрий Соколов',   1, 180),
  (3,  'Мария Иванова',     1, 240),
  (4,  'Павел Кузнецов',    2, 90),
  (5,  'Ольга Попова',      2, 410),
  (6,  'Артём Михайлов',    2, 0),
  (7,  'Полина Захарова',   2, 150),
  (8,  'Денис Григорьев',   3, 200),
  (9,  'Виктория Иванова',  3, 365),
  (10, 'Глеб Тимофеев',     3, 130),
  (11, 'Егор Новиков',      1, 275),
  (12, 'Софья Морозова',    3, 55);
"""

TASKS = [
    {
        "title": "Студенты группы ПИ-101",
        "level": "basic",
        "description": "Выведите столбец full_name всех студентов из группы «ПИ-101» "
        "(используйте JOIN таблиц students и groups).",
        "expected_sql": "SELECT s.full_name FROM students s JOIN groups g ON g.id = s.group_id "
        "WHERE g.name = 'ПИ-101';",
    },
    {
        "title": "Отличники (xp ≥ 300)",
        "level": "basic",
        "description": "Выведите full_name и xp студентов, у которых xp не меньше 300.",
        "expected_sql": "SELECT full_name, xp FROM students WHERE xp >= 300;",
    },
    {
        "title": "Сколько студентов в каждой группе",
        "level": "medium",
        "description": "Выведите название группы (столбец name) и количество студентов в ней. "
        "Используйте JOIN и GROUP BY.",
        "expected_sql": "SELECT g.name, count(*) FROM students s JOIN groups g ON g.id = s.group_id "
        "GROUP BY g.name;",
    },
    {
        "title": "Средний XP",
        "level": "medium",
        "description": "Выведите средний xp по всем студентам, округлённый до целого "
        "(одно число, функция round и avg).",
        "expected_sql": "SELECT round(avg(xp)) FROM students;",
    },
]


class Command(BaseCommand):
    help = "Создать демо-задания с автопроверкой (SETUP students+groups + SELECT-задачи)."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="sql-s-nulya").first() or Course.objects.first()
        if course is None:
            self.stdout.write(self.style.ERROR("Нет ни одного курса."))
            return

        created = 0
        for t in TASKS:
            obj, was_created = Assignment.objects.update_or_create(
                course=course,
                title=t["title"],
                defaults={
                    "description": t["description"],
                    "level": t["level"],
                    "type": "sql",
                    "setup_sql": SETUP,
                    "expected_sql": t["expected_sql"],
                    "expected_result": None,
                    "max_score": 10,
                    "is_final": False,
                },
            )
            created += 1 if was_created else 0

        self.stdout.write(
            self.style.SUCCESS(
                f"Заданий обработано: {len(TASKS)} (новых: {created}). "
                "Запустите compute_expected для расчёта эталонов."
            )
        )
