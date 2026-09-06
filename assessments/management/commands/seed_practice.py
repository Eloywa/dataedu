"""Демо-задания с автопроверкой: общая заготовка данных (students+groups) и
несколько SELECT-задач, где порядок строк не важен (фильтры, JOIN, агрегаты).

**Эталоны заданы прямо здесь, а не считаются при запуске.** Расчёт на сервере
требует PostgreSQL, а профиль разработки работает на файловой базе — команда
падала бы ровно там, где нужнее всего. Значения ниже посчитаны в PGlite, том же
движке, в котором запрос выполняет студент, поэтому расхождения диалектов
исключены.

Если менять `expected_sql`, эталон надо пересчитать: откройте задание в админке и
нажмите «Посчитать эталон» — расчёт идёт в браузере и от базы Django не зависит.
Забыть об этом трудно: при правке запроса админка сама обнуляет сохранённый эталон.
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
        "expected_result": {
            "columns": ["full_name"],
            "rows": [
                ["Анна Соколова"],
                ["Дмитрий Соколов"],
                ["Мария Иванова"],
                ["Егор Новиков"],
            ],
        },
    },
    {
        "title": "Выбрать всех студентов",
        "level": "basic",
        "description": "Выведите все столбцы таблицы students: id, full_name, group_id, xp.",
        "expected_sql": "SELECT id, full_name, group_id, xp FROM students;",
        "expected_result": {
            "columns": ["id", "full_name", "group_id", "xp"],
            "rows": [
                [1, "Анна Соколова", 1, 320],
                [2, "Дмитрий Соколов", 1, 180],
                [3, "Мария Иванова", 1, 240],
                [4, "Павел Кузнецов", 2, 90],
                [5, "Ольга Попова", 2, 410],
                [6, "Артём Михайлов", 2, 0],
                [7, "Полина Захарова", 2, 150],
                [8, "Денис Григорьев", 3, 200],
                [9, "Виктория Иванова", 3, 365],
                [10, "Глеб Тимофеев", 3, 130],
                [11, "Егор Новиков", 1, 275],
                [12, "Софья Морозова", 3, 55],
            ],
        },
    },
    {
        "title": "Отличники (xp ≥ 300)",
        "level": "basic",
        "description": "Выведите full_name и xp студентов, у которых xp не меньше 300.",
        "expected_sql": "SELECT full_name, xp FROM students WHERE xp >= 300;",
        "expected_result": {
            "columns": ["full_name", "xp"],
            "rows": [["Анна Соколова", 320], ["Ольга Попова", 410], ["Виктория Иванова", 365]],
        },
    },
    {
        "title": "Сколько студентов в каждой группе",
        "level": "medium",
        "description": "Выведите название группы (столбец name) и количество студентов в ней. "
        "Используйте JOIN и GROUP BY.",
        "expected_sql": "SELECT g.name, count(*) FROM students s JOIN groups g ON g.id = s.group_id "
        "GROUP BY g.name;",
        # Порядок строк при GROUP BY не определён — сравнение его и не требует.
        "expected_result": {
            "columns": ["name", "count"],
            "rows": [["ПИ-101", 4], ["ПИ-102", 4], ["МО-201", 4]],
        },
    },
    {
        "title": "Средний XP",
        "level": "medium",
        "description": "Выведите средний xp по всем студентам, округлённый до целого "
        "(одно число, функция round и avg).",
        "expected_sql": "SELECT round(avg(xp)) FROM students;",
        "expected_result": {"columns": ["round"], "rows": [["201"]]},
    },
]


class Command(BaseCommand):
    help = "Создать демо-задания с автопроверкой (SETUP students+groups + SELECT-задачи)."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="sql-s-nulya").first() or Course.objects.first()
        if course is None:
            self.stderr.write("Нет ни одного курса — сначала загрузите содержимое (load_dump).")
            return

        created = 0
        for t in TASKS:
            # Ищем по названию **среди всех курсов**, а не только внутри целевого:
            # часть заданий пришла из дампа и лежит в другом курсе, и сопоставление
            # по паре «курс + название» создавало для них дубль вместо обновления.
            existing = Assignment.objects.filter(title=t["title"]).order_by("created_at").first()
            obj, was_created = Assignment.objects.update_or_create(
                pk=existing.pk if existing else None,
                defaults={
                    "course": existing.course if existing else course,
                    "title": t["title"],
                    "description": t["description"],
                    "level": t["level"],
                    "type": "sql",
                    "setup_sql": SETUP,
                    "expected_sql": t["expected_sql"],
                    "expected_result": t["expected_result"],
                    "max_score": 10,
                    "is_final": False,
                },
            )
            created += 1 if was_created else 0

        # Задание на CREATE TABLE автопроверке не поддаётся: запрос студента не
        # возвращает строк, сравнивать нечего. Помечаем его типом ddl, чтобы оно
        # честно уходило преподавателю, а не предлагало студенту кнопку проверки.
        ddl = Assignment.objects.filter(title="Создать таблицу студентов").exclude(type="ddl")
        moved = ddl.update(type="ddl", expected_result=None)

        if options["verbosity"]:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Заданий с автопроверкой: {len(TASKS)} (новых: {created}); "
                    f"переведено на ручную проверку: {moved}."
                )
            )
