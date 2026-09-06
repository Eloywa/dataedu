"""Главная под роль, тренажёр, правовые страницы и заплатка сравнения строк."""

from django.db import connection
from django.test import TestCase
from django.urls import reverse

from accounts.legal import PRIVACY_VERSION, TERMS_VERSION
from core.apps import _like
from core.tests import factories as f
from courses.models import Course


class HomeTests(TestCase):
    def setUp(self):
        self.url = reverse("core:home")

    def test_guest_sees_the_landing(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")

    def test_teacher_sees_the_teacher_home(self):
        self.client.force_login(f.teacher())
        self.assertTemplateUsed(self.client.get(self.url), "core/home_teacher.html")

    def test_student_sees_the_student_home(self):
        self.client.force_login(f.student())
        self.assertTemplateUsed(self.client.get(self.url), "core/home_student.html")

    def test_student_is_offered_the_next_lesson(self):
        student = f.student()
        course, lessons = f.course_with_lessons(lessons=2)
        f.enroll(student, course)
        f.complete(student, lessons[0])

        self.client.force_login(student)
        current = self.client.get(self.url).context["current"]
        self.assertEqual(current["next_lesson"], lessons[1])
        self.assertEqual(current["pct"], 50)

    def test_student_who_finished_everything_has_no_current_course(self):
        student = f.student()
        course, lessons = f.course_with_lessons(lessons=1)
        f.enroll(student, course)
        f.complete_course(student, lessons)

        self.client.force_login(student)
        self.assertIsNone(self.client.get(self.url).context["current"])


class PublicPagesTests(TestCase):
    def test_trainer_is_open_to_guests(self):
        """Тренажёр работает целиком в браузере — вход для него не нужен."""
        self.assertEqual(self.client.get(reverse("core:trainer")).status_code, 200)

    def test_legal_pages_show_their_version(self):
        privacy = self.client.get(reverse("core:privacy"))
        self.assertContains(privacy, PRIVACY_VERSION)
        terms = self.client.get(reverse("core:terms"))
        self.assertContains(terms, TERMS_VERSION)


class SqliteLikeTests(TestCase):
    """Заплатка `LIKE` для SQLite (см. core/apps.py).

    Функция подменяет встроенное сравнение, то есть влияет на все запросы в
    разработке. Поэтому проверяется не только кириллица, но и то, что обычная
    семантика шаблона не поехала.
    """

    def test_case_insensitive_for_cyrillic(self):
        self.assertTrue(_like("%индекс%", "Индексы и производительность"))
        self.assertTrue(_like("%ИНДЕКС%", "Индексы и производительность"))

    def test_case_insensitive_for_latin(self):
        self.assertTrue(_like("%sql%", "Основы SQL"))

    def test_percent_matches_any_run(self):
        self.assertTrue(_like("а%я", "аллея"))
        self.assertFalse(_like("а%я", "аллеи"))

    def test_underscore_matches_one_character(self):
        self.assertTrue(_like("к_т", "кот"))
        self.assertFalse(_like("к_т", "крот"))

    def test_pattern_must_match_whole_value(self):
        self.assertFalse(_like("кот", "котёнок"))

    def test_escape_removes_special_meaning(self):
        self.assertTrue(_like(r"100\%", "100%", "\\"))
        self.assertFalse(_like(r"100\%", "100 процентов", "\\"))

    def test_regex_metacharacters_are_literal(self):
        """Точка и скобки в шаблоне — обычные символы, а не части выражения."""
        self.assertTrue(_like("a.b", "a.b"))
        self.assertFalse(_like("a.b", "axb"))

    def test_null_stays_null(self):
        self.assertIsNone(_like(None, "что-то"))
        self.assertIsNone(_like("%x%", None))

    def test_orm_search_uses_the_patched_function(self):
        f.course(title="Оконные функции SQL")
        found = Course.objects.filter(title__icontains="оконные")
        self.assertEqual(found.count(), 1)

    def test_escaped_search_term_is_literal(self):
        """Проценты в названии не должны превращаться в подстановочный знак."""
        f.course(title="Скидка 100% на курс")
        f.course(title="Обычный курс")
        self.assertEqual(Course.objects.filter(title__icontains="100%").count(), 1)

    def test_patch_is_not_applied_to_postgres(self):
        if connection.vendor == "sqlite":
            self.skipTest("прогон идёт на SQLite — проверять нечего")
        # На PostgreSQL регистронезависимость даёт сама СУБД.
        f.course(title="Оконные функции SQL")
        self.assertEqual(Course.objects.filter(title__icontains="оконные").count(), 1)


class TeacherHomeTests(TestCase):
    """Главная преподавателя: до этапа 12 там висела заглушка «на следующих этапах»."""

    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher)
        self.url = reverse("core:home")

    def test_links_to_every_teacher_section(self):
        self.client.force_login(self.teacher)
        response = self.client.get(self.url)
        for name in (
            "teaching:dashboard",
            "teaching:analytics",
            "teaching:report",
            "teaching:submissions",
            "messaging:inbox",
        ):
            self.assertContains(response, reverse(name))

    def test_shows_pending_queue_size(self):
        student = f.student()
        task = f.assignment(self.course, auto=False)
        f.submission(task, student, status="submitted")

        self.client.force_login(self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.context["pending"], 1)
        self.assertContains(response, "ждут проверки: 1")

    def test_empty_queue_is_said_plainly(self):
        self.client.force_login(self.teacher)
        self.assertContains(self.client.get(self.url), "непроверенных нет")

    def test_no_stale_placeholder_left(self):
        self.client.force_login(self.teacher)
        self.assertNotContains(self.client.get(self.url), "на следующих этапах")
