"""Кураторские учебные материалы по курсам (порт из Next-версии resources.ts).
Без БД — обычный словарь по slug курса с базовым набором по умолчанию.
"""

KIND_LABEL = {
    "doc": "Документация",
    "book": "Учебник",
    "practice": "Практика",
    "course": "Курс",
}

DEFAULT_RESOURCES = [
    {"title": "Документация PostgreSQL (рус.)", "url": "https://postgrespro.ru/docs/postgresql/current", "kind": "doc"},
    {"title": "Е. Моргунов. PostgreSQL. Основы языка SQL", "url": "https://postgrespro.ru/education/books/sqlprimer", "kind": "book"},
    {"title": "PostgreSQL Exercises — задачи на SQL", "url": "https://pgexercises.com/", "kind": "practice"},
]

COURSE_RESOURCES = {
    "sql-s-nulya": [
        {"title": "Postgres: первое знакомство (брошюра)", "url": "https://postgrespro.ru/education/books/introbook", "kind": "book"},
        {"title": "Е. Моргунов. Основы языка SQL", "url": "https://postgrespro.ru/education/books/sqlprimer", "kind": "book"},
        {"title": "PostgreSQL Exercises", "url": "https://pgexercises.com/", "kind": "practice"},
    ],
    "databases-for-teachers": [
        {"title": "Postgres: первое знакомство", "url": "https://postgrespro.ru/education/books/introbook", "kind": "book"},
        {"title": "Документация PostgreSQL (рус.)", "url": "https://postgrespro.ru/docs/postgresql/current", "kind": "doc"},
    ],
    "postgresql-praktika": [
        {"title": "Документация PostgreSQL (рус.)", "url": "https://postgrespro.ru/docs/postgresql/current", "kind": "doc"},
        {"title": "Е. Моргунов. Основы языка SQL", "url": "https://postgrespro.ru/education/books/sqlprimer", "kind": "book"},
        {"title": "PostgreSQL Exercises", "url": "https://pgexercises.com/", "kind": "practice"},
    ],
    "proektirovanie-er": [
        {"title": "Основы технологий баз данных", "url": "https://postgrespro.ru/education/books/dbtech", "kind": "book"},
        {"title": "Документация: ограничения целостности", "url": "https://postgrespro.ru/docs/postgresql/current/ddl-constraints", "kind": "doc"},
    ],
    "normalizaciya": [
        {"title": "Основы технологий баз данных", "url": "https://postgrespro.ru/education/books/dbtech", "kind": "book"},
        {"title": "Документация: ограничения целостности (CHECK, FK, UNIQUE)", "url": "https://postgrespro.ru/docs/postgresql/current/ddl-constraints", "kind": "doc"},
    ],
    "indeksy-proizvoditelnost": [
        {"title": "Документация: индексы", "url": "https://postgrespro.ru/docs/postgresql/current/indexes", "kind": "doc"},
        {"title": "Документация: использование EXPLAIN", "url": "https://postgrespro.ru/docs/postgresql/current/using-explain", "kind": "doc"},
        {"title": "Markus Winand. Use The Index, Luke!", "url": "https://use-the-index-luke.com/", "kind": "book"},
        {"title": "PostgreSQL 17 изнутри (Е. Рогов)", "url": "https://postgrespro.ru/education/books/internals", "kind": "book"},
    ],
    "okonnye-funkcii": [
        {"title": "Документация: оконные функции (учебник)", "url": "https://postgrespro.ru/docs/postgresql/current/tutorial-window", "kind": "doc"},
        {"title": "PostgreSQL. Профессиональный SQL", "url": "https://postgrespro.ru/education/books/advancedsql", "kind": "book"},
    ],
    "tranzakcii-blokirovki": [
        {"title": "Документация: изоляция транзакций", "url": "https://postgrespro.ru/docs/postgresql/current/transaction-iso", "kind": "doc"},
        {"title": "Документация: MVCC", "url": "https://postgrespro.ru/docs/postgresql/current/mvcc", "kind": "doc"},
        {"title": "PostgreSQL 17 изнутри (Е. Рогов)", "url": "https://postgrespro.ru/education/books/internals", "kind": "book"},
    ],
}


def get_course_resources(slug):
    return COURSE_RESOURCES.get(slug, DEFAULT_RESOURCES)
