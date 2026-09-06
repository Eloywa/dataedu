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

VAR_USE = re.compile(r"var\(\s*(--[\w-]+)")
VAR_DECL = re.compile(r"^\s*(--[\w-]+)\s*:", re.M)


def declared_tokens():
    return set(VAR_DECL.findall(CSS.read_text(encoding="utf-8")))


def files_using_tokens():
    yield CSS
    yield from TEMPLATES.rglob("*.html")


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

        # Цвета — всё, кроме размеров, шрифтов и радиусов: их тема не меняет.
        skip = ("--radius", "--font", "--header")
        light_colours = {
            t for t in VAR_DECL.findall(light.group(1)) if not t.startswith(skip)
        }
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


class StylesheetTests(SimpleTestCase):
    def test_old_stylesheet_is_gone(self):
        self.assertFalse(
            (Path(settings.BASE_DIR) / "static" / "css" / "terminal.css").exists(),
            "старая таблица стилей осталась в проекте",
        )

    def test_templates_reference_only_the_current_stylesheet(self):
        for path in TEMPLATES.rglob("*.html"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("terminal.css", text, f"{path.name} ссылается на старые стили")

    def test_no_external_resources_in_stylesheet(self):
        """Ноль внешних запросов: шрифты и всё прочее лежат в проекте."""
        found = re.findall(r"url\(\s*['\"]?(https?:)?//", CSS.read_text(encoding="utf-8"))
        self.assertEqual(found, [], "в стилях есть внешние ссылки")
