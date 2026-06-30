"""Генерируемая обложка курса: тёмный градиент по slug + тематическая иконка
(порт из Next-версии CourseCover, палитра гармонизирована под тёмную тему Terminal).
"""

import hashlib

GRADIENTS = [
    ("#1b2610", "#39491f"),
    ("#10231c", "#1f4034"),
    ("#221a10", "#3e2f16"),
    ("#161a17", "#2b332c"),
    ("#0f1e24", "#1c3a44"),
    ("#241019", "#43202f"),
    ("#10201f", "#1e3c3a"),
    ("#241313", "#43221f"),
]

ICONS = {
    "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "table": '<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="M3 9h18M3 14.5h18M9 4v16M15 4v16"/>',
    "key": '<circle cx="8" cy="8" r="3.5"/><path d="M10.5 10.5L19 19M14 18l2-2M16 16l2.5-2.5"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    "window": '<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="M3 9h18M7 16.5v-3M11 16.5v-5M15 16.5v-2M19 16.5v-4"/>',
}

SLUG_ICON = {
    "sql-s-nulya": "table",
    "databases-for-teachers": "database",
    "postgresql-praktika": "database",
    "proektirovanie-er": "key",
    "normalizaciya": "layers",
    "indeksy-proizvoditelnost": "bolt",
    "okonnye-funkcii": "window",
    "tranzakcii-blokirovki": "lock",
}


def cover_for(slug):
    h = int(hashlib.md5((slug or "").encode()).hexdigest(), 16)
    a, b = GRADIENTS[h % len(GRADIENTS)]
    icon = ICONS[SLUG_ICON.get(slug, "database")]
    return a, b, icon
