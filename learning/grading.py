"""Разбор формы проверки работы — без БД и без HTTP.

Отделено от представления, потому что проверять здесь есть что: балл приходит из
формы, то есть от недоверенной стороны, и «положить в базу что прислали» нельзя.
Функция возвращает разобранные значения или текст ошибки — ровно одно из двух.
"""

# Что преподаватель делает с работой. «Вернуть» — не оценка, а требование
# доработать: балл при этом всё равно фиксируется, иначе непонятно, за что вернули.
STATUSES = ("graded", "returned")


def clean_grade(raw_score, raw_feedback, raw_status, max_score):
    """Разобрать форму проверки. Возвращает `(данные, ошибка)` — одно из двух None.

    Балл округляется до целого: дробные баллы в ведомости не используются, а
    «84.7 из 100» преподаватель всё равно поставить не хотел.
    """
    status = (raw_status or "").strip()
    if status not in STATUSES:
        return None, "Неизвестное действие"

    try:
        score = round(float(str(raw_score).replace(",", ".")))
    except (TypeError, ValueError):
        return None, "Балл должен быть числом"

    if score < 0 or score > max_score:
        return None, f"Балл должен быть от 0 до {max_score}"

    feedback = (raw_feedback or "").strip() or None
    return {"score": score, "feedback": feedback, "status": status}, None
