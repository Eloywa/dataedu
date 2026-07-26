"""Уровни платформы по суммарному XP (порог-схема из Next-версии)."""

LEVEL_THRESHOLDS = [0, 60, 120, 200, 300, 420, 560, 720]


def level_for_xp(xp):
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp >= threshold:
            level = i + 1
    return level


def level_progress(xp):
    level = level_for_xp(xp)
    current = LEVEL_THRESHOLDS[level - 1]
    nxt = LEVEL_THRESHOLDS[level] if level < len(LEVEL_THRESHOLDS) else None

    if nxt is None:
        return {"level": level, "xp": xp, "into": xp - current, "span": 0, "pct": 100, "to_next": 0, "is_max": True}

    span = nxt - current
    into = xp - current
    return {
        "level": level,
        "xp": xp,
        "into": into,
        "span": span,
        "pct": round(into * 100 / span) if span else 0,
        "to_next": nxt - xp,
        "is_max": False,
    }
