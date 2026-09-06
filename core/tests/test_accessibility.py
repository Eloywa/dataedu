"""Разметка страниц: ориентиры, подписи полей, уровни заголовков.

Проверяется не «красиво ли», а то, что ломается незаметно и обнаруживается только
скринридером: две главные области вместо одной, поле без подписи, пропущенная
ступень заголовков. Всё это правится за минуту, когда найдено, и живёт годами,
когда не найдено.

Проверки идут по **всем** основным страницам разом: почти каждое такое нарушение
приезжает из общего шаблона, и точечный тест на одну страницу его пропустит.
"""

import re

from django.test import TestCase
from django.urls import reverse

from core.tests import factories as f

# Пары «имя маршрута → кто открывает». Список специально широкий: смысл проверки
# в охвате, а не в глубине.
STUDENT_PAGES = [
    "core:home",
    "courses:catalog",
    "core:trainer",
    "assessments:practice",
    "gamification:profile",
    "messaging:inbox",
    "accounts:settings",
    "core:privacy",
    "core:terms",
]
TEACHER_PAGES = [
    "core:home",
    "teaching:dashboard",
    "teaching:analytics",
    "teaching:report",
    "teaching:submissions",
    "messaging:inbox",
]
GUEST_PAGES = [
    "core:home",
    "courses:catalog",
    "core:trainer",
    "accounts:login",
    "accounts:register",
    "core:privacy",
]


class MarkupBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = f.teacher()
        cls.course, cls.lessons = f.course_with_lessons(author=cls.teacher, lessons=2)
        cls.student = f.student()
        f.enroll(cls.student, cls.course)
        f.assignment(cls.course, auto=True)

    def pages(self, names, user=None):
        """Список пар «маршрут, разметка». Именно список, а не генератор: при
        падении внутри subTest генератор закрывается досрочно, и в отчёте вместо
        настоящей ошибки появляется GeneratorExit."""
        if user is not None:
            self.client.force_login(user)
        else:
            self.client.logout()
        result = []
        for name in names:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, f"{name}: код {response.status_code}")
            result.append((name, response.content.decode("utf-8")))
        return result


class LandmarkTests(MarkupBase):
    def test_exactly_one_main_area(self):
        """Вложенный <main> — невалидная разметка и две главные области в навигации.

        Раньше `base.html` оборачивал содержимое в <main>, а каждый шаблон страницы
        открывал свой — то есть нарушение было на всех страницах сразу.
        """
        for role, names in (
            ("гость", None),
            ("студент", self.student),
            ("преподаватель", self.teacher),
        ):
            for name, html in self.pages(GUEST_PAGES if names is None else STUDENT_PAGES, names):
                self.assertEqual(
                    len(re.findall(r"<main\b", html)),
                    1,
                    f"{role} · {name}: главных областей не одна",
                )

    def test_skip_link_is_first_and_targets_content(self):
        for _, html in self.pages(GUEST_PAGES):
            self.assertIn('class="skip-link" href="#content"', html)
            self.assertIn('id="content"', html)

    def test_page_has_single_h1(self):
        for name, html in self.pages(STUDENT_PAGES, self.student):
            self.assertEqual(
                len(re.findall(r"<h1\b", html)), 1, f"{name}: заголовков первого уровня не один"
            )

    def test_heading_levels_do_not_skip(self):
        """Пропуск ступени (h1 → h3) ломает навигацию по заголовкам."""
        for name, html in self.pages(STUDENT_PAGES + ["courses:catalog"], self.student):
            levels = [int(m) for m in re.findall(r"<h([1-6])\b", html)]
            previous = 0
            for level in levels:
                if previous:
                    self.assertLessEqual(
                        level, previous + 1, f"{name}: скачок h{previous} → h{level}"
                    )
                previous = level


class FormLabelTests(MarkupBase):
    """Каждое поле ввода должно иметь доступное имя.

    Подсказка внутри поля (`placeholder`) именем не считается: она исчезает при
    вводе и не читается как подпись.
    """

    CONTROL = re.compile(r"<(input|select|textarea)\b([^>]*)>", re.S)

    def assert_all_named(self, html, page):
        labels = set(re.findall(r'<label[^>]*\bfor="([^"]+)"', html))
        for _tag, attrs in self.CONTROL.findall(html):
            if 'type="hidden"' in attrs:
                continue
            if "aria-label" in attrs or "aria-labelledby" in attrs:
                continue
            # Переключатели обычно обёрнуты в <label> — это тоже подпись.
            if 'type="radio"' in attrs or 'type="checkbox"' in attrs:
                continue
            ident = re.search(r'\bid="([^"]+)"', attrs)
            self.assertIsNotNone(ident, f"{page}: поле без id и без aria-label: {attrs[:60]}")
            self.assertIn(ident.group(1), labels, f"{page}: нет <label for> для {ident.group(1)}")

    def test_student_pages(self):
        for name, html in self.pages(STUDENT_PAGES, self.student):
            self.assert_all_named(html, name)

    def test_teacher_pages(self):
        for name, html in self.pages(TEACHER_PAGES, self.teacher):
            self.assert_all_named(html, name)

    def test_guest_pages(self):
        for name, html in self.pages(GUEST_PAGES):
            self.assert_all_named(html, name)

    def test_course_page_rating_is_grouped_and_named(self):
        """У звёздного рейтинга подпись группы и номер у каждого варианта.

        Без этого скринридер читает пять безымянных «★» подряд, не сообщая,
        к чему они относятся.
        """
        self.client.force_login(self.student)
        html = self.client.get(
            reverse("courses:course_detail", args=[self.course.slug])
        ).content.decode("utf-8")
        self.assertIn("<legend", html)
        self.assertIn("из 5", html)


class NavigationTests(MarkupBase):
    def test_menu_button_is_tied_to_the_menu(self):
        """Кнопка обязана ссылаться на существующий элемент и приходить скрытой.

        Скрытой — потому что показывает её скрипт: пока он не загрузился, кнопка
        ничем не управляет, а меню и так видно.
        """
        self.client.force_login(self.student)
        html = self.client.get(reverse("core:home")).content.decode("utf-8")
        button = re.search(r"<button[^>]*id=\"nav-toggle\"[^>]*>", html)
        self.assertIsNotNone(button, "кнопки меню нет в разметке")
        self.assertIn("hidden", button.group(0))
        self.assertIn('aria-expanded="false"', button.group(0))
        self.assertIn('aria-controls="site-nav"', button.group(0))
        self.assertIn('id="site-nav"', html)

    def test_nav_script_is_loaded(self):
        html = self.client.get(reverse("core:home")).content.decode("utf-8")
        self.assertIn("js/nav.js", html)


class AutonomyTests(MarkupBase):
    """Ноль внешних запросов — требование контура, в котором платформа работает.

    Проверяются и страницы платформы, и админка: django-jazzmin по умолчанию
    подключает шрифты с CDN, и эта настройка выключается явно.
    """

    EXTERNAL = re.compile(r'(?:src|href)="(https?://[^"]+)"')

    def test_no_external_resources_on_pages(self):
        for role, pages, user in (
            ("гость", GUEST_PAGES, None),
            ("студент", STUDENT_PAGES, self.student),
            ("преподаватель", TEACHER_PAGES, self.teacher),
        ):
            for name, html in self.pages(pages, user):
                found = self.EXTERNAL.findall(html)
                self.assertEqual(found, [], f"{role} · {name}: внешние ресурсы {found}")

    def test_no_external_resources_in_admin(self):
        admin = f.admin()
        self.client.force_login(admin)
        for url in ("/admin/", "/admin/courses/course/", "/admin/assessments/assignment/"):
            with self.subTest(url=url):
                html = self.client.get(url).content.decode("utf-8")
                found = self.EXTERNAL.findall(html)
                self.assertEqual(found, [], f"{url}: внешние ресурсы {found}")
