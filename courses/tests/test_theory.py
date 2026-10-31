"""Разметка теории урока: оглавление и врезки.

Всё это ломается тихо. Оглавление собирается из заголовков самой теории, и если
расширение `toc` отключится или сменится slugify, якоря станут вида `_1`:
ссылки в боковой колонке останутся кликабельными, но поедут не туда. Врезка без
подключённого расширения выведется строкой «!!! note» прямо в тексте урока —
и то и другое видно только глазами и только на той странице, куда заглянул.
"""

from django.test import SimpleTestCase

from courses.theory import render_theory

LESSON = """\
## Чем база отличается от документа

Текст первого раздела.

### Подзаголовок

!!! note "Обратите внимание"
    Запрос выполняется в браузере.

## СУБД и PostgreSQL

Текст второго раздела.
"""


class TocTests(SimpleTestCase):
    def test_headings_become_toc_with_anchors(self):
        html, toc = render_theory(LESSON)

        self.assertEqual(
            [(item["level"], item["name"]) for item in toc],
            [
                (2, "Чем база отличается от документа"),
                (3, "Подзаголовок"),
                (2, "СУБД и PostgreSQL"),
            ],
        )
        # Каждый пункт оглавления ведёт на заголовок, который действительно есть
        # в разметке: пара «ссылка — цель» появляется только вместе.
        for item in toc:
            self.assertIn(f'id="{item["id"]}"', html)

    def test_anchors_keep_cyrillic(self):
        """Стандартный slugify выбрасывает кириллицу и даёт якоря `_1`, `_2`."""
        _, toc = render_theory("## Нормализация\n\nтекст\n\n## Индексы\n\nтекст\n")

        ids = [item["id"] for item in toc]
        self.assertEqual(ids, ["нормализация", "индексы"])

    def test_single_heading_gives_no_toc(self):
        """Оглавление из одного пункта — не оглавление, а лишняя колонка."""
        _, toc = render_theory("## Единственный раздел\n\nтекст\n")

        self.assertEqual(toc, [])

    def test_empty_theory_does_not_fail(self):
        html, toc = render_theory(None)

        self.assertEqual(html, "")
        self.assertEqual(toc, [])


class AdmonitionTests(SimpleTestCase):
    def test_note_becomes_block(self):
        html, _ = render_theory(LESSON)

        self.assertIn('class="admonition note"', html)
        self.assertIn('class="admonition-title">Обратите внимание', html)
        self.assertNotIn("!!!", html)

    def test_quote_stays_a_quote(self):
        """Цитата под врезку не занята: `>` остаётся цитатой."""
        html, _ = render_theory("> Данные — это отдельные факты.\n")

        self.assertIn("<blockquote>", html)
        self.assertNotIn("admonition", html)
