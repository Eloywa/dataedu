"""Оформление админки (django-jazzmin).

Стандартная админка Django работоспособна, но выглядит служебной, а здесь она —
рабочее место преподавателя: через неё создаются курсы, уроки, тесты и задания.
Jazzmin даёт боковое меню, поиск по разделам и тёмную тему, не требуя переписывать
ни одного `ModelAdmin` — вся настройка декларативная.

**Важное ограничение: ноль внешних запросов.** Jazzmin по умолчанию подключает
шрифты с `fonts.googleapis.com`; здесь это выключено (`use_google_fonts_cdn`).
Требование не косметическое — платформа разворачивается в контуре без доступа
наружу, и любой внешний запрос там просто виснет (см. ARCHITECTURE.md §5).
"""

JAZZMIN_SETTINGS = {
    "site_title": "DataEdu",
    "site_header": "DataEdu",
    "site_brand": "DataEdu",
    "site_logo": None,
    "welcome_sign": "Администрирование DataEdu",
    "copyright": "DataEdu",
    "search_model": ["courses.Course", "accounts.User"],
    # Ноль внешних запросов: шрифты берутся системные, ничего не тянется с CDN.
    "use_google_fonts_cdn": False,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    # Курс и урок правятся вместе с вложенными элементами, поэтому у них —
    # одна страница со всеми полями, а не вкладки.
    "changeform_format_overrides": {
        "courses.course": "single",
        "courses.lesson": "single",
    },
    "topmenu_links": [
        {"name": "На сайт", "url": "/", "new_window": False},
        {"name": "Панель преподавателя", "url": "/teacher/", "new_window": False},
        {"name": "Проверка работ", "url": "/teacher/submissions/", "new_window": False},
    ],
    "usermenu_links": [
        {"name": "Настройки учётной записи", "url": "/settings/"},
    ],
    # Порядок разделов повторяет путь материала: сначала люди, потом курсы,
    # потом проверка знаний, потом наблюдение за обучением.
    "order_with_respect_to": [
        "accounts",
        "courses",
        "assessments",
        "learning",
        "gamification",
        "messaging",
        "auth",
    ],
    "icons": {
        "accounts": "fas fa-users-cog",
        "accounts.User": "fas fa-user",
        "accounts.Role": "fas fa-user-tag",
        "accounts.Consent": "fas fa-file-signature",
        "auth.Group": "fas fa-user-shield",
        "courses": "fas fa-book",
        "courses.Course": "fas fa-book-open",
        "courses.Module": "fas fa-layer-group",
        "courses.Lesson": "fas fa-file-alt",
        "courses.Topic": "fas fa-tags",
        "courses.CourseRating": "fas fa-star",
        "assessments": "fas fa-clipboard-check",
        "assessments.Test": "fas fa-clipboard-list",
        "assessments.Question": "fas fa-question-circle",
        "assessments.Assignment": "fas fa-code",
        "assessments.Submission": "fas fa-inbox",
        "learning": "fas fa-graduation-cap",
        "learning.StudyGroup": "fas fa-users",
        "learning.Enrollment": "fas fa-user-check",
        "learning.Reflection": "fas fa-comment-dots",
        "gamification": "fas fa-trophy",
        "gamification.Achievement": "fas fa-medal",
        "messaging": "fas fa-comments",
        "messaging.Message": "fas fa-envelope",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    # Связанные объекты открываются отдельным окном, а не модальным.
    # Модальное окно jazzmin грузит страницу админки в тесный iframe без
    # собственных стилей: на тёмной теме получается чёрный прямоугольник с
    # полосами прокрутки, форма внутри есть, но добраться до неё нельзя.
    # Штатное окно Django выглядит как остальная админка и работает всегда.
    "related_modal_active": False,
}

# Тёмная тема под палитру платформы: админка и сайт не должны выглядеть как две
# разные системы. `darkly` — ближайшая из встроенных; акцент задаётся кнопками.
JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    # В jazzmin 3 темы сами умеют светлый и тёмный режим; прежний `dark_mode_theme`
    # объявлен устаревшим и игнорируется.
    "default_theme_mode": "dark",
    "navbar": "navbar-dark",
    "navbar_small_text": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_flat_style": True,
    "sidebar_nav_compact_style": True,
    "brand_colour": "navbar-dark",
    "accent": "accent-olive",
    "button_classes": {
        "primary": "btn-outline-success",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": True,
}
