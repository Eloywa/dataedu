"""Значки достижений. Устроены так же, как обложки курсов (`courses/cover.py`).

Каждый показывает то, за что выдан, а не общий образ награды. Ключи совпадают со значением
`Achievement.icon` в базе и остались от первой версии платформы, поэтому `fire` рисует
неделю, а `trophy` щит: менять данные ради подписи незачем.
"""

BADGES = {
    # Флажок на первой ступени: первый завершённый урок.
    "flag": (
        '<path class="ci-tint" d="M15 8h21l-5 7.5 5 7.5H15z"/>'
        '<path d="M15 42V6"/>'
        '<path d="M15 8h21l-5 7.5 5 7.5H15"/>'
        '<path d="M8 42h24"/>'
    ),
    # Строка приглашения: первый выполненный запрос.
    "code": (
        '<path class="ci-tint" d="M6 18v-5a3 3 0 0 1 3-3h30a3 3 0 0 1 3 3v5z"/>'
        '<rect x="6" y="10" width="36" height="28" rx="3"/>'
        '<path d="M6 18h36"/>'
        '<path d="M13 24l5 4-5 4"/>'
        '<path d="M23 32h11"/>'
    ),
    # Медаль с отметкой: тест на 80 баллов и выше.
    "medal": (
        '<circle class="ci-tint" cx="24" cy="30" r="13"/>'
        '<path d="M15 4l7 14M33 4l-7 14M15 4h18"/>'
        '<circle cx="24" cy="30" r="13"/>'
        '<path d="M18 30.5l4.5 4.5 8-9"/>'
    ),
    # Календарь с семью отмеченными днями: неделя без пропусков.
    "fire": (
        '<path class="ci-tint" d="M6 19v-6a3 3 0 0 1 3-3h30a3 3 0 0 1 3 3v6z"/>'
        '<rect x="6" y="10" width="36" height="32" rx="3"/>'
        '<path d="M6 19h36M15 6v7M33 6v7"/>'
        '<circle class="ci-dot" cx="12" cy="30" r="1.7"/>'
        '<circle class="ci-dot" cx="16" cy="30" r="1.7"/>'
        '<circle class="ci-dot" cx="20" cy="30" r="1.7"/>'
        '<circle class="ci-dot" cx="24" cy="30" r="1.7"/>'
        '<circle class="ci-dot" cx="28" cy="30" r="1.7"/>'
        '<circle class="ci-dot" cx="32" cy="30" r="1.7"/>'
        '<circle class="ci-dot" cx="36" cy="30" r="1.7"/>'
    ),
    # Щит со звездой: защищённый итоговый проект.
    "trophy": (
        '<path class="ci-tint" d="M24 5l16 5.5v12C40 33 33 40 24 44c-9-4-16-11-16-21.5v-12z"/>'
        '<path d="M24 5l16 5.5v12C40 33 33 40 24 44c-9-4-16-11-16-21.5v-12z"/>'
        '<path d="M24 14l3 6.5 7 .8-5.2 4.7 1.4 6.9L24 29.4l-6.2 3.5 1.4-6.9L14 21.3l7-.8z"/>'
    ),
}

# Достижение, заведённое в админке с незнакомым значком.
DEFAULT_BADGE = "medal"


def badge_for(icon):
    return BADGES.get(icon or "", BADGES[DEFAULT_BADGE])
