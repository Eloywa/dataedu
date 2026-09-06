"""Страницы преподавателя: доступ, изоляция, проверка работ, карточка студента."""

from django.test import TestCase
from django.urls import reverse

from assessments.models import Submission
from core.tests import factories as f
from gamification.models import UserAchievement
from learning import grading


class CleanGradeTests(TestCase):
    """Разбор формы проверки — балл приходит от недоверенной стороны."""

    def test_valid_form(self):
        data, error = grading.clean_grade("80", " хорошо ", "graded", 100)
        self.assertIsNone(error)
        self.assertEqual(data, {"score": 80, "feedback": "хорошо", "status": "graded"})

    def test_empty_feedback_becomes_none(self):
        data, _ = grading.clean_grade("10", "   ", "graded", 100)
        self.assertIsNone(data["feedback"])

    def test_score_is_rounded(self):
        data, _ = grading.clean_grade("84.7", "", "graded", 100)
        self.assertEqual(data["score"], 85)

    def test_comma_decimal_is_accepted(self):
        data, _ = grading.clean_grade("84,2", "", "graded", 100)
        self.assertEqual(data["score"], 84)

    def test_non_numeric_is_rejected(self):
        self.assertIsNone(grading.clean_grade("отлично", "", "graded", 100)[0])

    def test_out_of_range_is_rejected(self):
        self.assertIsNone(grading.clean_grade("101", "", "graded", 100)[0])
        self.assertIsNone(grading.clean_grade("-1", "", "graded", 100)[0])

    def test_boundaries_are_allowed(self):
        self.assertEqual(grading.clean_grade("0", "", "graded", 100)[0]["score"], 0)
        self.assertEqual(grading.clean_grade("100", "", "graded", 100)[0]["score"], 100)

    def test_unknown_status_is_rejected(self):
        self.assertIsNone(grading.clean_grade("50", "", "удалено", 100)[0])
        self.assertIsNone(grading.clean_grade("50", "", "", 100)[0])


class TeacherAccessTests(TestCase):
    """Ни одна страница преподавателя не должна открываться студенту или гостю."""

    def setUp(self):
        self.teacher = f.teacher()
        self.student = f.student()
        self.urls = [
            reverse("teaching:dashboard"),
            reverse("teaching:analytics"),
            reverse("teaching:report"),
            reverse("teaching:submissions"),
            reverse("teaching:export_students"),
            reverse("teaching:export_difficulty"),
            reverse("teaching:export_vedomost"),
            reverse("teaching:export_moodle"),
        ]

    def test_guest_goes_to_login(self):
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn("/login/", response["Location"])

    def test_student_is_sent_home(self):
        self.client.force_login(self.student)
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertNotIn("teacher", response["Location"])

    def test_teacher_gets_every_page(self):
        self.client.force_login(self.teacher)
        for url in self.urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)


class DashboardTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher)
        self.student = f.student(username="ivanov")
        f.enroll(self.student, self.course)
        self.client.force_login(self.teacher)

    def test_shows_own_students(self):
        response = self.client.get(reverse("teaching:dashboard"))
        self.assertContains(response, "ivanov")

    def test_does_not_show_other_teachers_students(self):
        other_course, _ = f.course_with_lessons(author=f.teacher())
        f.enroll(f.student(username="petrov"), other_course)
        response = self.client.get(reverse("teaching:dashboard"))
        self.assertNotContains(response, "petrov")

    def test_unknown_course_filter_is_404(self):
        """Чужой курс в строке запроса не должен показывать чужих студентов."""
        alien = f.course(author=f.teacher(), slug="alien-course")
        response = self.client.get(reverse("teaching:dashboard"), {"course": alien.slug})
        self.assertEqual(response.status_code, 404)


class ExportTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher)
        self.student = f.student(username="ivanov")
        f.enroll(self.student, self.course)
        self.client.force_login(self.teacher)

    def test_students_csv_has_bom_and_semicolons(self):
        """Без BOM Excel на русской локали читает UTF-8 как cp1251."""
        response = self.client.get(reverse("teaching:export_students"))
        body = response.content.decode("utf-8")
        self.assertTrue(body.startswith("﻿"))
        self.assertIn(";", body.splitlines()[0])
        self.assertIn("ivanov", body)

    def test_moodle_csv_has_no_bom_and_commas(self):
        """Мастер импорта Moodle приклеил бы BOM к имени первого столбца."""
        response = self.client.get(reverse("teaching:export_vedomost"))
        self.assertTrue(response.content.decode("utf-8").startswith("﻿"))

        response = self.client.get(reverse("teaching:export_moodle"))
        body = response.content.decode("utf-8")
        self.assertFalse(body.startswith("﻿"))
        self.assertTrue(body.splitlines()[0].startswith("username,"))

    def test_export_is_an_attachment(self):
        response = self.client.get(reverse("teaching:export_students"))
        self.assertIn("attachment", response["Content-Disposition"])


class SubmissionQueueTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher)
        self.student = f.student(username="ivanov")
        f.enroll(self.student, self.course)
        self.task = f.assignment(self.course, auto=False, max_score=100)
        self.client.force_login(self.teacher)

    def test_queue_shows_own_work(self):
        f.submission(self.task, self.student, status="submitted")
        response = self.client.get(reverse("teaching:submissions"))
        self.assertContains(response, "ivanov")
        self.assertEqual(response.context["summary"]["pending"], 1)

    def test_queue_hides_other_teachers_work(self):
        other_course, _ = f.course_with_lessons(author=f.teacher())
        f.submission(f.assignment(other_course, auto=False), f.student(username="petrov"))
        response = self.client.get(reverse("teaching:submissions"))
        self.assertNotContains(response, "petrov")

    def test_pending_work_comes_first(self):
        f.submission(self.task, f.student(), status="graded", score=100)
        pending = f.submission(self.task, self.student, status="submitted")
        response = self.client.get(reverse("teaching:submissions"))
        self.assertEqual(response.context["rows"][0].pk, pending.pk)

    def test_summary_counts_whole_queue_not_the_page(self):
        for _ in range(30):
            f.submission(self.task, f.student(), status="submitted")
        response = self.client.get(reverse("teaching:submissions"))
        self.assertEqual(response.context["summary"]["pending"], 30)
        self.assertLess(len(response.context["rows"]), 30)


class GradeTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher)
        self.student = f.student()
        self.task = f.assignment(self.course, auto=False, max_score=100)
        self.submission = f.submission(self.task, self.student, status="submitted")
        self.url = reverse("teaching:grade", args=[self.submission.pk])

    def test_teacher_grades_the_work(self):
        self.client.force_login(self.teacher)
        response = self.client.post(
            self.url, {"score": "85", "feedback": "разобрано", "status": "graded"}
        )
        self.assertEqual(response.status_code, 302)

        self.submission.refresh_from_db()
        self.assertEqual(int(self.submission.score), 85)
        self.assertEqual(self.submission.feedback, "разобрано")
        self.assertEqual(self.submission.status, "graded")
        self.assertEqual(self.submission.graded_by, self.teacher)
        self.assertIsNotNone(self.submission.graded_at)

    def test_returning_for_rework(self):
        self.client.force_login(self.teacher)
        self.client.post(self.url, {"score": "30", "feedback": "", "status": "returned"})
        self.submission.refresh_from_db()
        self.assertEqual(self.submission.status, "returned")

    def test_score_above_maximum_is_rejected(self):
        self.client.force_login(self.teacher)
        response = self.client.post(self.url, {"score": "500", "status": "graded"})
        self.assertIn("error=", response["Location"])
        self.submission.refresh_from_db()
        self.assertIsNone(self.submission.score)

    def test_other_teacher_cannot_grade(self):
        """Подстановка чужого идентификатора в форму не должна проходить."""
        self.client.force_login(f.teacher())
        response = self.client.post(self.url, {"score": "100", "status": "graded"})
        self.assertEqual(response.status_code, 404)
        self.submission.refresh_from_db()
        self.assertIsNone(self.submission.score)

    def test_student_cannot_grade_own_work(self):
        self.client.force_login(self.student)
        response = self.client.post(self.url, {"score": "100", "status": "graded"})
        self.assertEqual(response.status_code, 302)
        self.submission.refresh_from_db()
        self.assertIsNone(self.submission.score)

    def test_get_is_rejected(self):
        self.client.force_login(self.teacher)
        self.assertEqual(self.client.get(self.url).status_code, 405)


class StudentCardTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher, lessons=2)
        self.student = f.student(username="ivanov")
        f.enroll(self.student, self.course)
        self.url = reverse("teaching:student", args=[self.student.pk])

    def test_teacher_opens_own_students_card(self):
        f.complete(self.student, self.lessons[0])
        self.client.force_login(self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ivanov")
        self.assertEqual(response.context["card"]["enrollments"][0].pct, 50)

    def test_stranger_student_is_not_found(self):
        """Иначе преподаватель открыл бы прогресс любого пользователя платформы."""
        outsider = f.student()
        self.client.force_login(self.teacher)
        response = self.client.get(reverse("teaching:student", args=[outsider.pk]))
        self.assertEqual(response.status_code, 404)

    def test_student_cannot_open_cards(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_only_last_attempt_per_test_is_shown(self):
        test = f.test_for(self.lessons[0])
        f.attempt(self.student, test, score=30, passed=False)
        f.attempt(self.student, test, score=90, passed=True)
        self.client.force_login(self.teacher)
        attempts = self.client.get(self.url).context["card"]["attempts"]
        self.assertEqual(len(attempts), 1)

    def test_anonymous_comment_is_not_attributed(self):
        """Карточка сама указывает на автора — анонимный комментарий здесь нельзя."""
        f.reflection(
            self.student, self.lessons[0], comment="слишком быстро", anonymous=True
        )
        self.client.force_login(self.teacher)
        response = self.client.get(self.url)
        self.assertNotContains(response, "слишком быстро")

    def test_signed_comment_is_shown(self):
        f.reflection(self.student, self.lessons[0], comment="всё понятно", anonymous=False)
        self.client.force_login(self.teacher)
        self.assertContains(self.client.get(self.url), "всё понятно")


class DefendProjectTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher)
        self.student = f.student()
        f.enroll(self.student, self.course)
        self.final = f.assignment(self.course, auto=False, is_final=True, max_score=100)
        f.achievement("project_defender", title="Защитник проекта", xp_reward=50)
        self.url = reverse("teaching:defend_project", args=[self.student.pk])

    def test_defence_creates_graded_work_and_award(self):
        self.client.force_login(self.teacher)
        self.client.post(self.url)

        submission = Submission.objects.get(assignment=self.final, user=self.student)
        self.assertEqual(submission.status, "graded")
        self.assertEqual(int(submission.score), 100)
        self.assertEqual(submission.graded_by, self.teacher)
        self.assertTrue(
            UserAchievement.objects.filter(
                user=self.student, achievement__code="project_defender"
            ).exists()
        )

    def test_second_defence_does_not_duplicate(self):
        self.client.force_login(self.teacher)
        self.client.post(self.url)
        self.client.post(self.url)
        self.assertEqual(Submission.objects.filter(assignment=self.final).count(), 1)
        self.assertEqual(UserAchievement.objects.filter(user=self.student).count(), 1)

    def test_other_teacher_cannot_record_defence(self):
        self.client.force_login(f.teacher())
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Submission.objects.exists())

    def test_without_final_assignment_nothing_happens(self):
        self.final.delete()
        self.client.force_login(self.teacher)
        response = self.client.post(self.url)
        self.assertIn("error=", response["Location"])
        self.assertFalse(Submission.objects.exists())
