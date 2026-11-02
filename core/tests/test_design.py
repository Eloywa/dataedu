"""Целостность системы стилей.

Проверяется то, что ломается тихо. Незаданная переменная в CSS не роняет страницу
и не выводит ошибку — элемент просто теряет цвет и сливается с фоном, а заметить
это можно только глазами и только на той странице, куда заглянул. Ровно так
случилось при смене оформления: токен `--secondary` из прежней палитры исчез, а
две страницы отчётов продолжали на него ссылаться.
"""

import re
import sqlite3
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

CSS = Path(settings.BASE_DIR) / "static" / "css" / "app.css"
TEMPLATES = Path(settings.BASE_DIR) / "templates"
SCRIPTS = Path(settings.BASE_DIR) / "static" / "js"

VAR_USE = re.compile(r"var\(\s*(--[\w-]+)")
VAR_DECL = re.compile(r"^\s*(--[\w-]+)\s*:", re.M)
COMMENT = re.compile(r"/\*.*?\*/", re.S)
COLOUR_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}|(?:rgb|rgba|hsl|hsla)\(")


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
    entry = set()
    for path in site_templates():
        text = path.read_text(encoding="utf-8")
        for name in re.findall(r"js/([\w.-]+\.js)", text):
            entry.add(SCRIPTS / name)

    # Модули, подключённые не из разметки, а импортом из другого модуля, тоже
    # рисуют разметку. Обход по импортам добавлен после того, как классы вывода
    # тренажёра переехали в static/js/sql/ и выпали из проверки: список,
    # собранный по одним лишь тегам <script>, снова разошёлся бы с делом.
    seen = set()
    queue = [path for path in entry if path.exists()]
    while queue:
        script = queue.pop()
        if script in seen:
            continue
        seen.add(script)
        text = script.read_text(encoding="utf-8")
        for target in re.findall(r'from\s+"([./][\w./-]+\.js)"', text):
            child = (script.parent / target).resolve()
            if child.exists() and SCRIPTS.resolve() in child.parents:
                queue.append(child)

    yield from sorted(seen)


class TokenTests(SimpleTestCase):
    def test_every_used_token_is_declared(self):
        declared = declared_tokens()
        missing = {}
        for path in files_using_tokens():
            for name in VAR_USE.findall(path.read_text(encoding="utf-8")):
                if name not in declared:
                    missing.setdefault(name, []).append(path.name)
        self.assertEqual(missing, {}, f"не объявлены токены: {missing}")

    def test_no_colour_literals_outside_tokens(self):
        """Цвет задаётся только токеном.

        Редизайн держится на том, что палитру можно поменять в одном месте — хоть
        под цвета вуза. Любой `#fff` или `rgba(...)` в обычном правиле выпадает из
        этой замены: при смене темы он остаётся прежним и даёт белое пятно на
        тёмном фоне или нечитаемую подпись. Так уже случилось со звёздами рейтинга
        (`#e2a33c`) и подписью на кнопке удаления.

        Исключения два: объявления самих токенов (`--name: #hex`) и блок `@media
        print` — там чёрное по белому задаётся намеренно, бумага не знает тем.
        """
        # Комментарии вырезаются, но переводы строк в них сохраняются: иначе
        # номера строк в сообщении об ошибке разойдутся с файлом.
        css = COMMENT.sub(lambda m: "\n" * m.group(0).count("\n"), CSS.read_text(encoding="utf-8"))

        offenders, depth, print_depth = [], 0, None
        for number, line in enumerate(css.splitlines(), 1):
            if print_depth is None and line.strip().startswith("@media print"):
                print_depth = depth
            depth += line.count("{") - line.count("}")
            if print_depth is not None and depth <= print_depth:
                print_depth = None
                continue
            if print_depth is not None or VAR_DECL.match(line):
                continue
            if COLOUR_LITERAL.search(line):
                offenders.append(f"{number}: {line.strip()}")

        self.assertEqual(offenders, [], "цвет задан мимо токена")

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


def _rgb(value):
    """Цвет токена как (r, g, b, a). Понимает `#rrggbb` и `rgba(...)`."""
    value = value.strip()
    if value.startswith("#"):
        return (*(int(value[i : i + 2], 16) for i in (1, 3, 5)), 1.0)
    r, g, b, a = re.findall(r"[\d.]+", value)
    return int(r), int(g), int(b), float(a)


def _over(top, base):
    """Полупрозрачный цвет поверх непрозрачного — так он и виден на экране."""
    alpha = top[3]
    return (
        *(round(t * alpha + b * (1 - alpha)) for t, b in zip(top[:3], base[:3], strict=True)),
        1.0,
    )


def _luminance(colour):
    def channel(value):
        value /= 255
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    r, g, b = colour[:3]
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(first, second):
    bright, dark = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (bright + 0.05) / (dark + 0.05)


def aa_pairs(colour):
    """Пары «текст — фон», которые в теме обязаны читаться."""
    text = ("--text", "--text-strong", "--muted", "--muted-soft", "--accent")
    states = ("--success", "--warning", "--danger")
    backgrounds = ("--bg", "--bg-soft", "--surface", "--surface-2")
    pairs = [(fg, colour[fg], bg, colour[bg]) for fg in text + states for bg in backgrounds]
    for fg, bg in (
        ("--on-accent", "--accent"),
        ("--on-action", "--action"),
        ("--on-action", "--action-hover"),
        ("--on-chrome", "--chrome"),
        ("--on-chrome-soft", "--chrome"),
        ("--mark", "--surface"),
        ("--text", "--field"),
    ):
        pairs.append((fg, colour[fg], bg, colour[bg]))
    # Метка статуса: цветной текст на своей полупрозрачной подложке поверх карточки.
    for state in ("--accent", *states):
        soft = _over(colour[f"{state}-soft"], colour["--surface"])
        pairs.append((state, colour[state], f"{state}-soft", soft))
    return pairs


class PaletteTests(SimpleTestCase):
    """Светлая и тёмная темы: цвета сняты с образца, контраст считается, а не на глаз."""

    def colours(self, pattern):
        block = re.search(pattern, CSS.read_text(encoding="utf-8"), re.S)
        self.assertIsNotNone(block)
        return {
            name: _rgb(value)
            for name, value in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", block.group(1))
            if value.strip().startswith(("#", "rgb"))
        }

    def test_light_theme_reaches_aa_contrast(self):
        for fg_name, fg, bg_name, bg in aa_pairs(self.colours(r":root\s*\{(.+?)\n\}")):
            with self.subTest(fg=fg_name, bg=bg_name):
                self.assertGreaterEqual(contrast(fg, bg), 4.5)

    def test_dark_theme_reaches_aa_contrast(self):
        colours = self.colours(r'\[data-theme="dark"\]\s*\{(.+?)\n\}')
        for fg_name, fg, bg_name, bg in aa_pairs(colours):
            with self.subTest(fg=fg_name, bg=bg_name):
                self.assertGreaterEqual(contrast(fg, bg), 4.5)

    def test_main_action_has_its_own_colour(self):
        """Основная кнопка красится отдельным токеном, а не цветом ссылок и фокуса."""
        css = CSS.read_text(encoding="utf-8")
        rule = re.search(r"\.btn-primary,\s*\.btn-accent\s*\{(.+?)\}", css, re.S)
        self.assertIsNotNone(rule)
        self.assertIn("var(--action)", rule.group(1))


class FontTests(SimpleTestCase):
    FONTS = Path(settings.BASE_DIR) / "static" / "vendor" / "fonts"

    def test_interface_font_is_the_bundled_one(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertIn('--font-sans: "Montserrat"', css)
        self.assertIn('--font-display: "Montserrat"', css)

    def test_every_montserrat_file_is_in_the_project(self):
        """Платформа не делает внешних запросов: без файла браузер молча возьмёт другой шрифт."""
        faces = (self.FONTS / "fonts.css").read_text(encoding="utf-8")
        files = re.findall(r"url\((montserrat-[\w-]+\.woff2)\)", faces)
        self.assertEqual(len(files), 16)
        for name in files:
            with self.subTest(file=name):
                self.assertTrue((self.FONTS / name).exists())
        self.assertTrue((self.FONTS / "montserrat-OFL.txt").exists())


class HomeSampleQueryTests(SimpleTestCase):
    """Таблицы и запрос на главной вписаны в шаблон и не должны разойтись с набором."""

    def setUp(self):
        scripts = SCRIPTS / "sql" / "datasets.js"
        sql = re.search(r"university:.*?sql: `(.*?)`", scripts.read_text(encoding="utf-8"), re.S)
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.executescript(sql.group(1))
        self.page = (TEMPLATES / "core" / "home.html").read_text(encoding="utf-8")

    def test_result_is_what_the_query_returns(self):
        query = re.search(r'<pre class="query-card-sql">(.*?)</pre>', self.page, re.S).group(1)
        rows = self.db.execute(query).fetchall()
        self.assertTrue(rows)
        for name, value in rows:
            with self.subTest(group=name):
                self.assertIn(f'<td>{name}</td><td class="is-number">{value:.2f}</td>', self.page)

    def test_table_cards_list_the_real_columns(self):
        for table in ("groups", "students", "marks"):
            card = re.search(
                rf'<h3 class="table-card-name">{table}</h3>(.*?)</ul>', self.page, re.S
            ).group(1)
            shown = re.findall(r"<li><span>(\w+)</span>", card)
            real = [row[1] for row in self.db.execute(f"pragma table_info({table})")]
            with self.subTest(table=table):
                self.assertEqual(shown, real)


class WarmThemeTests(SimpleTestCase):
    """Ламповая тема: третий набор цветов рядом со светлой и тёмной."""

    def tokens(self):
        css = CSS.read_text(encoding="utf-8")
        block = re.search(r'\[data-theme="warm"\]\s*\{(.+?)\n\}', css, re.S)
        self.assertIsNotNone(block, "не найден блок ламповой темы")
        return block.group(1), dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", block.group(1)))

    def test_redefines_every_colour(self):
        """Пропущенный токен дал бы светлое пятно на тёплом фоне."""
        css = CSS.read_text(encoding="utf-8")
        light = re.search(r":root\s*\{(.+?)\n\}", css, re.S)
        skip = ("--radius", "--font", "--header", "--chevron")
        expected = {t for t in VAR_DECL.findall(light.group(1)) if not t.startswith(skip)}
        block, _ = self.tokens()
        self.assertEqual(expected - set(VAR_DECL.findall(block)), set())

    def test_text_reaches_aa_contrast(self):
        """Средняя яркость — самый трудный случай для контраста, поэтому он считается.

        Тема намеренно светлее тёмной, и запас, который есть на почти чёрном фоне, здесь
        быстро кончается: приглушённая подпись на карточке теряет читаемость первой.
        """
        _, tokens = self.tokens()
        colour = {name: _rgb(value) for name, value in tokens.items() if "shadow" not in name}

        for fg_name, fg, bg_name, bg in aa_pairs(colour):
            with self.subTest(fg=fg_name, bg=bg_name):
                self.assertGreaterEqual(contrast(fg, bg), 4.5)

    def test_saved_choice_is_restored_before_first_paint(self):
        """Иначе выбор не переживал бы перезагрузку: скрипт в <head> знает темы поимённо."""
        base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
        self.assertIn('saved === "warm"', base)

    def test_every_theme_can_be_chosen_from_the_menu(self):
        base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
        for theme in ("light", "warm", "dark", "system"):
            with self.subTest(theme=theme):
                self.assertIn(f'data-theme-choice="{theme}"', base)

    def test_menu_is_closed_and_tied_to_its_button(self):
        """Открывает список скрипт: без него кнопке нечем управлять, а список не должен
        висеть открытым поверх страницы."""
        base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
        self.assertIn('aria-controls="theme-list"', base)
        self.assertRegex(base, r'id="theme-list"[^>]*\bhidden\b')

    def test_system_choice_forgets_the_saved_theme(self):
        """Иначе после перезагрузки вернулась бы тема, от которой только что отказались."""
        script = (SCRIPTS / "theme.js").read_text(encoding="utf-8")
        self.assertIn("localStorage.removeItem(KEY)", script)
        self.assertIn('removeAttribute("data-theme")', script)

    def test_button_has_an_icon_for_the_theme(self):
        base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
        self.assertRegex(base, r'class="icon-warm\b')

    def test_printing_stays_light(self):
        """Ведомость и сертификат — документы: тёплый фон на бумаге только расход тонера."""
        css = CSS.read_text(encoding="utf-8")
        printing = css[css.index("@media print") :]
        self.assertIn('[data-theme="warm"]', printing[: printing.index("--bg:")])


class EditorWiringTests(SimpleTestCase):
    """Поле `.trainer-input` без обвязки редактором нечитаемо.

    Его собственный текст прозрачный, а виден слой подсветки, который создаёт
    `setupEditor`. Страницу задания перевели на этот стиль, не подключив скрипт, и
    студент перестал видеть свой запрос. Сервер отдаёт такую страницу с кодом 200, и ни
    один тест страниц этого не заметит.
    """

    def test_every_page_with_the_field_sets_up_the_editor(self):
        checked = 0
        for path in site_templates():
            text = path.read_text(encoding="utf-8")
            if "trainer-input" not in text:
                continue
            checked += 1
            scripts = re.findall(r"js/([\w.-]+\.js)", text)
            self.assertTrue(
                any(
                    "setupEditor(" in (SCRIPTS / name).read_text(encoding="utf-8")
                    for name in scripts
                ),
                f"{path.name}: поле есть, а setupEditor не вызывается",
            )
        self.assertGreaterEqual(checked, 2, "проверка не нашла страниц с редактором")

    def test_the_gutter_is_not_under_the_text(self):
        """Иначе длинный запрос при прокрутке вбок наезжает на номера строк."""
        css = CSS.read_text(encoding="utf-8")
        layer = re.search(r"\.editor-layer \{(.+?)\n\}", css, re.S).group(1)
        self.assertIn("left: var(--editor-gutter)", layer)


class TrainerStageTests(SimpleTestCase):
    """Вкладки вывода тренажёра: разметка и скрипт обязаны совпадать по именам."""

    def test_every_stage_has_a_tab_and_a_panel(self):
        html = (TEMPLATES / "core" / "trainer.html").read_text(encoding="utf-8")
        script = (SCRIPTS / "trainer.js").read_text(encoding="utf-8")
        stages = re.search(r"STAGES = \[(.+?)\]", script).group(1)
        for name in re.findall(r'"(\w+)"', stages):
            with self.subTest(stage=name):
                self.assertIn(f'id="stage-tab-{name}"', html)
                self.assertIn(f'id="stage-{name}"', html)

    def test_output_is_outside_the_panes(self):
        """На узком экране панель запроса скрывается вкладкой — вывод не должен пропасть с ней."""
        html = (TEMPLATES / "core" / "trainer.html").read_text(encoding="utf-8")
        self.assertGreater(html.index('id="stage"'), html.index('id="pane-sql"'))
        self.assertLess(
            html.index('id="pane-sql"'), html.index("</section>", html.index('id="pane-sql"'))
        )
        self.assertGreater(
            html.index('id="output"'), html.index("</section>", html.index('id="pane-sql"'))
        )


class AchievementTileTests(SimpleTestCase):
    def test_words_are_not_broken_letter_by_letter(self):
        """`overflow-wrap: anywhere` в узкой колонке рвёт слова посимвольно."""
        css = CSS.read_text(encoding="utf-8")
        for selector in (".ach-title", ".ach-desc"):
            block = re.search(re.escape(selector) + r" \{(.+?)\n\}", css, re.S).group(1)
            self.assertNotIn("anywhere", block, selector)

    def test_text_is_one_column_next_to_the_icon(self):
        html = (TEMPLATES / "gamification" / "profile.html").read_text(encoding="utf-8")
        self.assertIn('class="ach-body"', html)


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


class HiddenAttributeTests(SimpleTestCase):
    """`hidden` в разметке должен действительно прятать элемент.

    Правило браузера `[hidden] { display: none }` лежит в его собственной
    таблице стилей, и любое авторское правило с `display` перебивает его
    независимо от специфичности. Значок непрочитанных сообщений из-за этого
    висел в шапке с нулём: разметка ставила ему `hidden`, а `display:
    inline-block` из `app.css` возвращал его на экран.
    """

    def test_stylesheet_enforces_hidden(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertRegex(
            css,
            r"\[hidden\][^{]*\{[^}]*display:\s*none\s*!important",
            "в app.css нет правила, которое делает атрибут hidden сильнее display",
        )


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
