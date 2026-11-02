"""Обложка курса: тематическая иконка на бирюзовом поле.

Иконки нарисованы для этого проекта, поэтому у них нет чужой лицензии и они ничего
не весят. Все на одной сетке 48 × 48 с одной толщиной линии (задаётся в
`_cover.html`), и каждая показывает предмет курса, а не общий образ: B-дерево с
выделенным путём поиска у индексов, разбиение таблицы у нормализации.

Два класса внутри рисунка: `ci-tint` — полупрозрачная заливка главной детали,
`ci-dot` — мелкая сплошная деталь. Цвет приходит от темы через `currentColor`.

Курс, заведённый преподавателем, получает общую иконку базы данных, пока для него
не нарисована своя: обложка не должна зависеть от того, искал ли кто-то картинку.
"""

ICONS = {
    "database": (
        '<ellipse class="ci-tint" cx="24" cy="11" rx="15" ry="5"/>'
        '<ellipse cx="24" cy="11" rx="15" ry="5"/>'
        '<path d="M9 11v26c0 2.8 6.7 5 15 5s15-2.2 15-5V11"/>'
        '<path d="M9 24c0 2.8 6.7 5 15 5s15-2.2 15-5"/>'
    ),
    # База данных под академической шапочкой: курс для будущих педагогов.
    "teaching": (
        '<path class="ci-tint" d="M24 4l16 7-16 7-16-7z"/>'
        '<path d="M24 4l16 7-16 7-16-7z"/>'
        '<path d="M40 11v7"/>'
        '<ellipse cx="24" cy="26" rx="13" ry="4"/>'
        '<path d="M11 26v13c0 2.2 5.8 4 13 4s13-1.8 13-4V26"/>'
        '<path d="M11 32.5c0 2.2 5.8 4 13 4s13-1.8 13-4"/>'
    ),
    # Окно консоли: первые запросы.
    "terminal": (
        '<path class="ci-tint" d="M6 17v-5a3 3 0 0 1 3-3h30a3 3 0 0 1 3 3v5z"/>'
        '<rect x="6" y="9" width="36" height="30" rx="3"/>'
        '<path d="M6 17h36"/>'
        '<circle class="ci-dot" cx="11" cy="13" r="1.1"/>'
        '<circle class="ci-dot" cx="15" cy="13" r="1.1"/>'
        '<path d="M13 23l5.5 4.5L13 32"/>'
        '<path d="M23 32h11"/>'
    ),
    # База данных и шестерня: работа с настоящей СУБД.
    "practice": (
        '<ellipse class="ci-tint" cx="19" cy="10" rx="13" ry="4.5"/>'
        '<ellipse cx="19" cy="10" rx="13" ry="4.5"/>'
        '<path d="M6 10v25c0 2.5 5.8 4.5 13 4.5 1.4 0 2.7-.1 4-.2"/>'
        '<path d="M32 10v11"/>'
        '<path d="M6 22.5c0 2.5 5.8 4.5 13 4.5 1.4 0 2.7-.1 4-.2"/>'
        '<circle class="ci-tint" cx="34.5" cy="33.5" r="6.5"/>'
        '<circle cx="34.5" cy="33.5" r="6.5"/>'
        '<circle cx="34.5" cy="33.5" r="2"/>'
        '<path d="M34.5 24v3M34.5 40v3M25 33.5h3M41 33.5h3'
        'M27.8 26.8l2.1 2.1M39.1 38.1l2.1 2.1M27.8 40.2l2.1-2.1M39.1 28.9l2.1-2.1"/>'
    ),
    # Таблица с рамкой-окном, которая движется по строкам.
    "window": (
        '<rect class="ci-tint" x="6" y="20" width="30" height="14"/>'
        '<rect x="6" y="6" width="30" height="36" rx="3"/>'
        '<path d="M6 13h30M6 20h30M6 27h30M6 34h30M16 6v36"/>'
        '<path d="M42 15v18M38.5 29.5L42 33l3.5-3.5"/>'
    ),
    # Замок и встречные стрелки: параллельные транзакции.
    "lock": (
        '<rect class="ci-tint" x="9" y="21" width="30" height="22" rx="3"/>'
        '<rect x="9" y="21" width="30" height="22" rx="3"/>'
        '<path d="M15 21v-6a9 9 0 0 1 18 0v6"/>'
        '<path d="M17 28h14M28 25l3 3-3 3M31 36H17M20 33l-3 3 3 3"/>'
    ),
    # B-дерево: выделен путь поиска от корня к листу.
    "btree": (
        '<rect class="ci-tint" x="18" y="5" width="12" height="8" rx="1.5"/>'
        '<rect class="ci-tint" x="30" y="21" width="12" height="8" rx="1.5"/>'
        '<rect class="ci-tint" x="26" y="36" width="8" height="7" rx="1.5"/>'
        '<rect x="18" y="5" width="12" height="8" rx="1.5"/>'
        '<rect x="6" y="21" width="12" height="8" rx="1.5"/>'
        '<rect x="30" y="21" width="12" height="8" rx="1.5"/>'
        '<rect x="2" y="36" width="8" height="7" rx="1.5"/>'
        '<rect x="14" y="36" width="8" height="7" rx="1.5"/>'
        '<rect x="26" y="36" width="8" height="7" rx="1.5"/>'
        '<rect x="38" y="36" width="8" height="7" rx="1.5"/>'
        '<path d="M24 13v4H12v4M24 17h12v4M12 29v3.5H6V36M12 32.5h6V36'
        'M36 29v3.5h-6V36M36 32.5h6V36"/>'
    ),
    # ER-диаграмма: три сущности и связи «один ко многим».
    "er": (
        '<path class="ci-tint" d="M5 13V9a2 2 0 0 1 2-2h11a2 2 0 0 1 2 2v4z"/>'
        '<path class="ci-tint" d="M28 13V9a2 2 0 0 1 2-2h11a2 2 0 0 1 2 2v4z"/>'
        '<path class="ci-tint" d="M16 35v-4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v4z"/>'
        '<rect x="5" y="7" width="15" height="14" rx="2"/>'
        '<rect x="28" y="7" width="15" height="14" rx="2"/>'
        '<rect x="16" y="29" width="16" height="14" rx="2"/>'
        '<path d="M5 13h15M28 13h15M16 35h16"/>'
        '<path d="M20 14h8M25 14l3-3M25 14l3 3"/>'
        '<path d="M12.5 21v18H16M13 39l3-3M13 39l3 3"/>'
    ),
    # Одна широкая таблица распадается на две связанные.
    "split": (
        '<rect x="4" y="9" width="17" height="30" rx="2"/>'
        '<path d="M4 16.5h17M4 24h17M4 31.5h17M12.5 9v30"/>'
        '<path d="M24.5 24h6M27.5 21l3 3-3 3"/>'
        '<path class="ci-tint" d="M33 12V9a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v3z"/>'
        '<path class="ci-tint" d="M33 32v-3a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v3z"/>'
        '<rect x="33" y="7" width="12" height="14" rx="2"/>'
        '<rect x="33" y="27" width="12" height="14" rx="2"/>'
        '<path d="M33 12h12M33 32h12M39 21v6"/>'
    ),
}

SLUG_ICON = {
    "databases-for-teachers": "teaching",
    "sql-s-nulya": "terminal",
    "postgresql-praktika": "practice",
    "okonnye-funkcii": "window",
    "tranzakcii-blokirovki": "lock",
    "indeksy-proizvoditelnost": "btree",
    "proektirovanie-er": "er",
    "normalizaciya": "split",
}


def cover_for(slug):
    """Разметка иконки курса. Курс без своей иконки получает общую."""
    return ICONS[SLUG_ICON.get(slug, "database")]
