"""Целостность системы стилей.

Проверяется то, что ломается тихо. Незаданная переменная в CSS не роняет страницу
и не выводит ошибку — элемент просто теряет цвет и сливается с фоном, а заметить
это можно только глазами и только на той странице, куда заглянул. Ровно так
случилось при смене оформления: токен `--secondary` из прежней палитры исчез, а
две страницы отчётов продолжали на него ссылаться.
"""

import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

CSS = Path(settings.BASE_DIR) / "static" / "css" / "app.css"
TEMPLATES = Path(settings.BASE_DIR) / "templates"
SCRIPTS = Path(settings.BASE_DIR) / "static" / "js"

VAR_USE = re.compile(r"var\(\s*(--[\w-]+)")
VAR_DECL = re.compile(r"^\s*(--[\w-]+)\s*:", re.M)


def declared_tokens():
    return set(VAR_DECL.findall(CSS.read_text(encoding="utf-8")))


def site_templates():
    """Шаблоны самой платформы — без админки.

    Админка оформлена Django и Jazzmin: у неё своя система стилей и свои
    переменные (`--darkened-bg`, `--hairline-color`). Требовать, чтобы они были
    объявлены в нашей таблице, — значит проверять чужой дизайн.
    """
    for path in TEMPLATES.rglob("*.html"):
        if "admin" not in path.parts:
            yield path


def files_using_tokens():
    yield CSS
    yield from site_templates()


def site_scripts():
    """Скрипты, подключённые со страниц платформы.

    Скрипт, который используется только в админке, оформляется её средствами, и
    искать его классы в `app.css` бессмысленно. Список собирается из разметки, а
    не ведётся руками: иначе он разойдётся с действительностью при первом же
    новом файле.
    """
    referenced = set()
    for path in site_templates():
        text = path.read_text(encoding="utf-8")
        for name in re.findall(r"js/([\w.-]+\.js)", text):
            referenced.add(name)
    for script in SCRIPTS.glob("*.js"):
        if script.name in referenced:
            yield script


class TokenTests(SimpleTestCase):
    def test_every_used_token_is_declared(self):
        declared = declared_tokens()
        missing = {}
        for path in files_using_tokens():
            for name in VAR_USE.findall(path.read_text(encoding="utf-8")):
                if name not in declared:
                    missing.setdefault(name, []).append(path.name)
        self.assertEqual(missing, {}, f"не объявлены токены: {missing}")

    def test_dark_theme_redefines_every_colour(self):
        """Тёмная тема обязана переопределить все цвета, а не часть.

        Пропущенный токен даёт светлое пятно на тёмном фоне — например, белую
        карточку среди тёмных, — и находится это только просмотром всех страниц
        в обеих темах.
        """
        css = CSS.read_text(encoding="utf-8")
        light = re.search(r":root\s*\{(.+?)\n\}", css, re.S)
        dark = re.search(r'\[data-theme="dark"\]\s*\{(.+?)\n\}', css, re.S)
        self.assertIsNotNone(light, "не найден блок :root")
        self.assertIsNotNone(dark, "не найден блок тёмной темы")

        # От темы зависит только цвет. Размеры, шрифты, радиусы и векторные формы
        # одинаковы в обеих и переопределять их не нужно — список ведётся здесь,
        # чтобы новый нецветовой токен пришлось внести осознанно.
        skip = ("--radius", "--font", "--header", "--chevron")
        light_colours = {t for t in VAR_DECL.findall(light.group(1)) if not t.startswith(skip)}
        dark_colours = set(VAR_DECL.findall(dark.group(1)))
        self.assertEqual(
            light_colours - dark_colours, set(), "в тёмной теме не переопределены токены"
        )

    def test_system_dark_matches_explicit_dark(self):
        """Системная тёмная тема и выбранная руками обязаны совпадать.

        Это два разных блока правил (`prefers-color-scheme` и `[data-theme]`), и
        разойтись они могут незаметно: человек, выбравший тёмную тему кнопкой,
        увидит не то, что человек с тёмной темой в системе.
        """
        css = CSS.read_text(encoding="utf-8")
        explicit = re.search(r'\[data-theme="dark"\]\s*\{(.+?)\n\}', css, re.S)
        system = re.search(r":root:not\(\[data-theme\]\)\s*\{(.+?)\n  \}", css, re.S)
        self.assertIsNotNone(system, "не найден блок системной тёмной темы")

        def pairs(block):
            return dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", block))

        self.assertEqual(
            pairs(explicit.group(1)),
            pairs(system.group(1)),
            "значения тёмной темы разошлись между выбором кнопкой и системной настройкой",
        )


class RuntimeClassTests(SimpleTestCase):
    """Классы, которые скрипты создают во время работы, тоже должны быть в стилях.

    Их не видно при просмотре шаблонов: разметку результата запроса, ошибки и
    вердикта автопроверки собирает JavaScript. Именно поэтому при переписывании
    таблицы стилей одиннадцать классов тренажёра остались без правил — вывод
    рисовался голой таблицей, и заметить это можно было только выполнив запрос.
    """

    CLASS_ATTR = re.compile(r'class="([a-z][a-z0-9 _-]*)"')

    def test_classes_from_scripts_are_styled(self):
        css = CSS.read_text(encoding="utf-8")
        missing = {}
        for script in site_scripts():
            text = script.read_text(encoding="utf-8")
            for group in self.CLASS_ATTR.findall(text):
                for name in group.split():
                    if f".{name}" not in css:
                        missing.setdefault(name, []).append(script.name)
        self.assertEqual(missing, {}, f"классы без стилей: {missing}")


class StylesheetTests(SimpleTestCase):
    def test_old_stylesheet_is_gone(self):
        self.assertFalse(
            (Path(settings.BASE_DIR) / "static" / "css" / "terminal.css").exists(),
            "старая таблица стилей осталась в проекте",
        )

    def test_templates_reference_only_the_current_stylesheet(self):
        for path in site_templates():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("terminal.css", text, f"{path.name} ссылается на старые стили")

    def test_no_external_resources_in_stylesheet(self):
        """Ноль внешних запросов: шрифты и всё прочее лежат в проекте."""
        found = re.findall(r"url\(\s*['\"]?(https?:)?//", CSS.read_text(encoding="utf-8"))
        self.assertEqual(found, [], "в стилях есть внешние ссылки")
