"""Каталог и страница курса: отбор, запись, отзывы, последовательное открытие."""

from django.db import connection
from django.test import TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from core.tests import factories as f
from courses.models import CourseRating
from learning.models import Enrollment


class CatalogTests(TestCase):
    def setUp(self):
        self.url = reverse("courses:catalog")

    def test_open_to_guests(self):
        f.course(title="Основы SQL")
        self.assertContains(self.client.get(self.url), "Основы SQL")

    def test_unpublished_course_is_hidden(self):
        f.course(title="Черновик", published=False)
        self.assertNotContains(self.client.get(self.url), "Черновик")

    def test_search_by_title(self):
        f.course(title="Индексы и производительность")
        f.course(title="Оконные функции")
        response = self.client.get(self.url, {"q": "Индексы"})
        self.assertContains(response, "Индексы")
        self.assertNotContains(response, "Оконные")

    def test_search_ignores_case_in_cyrillic(self):
        """Встроенный UPPER в SQLite кириллицу не приводит — см. core/apps.py.

        Без подмены функций поиск «индекс» не находил бы «Индексы», причём только
        в разработке: на PostgreSQL тот же запрос работает. Расхождение сред опаснее
        самой ошибки, поэтому оно закрыто и закреплено этим тестом.
        """
        f.course(title="Индексы и производительность")
        self.assertContains(self.client.get(self.url, {"q": "индекс"}), "Индексы")
        self.assertContains(self.client.get(self.url, {"q": "ИНДЕКС"}), "Индексы")

    def test_filter_by_level(self):
        f.course(title="Простой курс", level="basic")
        f.course(title="Сложный курс", level="advanced")
        response = self.client.get(self.url, {"level": "advanced"})
        self.assertContains(response, "Сложный курс")
        self.assertNotContains(response, "Простой курс")

    def test_filter_by_topic(self):
        from courses.models import CourseTopic

        topic = f.topic(code="joins")
        tagged = f.course(title="С темой")
        f.course(title="Без темы")
        CourseTopic.objects.create(course=tagged, topic=topic)

        response = self.client.get(self.url, {"topic": "joins"})
        self.assertContains(response, "С темой")
        self.assertNotContains(response, "Без темы")

    def test_sort_by_rating(self):
        weak = f.course(title="Слабый")
        strong = f.course(title="Сильный")
        f.rate(f.student(), weak, rating=2)
        f.rate(f.student(), strong, rating=5)

        titles = [c.title for c in self.client.get(self.url, {"sort": "rating"}).context["courses"]]
        self.assertEqual(titles[0], "Сильный")

    def test_enrolled_student_sees_progress(self):
        student = f.student()
        course, lessons = f.course_with_lessons(lessons=2)
        f.enroll(student, course)
        f.complete(student, lessons[0])

        self.client.force_login(student)
        card = self.client.get(self.url).context["courses"][0]
        self.assertTrue(card.is_enrolled)
        self.assertEqual(card.prog["pct"], 50)

    @override_settings(PAGE_SIZE=3)
    def test_pagination_limits_the_page(self):
        for i in range(7):
            f.course(title=f"Курс {i}")
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["courses"]), 3)
        self.assertEqual(response.context["page"].paginator.num_pages, 3)

    @override_settings(PAGE_SIZE=3)
    def test_pagination_keeps_the_filter(self):
        for i in range(7):
            f.course(title=f"SQL {i}", level="advanced")
        f.course(title="Лишний", level="basic")
        response = self.client.get(self.url, {"level": "advanced", "page": 2})
        self.assertNotContains(response, "Лишний")

    def test_query_count_does_not_grow_with_courses(self):
        """Каталог не должен делать по паре запросов на карточку.

        Проверяется не конкретное число, а его неизменность: шесть курсов и
        двенадцать обязаны стоить одинаково. Именно это ломается, когда прогресс
        начинают считать внутри цикла по карточкам.
        """
        student = f.student()

        def add_courses(n):
            for _ in range(n):
                course, lessons = f.course_with_lessons(lessons=2)
                f.enroll(student, course)
                f.complete(student, lessons[0])

        self.client.force_login(student)

        add_courses(6)
        with CaptureQueriesContext(connection) as few:
            self.client.get(self.url)

        add_courses(6)
        with CaptureQueriesContext(connection) as many:
            self.client.get(self.url)

        self.assertEqual(len(many), len(few))


class CourseDetailTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(
            author=self.teacher, modules=2, lessons=2
        )
        self.student = f.student()
        self.url = reverse("courses:course_detail", args=[self.course.slug])

    def test_unpublished_course_is_404(self):
        hidden = f.course(published=False)
        response = self.client.get(reverse("courses:course_detail", args=[hidden.slug]))
        self.assertEqual(response.status_code, 404)

    def test_second_week_is_locked_until_first_is_done(self):
        f.enroll(self.student, self.course)
        self.client.force_login(self.student)
        modules = self.client.get(self.url).context["modules"]
        self.assertTrue(modules[0].gate["unlocked"])
        self.assertFalse(modules[1].gate["unlocked"])

    def test_second_week_opens_after_the_first(self):
        f.enroll(self.student, self.course)
        f.complete(self.student, self.lessons[0])
        f.complete(self.student, self.lessons[1])

        self.client.force_login(self.student)
        modules = self.client.get(self.url).context["modules"]
        self.assertTrue(modules[1].gate["unlocked"])

    def test_teacher_sees_all_weeks(self):
        self.client.force_login(self.teacher)
        modules = self.client.get(self.url).context["modules"]
        self.assertTrue(all(m.gate["unlocked"] for m in modules))

    def test_next_lesson_is_the_first_unfinished(self):
        f.enroll(self.student, self.course)
        f.complete(self.student, self.lessons[0])
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(self.url).context["next_lesson"], self.lessons[1])


class EnrollTests(TestCase):
    def setUp(self):
        self.course = f.course()
        self.student = f.student()
        self.url = reverse("courses:enroll", args=[self.course.slug])

    def test_student_enrolls(self):
        self.client.force_login(self.student)
        self.client.post(self.url)
        self.assertTrue(Enrollment.objects.filter(user=self.student, course=self.course).exists())

    def test_second_enrollment_does_not_duplicate(self):
        self.client.force_login(self.student)
        self.client.post(self.url)
        self.client.post(self.url)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_guest_is_sent_to_login(self):
        response = self.client.post(self.url)
        self.assertIn("/login/", response["Location"])
        self.assertEqual(Enrollment.objects.count(), 0)


class ReviewTests(TestCase):
    def setUp(self):
        self.course = f.course()
        self.student = f.student()
        self.url = reverse("courses:review", args=[self.course.slug])

    def test_review_is_saved(self):
        self.client.force_login(self.student)
        self.client.post(self.url, {"rating": "5", "comment": "полезно"})
        rating = CourseRating.objects.get()
        self.assertEqual(rating.rating, 5)
        self.assertEqual(rating.comment, "полезно")

    def test_second_review_replaces_the_first(self):
        self.client.force_login(self.student)
        self.client.post(self.url, {"rating": "5", "comment": "первое"})
        self.client.post(self.url, {"rating": "3", "comment": "передумал"})
        self.assertEqual(CourseRating.objects.count(), 1)
        self.assertEqual(CourseRating.objects.get().rating, 3)

    def test_out_of_scale_rating_is_ignored(self):
        self.client.force_login(self.student)
        self.client.post(self.url, {"rating": "9", "comment": "накрутка"})
        self.assertEqual(CourseRating.objects.count(), 0)

    def test_non_numeric_rating_does_not_crash(self):
        self.client.force_login(self.student)
        response = self.client.post(self.url, {"rating": "пять"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CourseRating.objects.count(), 0)


class LessonTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(
            author=self.teacher, modules=2, lessons=1
        )
        self.student = f.student()
        f.enroll(self.student, self.course)

    def test_lesson_renders_theory(self):
        self.client.force_login(self.student)
        response = self.client.get(
            reverse("courses:lesson_detail", args=[self.lessons[0].pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.lessons[0].title)

    def test_locked_lesson_shows_the_lock_page(self):
        self.client.force_login(self.student)
        response = self.client.get(
            reverse("courses:lesson_detail", args=[self.lessons[1].pk])
        )
        self.assertTemplateUsed(response, "lessons/lesson_locked.html")

    def test_completing_a_lesson_records_progress(self):
        f.achievement("first_lesson")
        self.client.force_login(self.student)
        self.client.post(reverse("courses:complete_lesson", args=[self.lessons[0].pk]))
        self.student.refresh_from_db()
        # 10 XP за урок + 25 за достижение «Первый шаг».
        self.assertEqual(self.student.xp, 35)

    def test_navigation_between_lessons(self):
        self.client.force_login(self.teacher)
        response = self.client.get(
            reverse("courses:lesson_detail", args=[self.lessons[0].pk])
        )
        self.assertIsNone(response.context["prev_lesson"])
        self.assertEqual(response.context["next_lesson"], self.lessons[1])


class ReflectionTests(TestCase):
    def setUp(self):
        self.course, self.lessons = f.course_with_lessons(lessons=1)
        self.lesson = self.lessons[0]
        self.student = f.student()
        self.url = reverse("courses:submit_reflection", args=[self.lesson.pk])

    def test_reflection_is_saved(self):
        self.client.force_login(self.student)
        self.client.post(self.url, {"clarity": "4", "difficulty": "2", "comment": "ок"})
        from learning.models import Reflection

        reflection = Reflection.objects.get()
        self.assertEqual((reflection.clarity_rating, reflection.difficulty_rating), (4, 2))

    def test_out_of_scale_values_are_rejected(self):
        from learning.models import Reflection

        self.client.force_login(self.student)
        response = self.client.post(self.url, {"clarity": "9", "difficulty": "2"})
        self.assertIn("reflection=invalid", response["Location"])
        self.assertEqual(Reflection.objects.count(), 0)

    def test_teacher_does_not_fill_reflection(self):
        """Оценки преподавателя исказили бы данные исследования."""
        from learning.models import Reflection

        self.client.force_login(f.teacher())
        self.client.post(self.url, {"clarity": "5", "difficulty": "1"})
        self.assertEqual(Reflection.objects.count(), 0)

    def test_editing_replaces_the_previous_answer(self):
        from learning.models import Reflection

        self.client.force_login(self.student)
        self.client.post(self.url, {"clarity": "3", "difficulty": "3"})
        self.client.post(self.url, {"clarity": "5", "difficulty": "1"})
        self.assertEqual(Reflection.objects.count(), 1)
        self.assertEqual(Reflection.objects.get().clarity_rating, 5)

    def test_xp_is_given_once_per_lesson(self):
        self.client.force_login(self.student)
        self.client.post(self.url, {"clarity": "3", "difficulty": "3"})
        self.student.refresh_from_db()
        after_first = self.student.xp

        self.client.post(self.url, {"clarity": "4", "difficulty": "2"})
        self.student.refresh_from_db()
        self.assertEqual(self.student.xp, after_first)
