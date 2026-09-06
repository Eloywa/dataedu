"""Проставить темы вопросам — для карты освоения по темам (этап 11).

Связь «вопрос → тема» появилась на этапе 11, а вопросов в базе 116, и вручную
размечать их в админке долго. Команда делает первичную разметку, которую
преподаватель потом правит точечно (в списке вопросов тема редактируется прямо
в строке).

Логика в два шага:

1. **По ключевым словам** в тексте вопроса и названии урока. Слова подобраны так,
   чтобы не пересекаться между темами; при нескольких совпадениях берётся тема
   с большим числом попаданий.
2. **Откат на основную тему курса** (первая запись `CourseTopic`), если ключевых
   слов не нашлось. Это заведомо грубее, но лучше пустой карты: у курса тема
   всегда осмысленная.

Разметка не затирает уже проставленные темы — только заполняет пустые
(`--force` меняет поведение). Сначала стоит посмотреть `--dry-run`.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from assessments.models import Question
from courses.models import CourseTopic, Topic

# Ключевые слова в нижнем регистре. Порядок не важен: выбирается тема с наибольшим
# числом совпадений, при равенстве — первая по списку.
KEYWORDS = {
    "Нормализация": [
        "нормализ",
        "нормальн",
        "избыточност",
        "аномали",
        "1нф",
        "2нф",
        "3нф",
        "декомпозиц",
        "дублирован",
    ],
    "ER-моделирование": [
        "er-",
        "er ",
        "сущность",
        "сущност",
        "кардинальн",
        "диаграмм",
        "связь между",
    ],
    "Транзакции": [
        "транзакц",
        "commit",
        "rollback",
        "блокировк",
        "изоляц",
        "acid",
        "deadlock",
    ],
    "Индексы": ["индекс", "b-tree", "btree", "seq scan", "index scan"],
    "Производительность": [
        "производительн",
        "explain",
        "план запроса",
        "оптимизац",
        "медленн",
    ],
    "Проектирование БД": [
        "первичный ключ",
        "внешний ключ",
        "primary key",
        "foreign key",
        "схем",
        "проектирован",
        "атрибут",
        "тип данных",
        "constraint",
        "целостност",
    ],
    "PostgreSQL": [
        "psql",
        "postgres",
        "coalesce",
        "serial",
        "sequence",
        "расширени",
    ],
    "SQL": [
        "select",
        "where",
        "join",
        "group by",
        "order by",
        "count",
        "avg(",
        "sum(",
        "distinct",
        "having",
        "limit",
        "запрос",
        "выборк",
        "оконн",
        "over(",
        "insert",
        "update",
        "delete",
    ],
}


class Command(BaseCommand):
    help = "Первичная разметка вопросов темами для карты освоения."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="только показать результат")
        parser.add_argument(
            "--force", action="store_true", help="перезаписывать уже проставленные темы"
        )

    def handle(self, *args, **options):
        topics = {t.name: t for t in Topic.objects.all()}
        missing = [name for name in KEYWORDS if name not in topics]
        if missing:
            self.stdout.write(self.style.WARNING(f"Нет таких тем в базе: {', '.join(missing)}"))

        primary_by_course = {}
        for ct in CourseTopic.objects.select_related("topic").order_by("course_id"):
            primary_by_course.setdefault(ct.course_id, ct.topic)

        qs = Question.objects.select_related("test__lesson__module__course")
        if not options["force"]:
            qs = qs.filter(topic__isnull=True)

        by_keyword, by_course, untouched = 0, 0, 0
        stats = {}
        updates = []

        for q in qs:
            haystack = (q.text or "").lower()
            lesson = q.test.lesson if q.test_id else None
            if lesson:
                haystack += " " + (lesson.title or "").lower()

            best_name, best_hits = None, 0
            for name, words in KEYWORDS.items():
                if name not in topics:
                    continue
                hits = sum(1 for w in words if w in haystack)
                if hits > best_hits:
                    best_name, best_hits = name, hits

            if best_name:
                topic = topics[best_name]
                by_keyword += 1
            else:
                course = lesson.module.course if lesson and lesson.module_id else None
                topic = primary_by_course.get(course.id) if course else None
                if topic is None:
                    untouched += 1
                    continue
                by_course += 1

            stats[topic.name] = stats.get(topic.name, 0) + 1
            q.topic = topic
            updates.append(q)

        self.stdout.write(f"\nПо ключевым словам: {by_keyword}")
        self.stdout.write(f"По основной теме курса: {by_course}")
        self.stdout.write(f"Не удалось определить: {untouched}")
        self.stdout.write("\nРаспределение:")
        for name, n in sorted(stats.items(), key=lambda kv: -kv[1]):
            self.stdout.write(f"  {name:24} {n}")

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING("\nПробный запуск — ничего не сохранено."))
            return

        with transaction.atomic():
            Question.objects.bulk_update(updates, ["topic"], batch_size=200)
        self.stdout.write(self.style.SUCCESS(f"\nПроставлено тем: {len(updates)}."))
