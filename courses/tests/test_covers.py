"""Обложки курсов: снимок там, где он объявлен, рисованная плашка везде ещё.

Список курсов со снимками ведётся руками (`courses.cover.PHOTOS`), и разойтись
с содержимым папки он может в обе стороны: объявленный, но не положенный файл
даёт битую картинку в каталоге, а положенный, но не объявленный — мёртвый вес в
репозитории. Проверяется и то и другое.
"""

from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from core.tests import factories as f
from courses.cover import PHOTOS, cover_for, photo_for

COVERS = Path(settings.BASE_DIR) / "static" / "img" / "covers"


class CoverFilesTests(SimpleTestCase):
    def test_every_declared_photo_exists(self):
        missing = sorted(slug for slug in PHOTOS if not (COVERS / f"{slug}.jpg").exists())
        self.assertEqual(missing, [], f"объявлены, но файлов нет: {missing}")

    def test_every_file_is_declared(self):
        extra = sorted(p.stem for p in COVERS.glob("*.jpg") if p.stem not in PHOTOS)
        self.assertEqual(extra, [], f"файлы есть, но в PHOTOS не объявлены: {extra}")

    def test_provenance_is_recorded(self):
        """Снимки чужие. Для дипломной работы происхождение и лицензия каждого
        должны быть записаны, иначе их нельзя ни защитить, ни заменить."""
        readme = COVERS / "README.md"
        self.assertTrue(readme.exists(), "нет README с происхождением снимков")
        text = readme.read_text(encoding="utf-8")
        self.assertIn("unsplash.com/license", text, "не указана лицензия")
        for slug in PHOTOS:
            with self.subTest(slug=slug):
                self.assertIn(f"{slug}.jpg", text, "снимок не описан в README")


class CoverChoiceTests(SimpleTestCase):
    def test_known_course_gets_a_photo(self):
        self.assertEqual(photo_for("normalizaciya"), "img/covers/normalizaciya.jpg")

    def test_unknown_course_falls_back_to_drawing(self):
        """Преподаватель заводит курс без картинки — каталог не должен зиять дырой."""
        self.assertIsNone(photo_for("kurs-prepodavatelya"))
        a, b, icon = cover_for("kurs-prepodavatelya")
        self.assertTrue(a.startswith("#") and b.startswith("#"))
        self.assertTrue(icon)

    def test_drawing_is_stable_for_a_slug(self):
        """Обложка не должна «прыгать» между открытиями страницы."""
        self.assertEqual(cover_for("kurs-prepodavatelya"), cover_for("kurs-prepodavatelya"))


class CatalogRenderTests(TestCase):
    def test_catalog_shows_the_photo(self):
        f.course(slug="normalizaciya", title="Нормализация баз данных")
        html = self.client.get(reverse("courses:catalog")).content.decode("utf-8")
        self.assertIn("img/covers/normalizaciya.jpg", html)
        self.assertIn("cover-photo", html)

    def test_catalog_falls_back_to_gradient(self):
        f.course(slug="kurs-prepodavatelya", title="Курс преподавателя")
        html = self.client.get(reverse("courses:catalog")).content.decode("utf-8")
        self.assertIn("linear-gradient", html)
