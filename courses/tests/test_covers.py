"""Обложки курсов: у каждого курса из набора своя иконка, у нового — общая."""

import re
from xml.etree import ElementTree

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from core.tests import factories as f
from courses.cover import ICONS, SLUG_ICON, cover_for


class CoverIconTests(SimpleTestCase):
    def test_courses_do_not_share_an_icon(self):
        """Иконка показывает предмет курса: одинаковые не отличить в каталоге."""
        self.assertEqual(len(set(SLUG_ICON.values())), len(SLUG_ICON))

    def test_every_course_points_to_a_drawn_icon(self):
        self.assertEqual(set(SLUG_ICON.values()) - set(ICONS), set())

    def test_unknown_course_gets_the_common_icon(self):
        """Преподаватель заводит курс без своей иконки — каталог не должен зиять дырой."""
        self.assertEqual(cover_for("kurs-prepodavatelya"), ICONS["database"])

    def test_every_icon_is_valid_svg(self):
        """Незакрытый тег не даёт ошибки: страница просто теряет часть разметки."""
        for name, icon in ICONS.items():
            with self.subTest(icon=name):
                ElementTree.fromstring(f"<svg>{icon}</svg>")

    def test_colour_comes_from_the_theme(self):
        """Цвет в рисунке не задаётся: иначе иконка не перекрасится вместе с темой."""
        for name, icon in ICONS.items():
            with self.subTest(icon=name):
                self.assertIsNone(re.search(r"#[0-9a-fA-F]{3,8}|fill=|stroke=", icon))


class CatalogRenderTests(TestCase):
    def test_catalog_shows_the_course_icon(self):
        f.course(slug="normalizaciya", title="Нормализация баз данных")
        html = self.client.get(reverse("courses:catalog")).content.decode("utf-8")
        self.assertIn(ICONS["split"], html)

    def test_catalog_loads_no_cover_pictures(self):
        f.course(slug="normalizaciya", title="Нормализация баз данных")
        html = self.client.get(reverse("courses:catalog")).content.decode("utf-8")
        self.assertNotIn("img/covers/", html)
        self.assertNotIn("linear-gradient", html)
