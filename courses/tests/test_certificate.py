"""Сертификат о прохождении курса."""

from django.test import TestCase, override_settings
from django.urls import reverse

from core.tests import factories as f
from courses.views import certificate_code


class CertificateAccessTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher(username="petrova")
        self.course, self.lessons = f.course_with_lessons(author=self.teacher, lessons=2)
        self.student = f.student(username="ivanov", display_name="Иванов И. И.")
        self.url = reverse("courses:certificate", args=[self.course.slug])

    def test_guest_is_sent_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_not_enrolled_student_gets_the_locked_page(self):
        self.client.force_login(self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "courses/certificate_locked.html")

    def test_partial_progress_is_not_enough(self):
        f.enroll(self.student, self.course)
        f.complete(self.student, self.lessons[0])
        self.client.force_login(self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "50%", status_code=403)

    def test_full_completion_opens_the_certificate(self):
        f.enroll(self.student, self.course)
        f.complete_course(self.student, self.lessons)
        self.client.force_login(self.student)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "courses/certificate.html")
        self.assertContains(response, "Иванов И. И.")
        self.assertContains(response, self.course.title)
        self.assertEqual(response.context["lesson_count"], 2)

    def test_certificate_names_the_author_as_teacher(self):
        f.enroll(self.student, self.course)
        f.complete_course(self.student, self.lessons)
        self.client.force_login(self.student)
        self.assertContains(self.client.get(self.url), "petrova")

    def test_unpublished_course_is_404(self):
        hidden, lessons = f.course_with_lessons(author=self.teacher, published=False)
        f.enroll(self.student, hidden)
        f.complete_course(self.student, lessons)
        self.client.force_login(self.student)
        response = self.client.get(reverse("courses:certificate", args=[hidden.slug]))
        self.assertEqual(response.status_code, 404)

    def test_link_appears_on_the_course_page_only_when_earned(self):
        f.enroll(self.student, self.course)
        self.client.force_login(self.student)
        course_url = reverse("courses:course_detail", args=[self.course.slug])
        self.assertFalse(self.client.get(course_url).context["certificate_ready"])

        f.complete_course(self.student, self.lessons)
        self.assertTrue(self.client.get(course_url).context["certificate_ready"])


class CertificateDateTests(TestCase):
    def test_date_is_the_last_completed_lesson_not_today(self):
        """Иначе сертификат показывал бы разную дату при каждом открытии."""
        teacher = f.teacher()
        course, lessons = f.course_with_lessons(author=teacher, lessons=2)
        student = f.student()
        f.enroll(student, course)
        f.complete_course(student, lessons)

        self.client.force_login(student)
        url = reverse("courses:certificate", args=[course.slug])
        first = self.client.get(url).context["issued_at"]
        second = self.client.get(url).context["issued_at"]
        self.assertEqual(first, second)


class CertificateCodeTests(TestCase):
    def test_code_is_stable_for_the_same_pair(self):
        student, course = f.student(), f.course()
        self.assertEqual(
            certificate_code(student.pk, course.pk), certificate_code(student.pk, course.pk)
        )

    def test_different_students_get_different_codes(self):
        course = f.course()
        self.assertNotEqual(
            certificate_code(f.student().pk, course.pk),
            certificate_code(f.student().pk, course.pk),
        )

    def test_different_courses_get_different_codes(self):
        student = f.student()
        self.assertNotEqual(
            certificate_code(student.pk, f.course().pk),
            certificate_code(student.pk, f.course().pk),
        )

    def test_code_has_expected_shape(self):
        code = certificate_code(f.student().pk, f.course().pk)
        self.assertTrue(code.startswith("DE-"))
        self.assertEqual(len(code), 11)

    @override_settings(SECRET_KEY="another-secret-entirely")
    def test_code_depends_on_the_secret(self):
        """Ключ — соль: без него код нельзя подобрать к чужой паре."""
        student, course = f.student(), f.course()
        with_other_key = certificate_code(student.pk, course.pk)

        with override_settings(SECRET_KEY="original-secret"):
            with_original = certificate_code(student.pk, course.pk)

        self.assertNotEqual(with_other_key, with_original)
