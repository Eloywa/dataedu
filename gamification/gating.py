"""Последовательное открытие модулей/недель.

Модуль открыт, если все предыдущие пройдены полностью. Первый — всегда.
Преподаватель (bypass) видит всё.
"""


def compute_gating(modules_progress, bypass=False):
    """modules_progress — список (total, completed) в порядке модулей.
    Возвращает список dict {is_complete, unlocked}.
    """
    result = []
    prev_complete = True
    for total, completed in modules_progress:
        is_complete = total > 0 and completed == total
        result.append({"is_complete": is_complete, "unlocked": bypass or prev_complete})
        prev_complete = prev_complete and is_complete
    return result
