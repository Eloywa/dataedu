"""Предрасчёт эталонного результата SQL-задания.

Вынесено из management-команды, потому что тем же кодом пользуется кнопка «Посчитать
эталон» в админке: у преподавателя не должно быть повода лезть в терминал, а расчёт в
двух местах разошёлся бы.

**Модель доверия.** Здесь исполняется только SQL **преподавателя** (`setup_sql` +
`expected_sql`) — доверенный. Студенческий SQL сервер не исполняет никогда: он работает
в браузере на PGlite, а сервер лишь сравнивает присланные строки с посчитанным здесь
эталоном (см. §17.10 архитектурного документа).

Исполнение изолировано: одноразовая схема `tmp_chk`, отдельное соединение psycopg вне
пула Django, и в конце — безусловный `rollback()`, после которого исчезают и схема, и
`search_path`. Соединение не в autocommit, поэтому откат надёжен.
"""

import psycopg
from django.conf import settings

from .grading import jsonable


def _conn_params():
    db = settings.DATABASES["default"]
    # Серверный расчёт исполняет SQL в PostgreSQL. Если Django работает на другой
    # базе (в профиле разработки это SQLite), подключаться некуда — и падать
    # ошибкой сокета неправильно: человек решит, что не запущен сервер БД, хотя
    # его тут и не должно быть.
    if "postgresql" not in db.get("ENGINE", ""):
        raise ExpectedError(
            "Серверный расчёт работает только на PostgreSQL, а Django сейчас "
            "подключён к другой базе. Посчитайте эталон кнопкой в браузере — она "
            "выполняет запрос в том же движке, что и студент, и от базы Django "
            "не зависит."
        )
    return dict(
        host=db["HOST"],
        port=db["PORT"],
        user=db["USER"],
        password=db["PASSWORD"],
        dbname=db["NAME"],
    )


def _statements(sql):
    return [s.strip() for s in (sql or "").split(";") if s.strip()]


class ExpectedError(Exception):
    """Не удалось посчитать эталон: не хватает данных или SQL преподавателя с ошибкой."""


def compute_expected(assignment, conn=None):
    """Посчитать и вернуть `{"columns": [...], "rows": [[...]]}` — без сохранения.

    `conn` можно передать, чтобы переиспользовать соединение при пакетном расчёте.
    Ошибки поднимаются как `ExpectedError` с текстом от PostgreSQL — преподавателю
    нужно видеть, что именно в его запросе не так.
    """
    if not (assignment.setup_sql or "").strip():
        raise ExpectedError("Не заполнена заготовка данных (setup_sql).")
    if not (assignment.expected_sql or "").strip():
        raise ExpectedError("Не заполнен эталонный запрос (expected_sql).")

    own_conn = conn is None
    conn = conn or psycopg.connect(**_conn_params())
    try:
        cur = conn.cursor()
        try:
            cur.execute("DROP SCHEMA IF EXISTS tmp_chk CASCADE; CREATE SCHEMA tmp_chk;")
            cur.execute("SET search_path TO tmp_chk, public;")
            for stmt in _statements(assignment.setup_sql):
                cur.execute(stmt)
            cur.execute(assignment.expected_sql)
            if cur.description is None:
                raise ExpectedError(
                    "Эталонный запрос не вернул таблицу — для задания с автопроверкой нужен SELECT."
                )
            cols = [d.name for d in cur.description]
            rows = [list(r) for r in cur.fetchall()]
            return {"columns": cols, "rows": jsonable(rows)}
        except psycopg.Error as e:
            raise ExpectedError(str(e).strip()) from e
        finally:
            conn.rollback()  # схема tmp_chk и search_path исчезают
    finally:
        if own_conn:
            conn.close()


def compute_and_save(assignment, conn=None):
    """Посчитать эталон и записать в `assignment.expected_result`."""
    result = compute_expected(assignment, conn=conn)
    assignment.expected_result = result
    assignment.save(update_fields=["expected_result"])
    return result
