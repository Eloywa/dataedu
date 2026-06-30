"""Сравнение результатов SQL: без учёта порядка строк (порядок столбцов — по позиции).
Значения приводятся к строке, поэтому разница типов (int/Decimal/строка из PGlite)
не мешает сравнению.
"""


def _norm(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def normalize_rows(rows):
    return sorted(tuple(_norm(v) for v in row) for row in rows)


def rows_equal(cols_a, rows_a, cols_b, rows_b):
    if len(cols_a or []) != len(cols_b or []):
        return False
    return normalize_rows(rows_a or []) == normalize_rows(rows_b or [])


def jsonable(rows):
    """Привести значения строк к JSON-совместимым (Decimal/датавремя → строка)."""
    out = []
    for row in rows:
        out.append([v if v is None or isinstance(v, (int, float, str, bool)) else str(v) for v in row])
    return out
