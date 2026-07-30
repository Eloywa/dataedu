"""Сравнение результатов SQL: без учёта порядка строк (порядок столбцов — по позиции).
Значения приводятся к строке, поэтому разница типов (int/Decimal/строка из PGlite)
не мешает сравнению.
"""

from collections import Counter


def _norm(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def normalize_rows(rows):
    """Нормализованные строки как **мультимножество** (порядок строк не важен).

    Сравнение идёт через `Counter`, а не через `sorted`, и это не стилистика: сортировка
    кортежей падает с `TypeError`, если в одной позиции у разных строк оказываются `None`
    и строка (`'<' not supported between instances of 'str' and 'NoneType'`). Условие
    редкое — первые столбцы должны совпасть, а расхождение прийтись на NULL, — но
    достижимое обычным запросом студента с NULL в выборке, и раньше оно роняло
    точку проверки в 500.
    """
    return Counter(tuple(_norm(v) for v in row) for row in (rows or []))


def rows_equal(cols_a, rows_a, cols_b, rows_b):
    if len(cols_a or []) != len(cols_b or []):
        return False
    return normalize_rows(rows_a) == normalize_rows(rows_b)


def jsonable(rows):
    """Привести значения строк к JSON-совместимым (Decimal/датавремя → строка)."""
    out = []
    for row in rows:
        out.append([v if v is None or isinstance(v, (int, float, str, bool)) else str(v) for v in row])
    return out


# --- Диагностика автопроверки (этап 10.5) ---------------------------------------
#
# «Неверно» без объяснений — плохая обратная связь: студент не понимает, ошибся он в
# условии отбора, забыл DISTINCT или выбрал не те столбцы. Поэтому итог раскладывается
# на три независимые проверки: столбцы, число строк, состав строк.
#
# **Жёсткое ограничение: диагностика не раскрывает эталон.** Сообщаются только формы и
# количества (сколько столбцов ожидалось, на сколько строк расхождение), но никогда —
# содержимое эталонных строк и названия эталонных столбцов. Иначе подсказка превращается
# в выдачу ответа.


def diagnose(student_cols, student_rows, expected_cols, expected_rows):
    """Разложить итог проверки на понятные студенту составляющие.

    Возвращает `{"passed": bool, "checks": [{"label", "ok", "detail"}], "hint": str}`.
    """
    student_cols = student_cols or []
    expected_cols = expected_cols or []
    n_student, n_expected = len(student_rows or []), len(expected_rows or [])

    cols_ok = len(student_cols) == len(expected_cols)
    count_ok = n_student == n_expected

    s_multi, e_multi = normalize_rows(student_rows), normalize_rows(expected_rows)
    content_ok = cols_ok and s_multi == e_multi

    checks = [
        {
            "label": "столбцы",
            "ok": cols_ok,
            "detail": (
                f"{len(student_cols)}"
                if cols_ok
                else f"ожидалось {len(expected_cols)}, в выборке {len(student_cols)}"
            ),
        },
        {
            "label": "число строк",
            "ok": count_ok,
            "detail": f"{n_student}" if count_ok else f"ожидалось {n_expected}, получено {n_student}",
        },
    ]

    # Состав строк имеет смысл сравнивать только при совпавшем числе столбцов:
    # иначе несовпадение уже объяснено предыдущей проверкой.
    if cols_ok:
        missing = sum((e_multi - s_multi).values())
        extra = sum((s_multi - e_multi).values())
        if content_ok:
            detail = "совпадает"
        else:
            parts = []
            if missing:
                parts.append(f"не хватает {missing}")
            if extra:
                parts.append(f"лишних {extra}")
            detail = ", ".join(parts) or "строки отличаются"
        checks.append({"label": "состав строк", "ok": content_ok, "detail": detail})
    else:
        missing = extra = 0

    passed = cols_ok and content_ok
    return {
        "passed": passed,
        "checks": checks,
        "hint": _hint(passed, cols_ok, s_multi, e_multi, missing, extra),
    }


def _hint(passed, cols_ok, s_multi, e_multi, missing, extra):
    """Одна подсказка о вероятной причине — по форме расхождения, без содержимого."""
    if passed:
        return ""
    if not cols_ok:
        return "Проверьте список столбцов после SELECT: их число отличается от ожидаемого."

    # Дубликаты у студента там, где эталон уникален — типичный пропуск DISTINCT/GROUP BY.
    has_dupes = any(n > 1 for n in s_multi.values())
    expected_unique = all(n == 1 for n in e_multi.values())
    if has_dupes and expected_unique:
        return (
            "В выборке есть повторяющиеся строки, а в ожидаемом результате их нет — "
            "возможно, нужен DISTINCT или группировка, либо соединение размножает строки."
        )
    if extra and not missing:
        return (
            "Все нужные строки на месте, но есть лишние — условие отбора слишком широкое: "
            "проверьте WHERE."
        )
    if missing and not extra:
        return (
            "Лишних строк нет, но часть нужных не хватает — условие отбора слишком узкое: "
            "проверьте WHERE и границы сравнений."
        )
    if missing and extra:
        return (
            "Строки не совпадают по содержимому: проверьте вычисляемые значения "
            "и условия соединения таблиц."
        )
    return "Результат отличается от ожидаемого."
