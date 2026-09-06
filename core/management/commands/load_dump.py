"""Наполнение платформы учебным содержимым из дампа первой версии.

Зачем это нужно. Django-версия создаёт схему миграциями, но пустая платформа
бесполезна: без курсов не посмотреть ни каталог, ни аналитику, ни ведомость.
Всё содержимое — семь курсов с теорией, тесты, задания и демонстрационные данные
об обучении — уже существует, но лежит в дампе PostgreSQL от Next-версии.

Команда читает **текстовый дамп** (`db/dump.sql`), а не подключается ко второй
базе: подключение потребовало бы поднятого сервера с той базой на машине, где
проект разворачивают. Дамп — обычный файл, он лежит в репозитории, и развёртывание
сводится к `migrate` + `load_dump`.

Что делает разбор:

- берёт блоки `COPY … FROM stdin;` (табличный формат pg_dump);
- раскрывает экранирование: `\\N` — NULL, `\\n`, `\\t`, `\\r`, `\\\\`;
- переставляет и переименовывает столбцы там, где схема разошлась (`full_name` →
  `display_name`, логин выводится из email, `topic_id` и эталоны заданий в дампе
  отсутствуют — они появились уже в Django-версии);
- вставляет пачками, в порядке зависимостей.

Пароли из дампа **не переносятся**: там хеши scrypt от Next-версии, Django их не
понимает. Пароли задаются отдельно — `manage.py set_demo_passwords`.
"""

import re
import uuid
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

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
from messaging.models import Message

COPY_RE = re.compile(r"^COPY public\.(\w+) \(([^)]*)\) FROM stdin;$")

# Экранирование текстового формата COPY. Порядок важен: обратный слэш
# раскрывается последним, иначе `\\n` превратился бы в перевод строки.
ESCAPES = [("\\t", "\t"), ("\\n", "\n"), ("\\r", "\r"), ("\\b", "\b"), ("\\f", "\f"), ("\\v", "\v")]


def unescape(value):
    if value == "\\N":
        return None
    out = []
    i = 0
    while i < len(value):
        if value[i] == "\\" and i + 1 < len(value):
            pair = value[i : i + 2]
            if pair == "\\\\":
                out.append("\\")
                i += 2
                continue
            replacement = dict(ESCAPES).get(pair)
            if replacement is not None:
                out.append(replacement)
                i += 2
                continue
        out.append(value[i])
        i += 1
    return "".join(out)


def parse_dump(text):
    """{имя таблицы: (столбцы, [строки])} из всех блоков COPY."""
    tables = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        match = COPY_RE.match(lines[i].strip())
        if not match:
            i += 1
            continue
        name = match.group(1)
        columns = [c.strip() for c in match.group(2).split(",")]
        rows = []
        i += 1
        while i < len(lines) and lines[i] != "\\.":
            rows.append([unescape(v) for v in lines[i].split("\t")])
            i += 1
        tables[name] = (columns, rows)
        i += 1
    return tables


def as_bool(value):
    return None if value is None else value == "t"


def as_int(value):
    return None if value is None else int(value)


def as_dec(value):
    return None if value is None else value


def username_from_email(email, taken):
    """Логин-псевдоним из локальной части адреса — то же правило, что в миграции 0002."""
    base = (email or "").split("@")[0].strip().lower()
    base = "".join(ch for ch in base if ch.isalnum() or ch in "._-") or "user"
    candidate, n = base, 1
    while candidate in taken:
        n += 1
        candidate = f"{base}{n}"
    taken.add(candidate)
    return candidate


class Command(BaseCommand):
    help = "Загрузить учебное содержимое и демо-данные из db/dump.sql"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default=None,
            help="Путь к дампу (по умолчанию db/dump.sql в корне проекта).",
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Очистить учебные таблицы перед загрузкой. Учётные записи "
            "суперпользователей не трогаются.",
        )

    def handle(self, *args, **options):
        path = Path(options["path"]) if options["path"] else settings.BASE_DIR / "db" / "dump.sql"
        if not path.exists():
            raise CommandError(f"Дамп не найден: {path}")

        tables = parse_dump(path.read_text(encoding="utf-8"))
        if not tables:
            raise CommandError("В файле не найдено ни одного блока COPY")

        with transaction.atomic():
            if options["flush"]:
                self._flush()
            counts = self._load(tables)

        if options["verbosity"]:
            total = sum(counts.values())
            self.stdout.write(self.style.SUCCESS(f"Загружено строк: {total}"))
            for name, n in counts.items():
                if n:
                    self.stdout.write(f"  {name}: {n}")
            self.stdout.write(
                "Пароли из дампа не переносятся. Задайте их командой set_demo_passwords."
            )

    def _flush(self):
        """Очистка в обратном порядке зависимостей."""
        for model in (
            Message,
            Activity,
            UserAchievement,
            Achievement,
            Reflection,
            LessonProgress,
            AnswerSubmission,
            TestAttempt,
            Submission,
            Assignment,
            AnswerOption,
            Question,
            Test,
            Enrollment,
            CourseRating,
            Lesson,
            Module,
            CourseTopic,
            Course,
            Topic,
        ):
            model.objects.all().delete()
        # Суперпользователи остаются: иначе после перезагрузки данных некому
        # зайти в админку на машине, где проект только что развернули.
        User.objects.filter(is_superuser=False).delete()
        Role.objects.all().delete()

    def _load(self, tables):
        counts = {}

        def rows_of(name):
            if name not in tables:
                return [], []
            columns, rows = tables[name]
            return columns, [dict(zip(columns, row)) for row in rows]

        # --- Роли и пользователи ------------------------------------------
        _, roles = rows_of("roles")
        Role.objects.bulk_create(
            [
                Role(id=r["id"], code=r["code"], name=r["name"], description=r["description"])
                for r in roles
            ],
            ignore_conflicts=True,
        )
        counts["roles"] = len(roles)

        _, users = rows_of("users")
        taken = set(User.objects.values_list("username", flat=True))
        existing_users = set(str(pk) for pk in User.objects.values_list("id", flat=True))
        new_users = []
        for u in users:
            if u["id"] in existing_users:
                continue
            person = User(
                id=u["id"],
                username=username_from_email(u["email"], taken),
                # Email из дампа демонстрационный. Он сохраняется, потому что на нём
                # держится узнаваемость демо-аккаунтов; в реальной эксплуатации поле
                # необязательно и остаётся пустым (см. правовой контур).
                email=u["email"] or None,
                display_name=u["full_name"] or "",
                role_id=u["role_id"],
                avatar_url=u["avatar_url"],
                xp=as_int(u["xp"]) or 0,
                level=as_int(u["level"]) or 1,
                is_active=as_bool(u["is_active"]),
                last_seen_at=u["last_seen_at"],
                created_at=u["created_at"],
                updated_at=u["updated_at"],
            )
            # Хеши scrypt из Next-версии Django не понимает: пароль помечается
            # неустановленным, задаётся отдельной командой.
            person.set_unusable_password()
            new_users.append(person)
        User.objects.bulk_create(new_users, ignore_conflicts=True)
        counts["users"] = len(new_users)

        # Преподаватели и админы должны попадать в админку.
        User.objects.filter(role__code__in=("teacher", "admin")).update(is_staff=True)

        # --- Курсы ---------------------------------------------------------
        counts["topics"] = self._bulk(
            Topic, rows_of("topics")[1], lambda r: Topic(id=r["id"], code=r["code"], name=r["name"])
        )
        counts["courses"] = self._bulk(
            Course,
            rows_of("courses")[1],
            lambda r: Course(
                id=r["id"],
                title=r["title"],
                slug=r["slug"],
                description=r["description"],
                semester=r["semester"],
                author_id=r["author_id"],
                is_published=as_bool(r["is_published"]),
                created_at=r["created_at"],
                level=r["level"],
                cover_url=r["cover_url"],
            ),
        )
        counts["course_topics"] = self._bulk(
            CourseTopic,
            rows_of("course_topics")[1],
            lambda r: CourseTopic(course_id=r["course_id"], topic_id=r["topic_id"]),
        )
        counts["modules"] = self._bulk(
            Module,
            rows_of("modules")[1],
            lambda r: Module(
                id=r["id"],
                course_id=r["course_id"],
                title=r["title"],
                description=r["description"],
                order_index=as_int(r["order_index"]),
                week_number=as_int(r["week_number"]),
            ),
        )
        counts["lessons"] = self._bulk(
            Lesson,
            rows_of("lessons")[1],
            lambda r: Lesson(
                id=r["id"],
                module_id=r["module_id"],
                title=r["title"],
                theory_content=r["theory_content"],
                order_index=as_int(r["order_index"]),
                est_minutes=as_int(r["est_minutes"]),
                xp_reward=as_int(r["xp_reward"]) or 0,
            ),
        )
        counts["course_ratings"] = self._bulk(
            CourseRating,
            rows_of("course_ratings")[1],
            lambda r: CourseRating(
                id=r["id"],
                course_id=r["course_id"],
                user_id=r["user_id"],
                rating=as_int(r["rating"]),
                comment=r["comment"],
                created_at=r["created_at"],
            ),
        )

        # --- Тесты и задания -----------------------------------------------
        counts["tests"] = self._bulk(
            Test,
            rows_of("tests")[1],
            lambda r: Test(
                id=r["id"],
                lesson_id=r["lesson_id"],
                title=r["title"],
                pass_score=as_int(r["pass_score"]),
                time_limit_sec=as_int(r["time_limit_sec"]),
            ),
        )
        counts["questions"] = self._bulk(
            Question,
            rows_of("questions")[1],
            # topic_id в дампе нет: связь «вопрос → тема» появилась уже в
            # Django-версии. Проставляется командой assign_question_topics.
            lambda r: Question(
                id=r["id"],
                test_id=r["test_id"],
                text=r["text"],
                type=r["type"],
                points=as_int(r["points"]),
                order_index=as_int(r["order_index"]),
            ),
        )
        counts["answer_options"] = self._bulk(
            AnswerOption,
            rows_of("answer_options")[1],
            lambda r: AnswerOption(
                id=r["id"],
                question_id=r["question_id"],
                text=r["text"],
                is_correct=as_bool(r["is_correct"]),
                order_index=as_int(r["order_index"]),
            ),
        )
        counts["assignments"] = self._bulk(
            Assignment,
            rows_of("assignments")[1],
            # setup_sql и expected_result в дампе отсутствуют: автопроверка на
            # PGlite появилась в Django-версии. Эталоны считает compute_expected.
            lambda r: Assignment(
                id=r["id"],
                course_id=r["course_id"],
                lesson_id=r["lesson_id"],
                title=r["title"],
                description=r["description"],
                level=r["level"],
                type=r["type"],
                expected_sql=r["expected_sql"],
                max_score=as_int(r["max_score"]),
                is_final=as_bool(r["is_final"]),
                created_at=r["created_at"],
            ),
        )

        # --- Обучение -------------------------------------------------------
        counts["enrollments"] = self._bulk(
            Enrollment,
            rows_of("enrollments")[1],
            lambda r: Enrollment(
                id=r["id"],
                user_id=r["user_id"],
                course_id=r["course_id"],
                status=r["status"],
                enrolled_at=r["enrolled_at"],
                completed_at=r["completed_at"],
            ),
        )
        counts["lesson_progress"] = self._bulk(
            LessonProgress,
            rows_of("lesson_progress")[1],
            lambda r: LessonProgress(
                id=r["id"],
                user_id=r["user_id"],
                lesson_id=r["lesson_id"],
                status=r["status"],
                time_spent_sec=as_int(r["time_spent_sec"]) or 0,
                visits=as_int(r["visits"]) or 0,
                started_at=r["started_at"],
                completed_at=r["completed_at"],
            ),
        )
        counts["test_attempts"] = self._bulk(
            TestAttempt,
            rows_of("test_attempts")[1],
            lambda r: TestAttempt(
                id=r["id"],
                user_id=r["user_id"],
                test_id=r["test_id"],
                score=as_dec(r["score"]),
                is_passed=as_bool(r["is_passed"]),
                started_at=r["started_at"],
                finished_at=r["finished_at"],
            ),
        )
        counts["answer_submissions"] = self._bulk(
            AnswerSubmission,
            rows_of("answer_submissions")[1],
            lambda r: AnswerSubmission(
                id=r["id"],
                attempt_id=r["attempt_id"],
                question_id=r["question_id"],
                answer_option_id=r["answer_option_id"],
                text_answer=r["text_answer"],
                is_correct=as_bool(r["is_correct"]),
            ),
        )
        counts["submissions"] = self._bulk(
            Submission,
            rows_of("submissions")[1],
            lambda r: Submission(
                id=r["id"],
                assignment_id=r["assignment_id"],
                user_id=r["user_id"],
                sql_query=r["sql_query"],
                file_url=r["file_url"],
                text_answer=r["text_answer"],
                score=as_dec(r["score"]),
                feedback=r["feedback"],
                status=r["status"],
                graded_by_id=r["graded_by"],
                submitted_at=r["submitted_at"],
                graded_at=r["graded_at"],
            ),
        )
        counts["reflections"] = self._bulk(
            Reflection,
            rows_of("reflections")[1],
            lambda r: Reflection(
                id=r["id"],
                user_id=r["user_id"],
                lesson_id=r["lesson_id"],
                clarity_rating=as_int(r["clarity_rating"]),
                difficulty_rating=as_int(r["difficulty_rating"]),
                comment=r["comment"],
                created_at=r["created_at"],
            ),
        )
        counts["activities"] = self._bulk(
            Activity,
            rows_of("activities")[1],
            lambda r: Activity(
                id=r["id"],
                user_id=r["user_id"],
                type=r["type"],
                entity_type=r["entity_type"],
                entity_id=uuid.UUID(r["entity_id"]) if r["entity_id"] else None,
                metadata=None,
                created_at=r["created_at"],
            ),
        )

        # --- Геймификация и переписка ---------------------------------------
        counts["achievements"] = self._bulk(
            Achievement,
            rows_of("achievements")[1],
            lambda r: Achievement(
                id=r["id"],
                code=r["code"],
                title=r["title"],
                description=r["description"],
                icon=r["icon"],
                xp_reward=as_int(r["xp_reward"]) or 0,
            ),
        )
        counts["user_achievements"] = self._bulk(
            UserAchievement,
            rows_of("user_achievements")[1],
            lambda r: UserAchievement(
                id=r["id"],
                user_id=r["user_id"],
                achievement_id=r["achievement_id"],
                awarded_at=r["awarded_at"],
            ),
        )
        counts["messages"] = self._bulk(
            Message,
            rows_of("messages")[1],
            lambda r: Message(
                id=r["id"],
                sender_id=r["sender_id"],
                recipient_id=r["recipient_id"],
                course_id=r["course_id"],
                body=r["body"],
                created_at=r["created_at"],
                read_at=r["read_at"],
            ),
        )
        return counts

    def _bulk(self, model, rows, build):
        """Вставка пачкой с пропуском уже существующего.

        `ignore_conflicts` делает команду повторяемой: запуск на непустой базе
        ничего не ломает и не задваивает — это важно, потому что развёртывание
        часто повторяют, а не начинают с чистого листа.
        """
        if not rows:
            return 0
        objects = [build(r) for r in rows]
        model.objects.bulk_create(objects, batch_size=500, ignore_conflicts=True)
        return len(objects)
