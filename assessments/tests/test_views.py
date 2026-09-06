"""Тесты урока и практические задания: оценивание на сервере."""

import json

from django.test import TestCase
from django.urls import reverse

from assessments.models import AnswerSubmission, Submission, TestAttempt
from core.tests import factories as f


class LessonTestTests(TestCase):
    def setUp(self):
        self.course, self.lessons = f.course_with_lessons(lessons=1)
        self.lesson = self.lessons[0]
        self.test = f.test_for(self.lesson, pass_score=60)
        self.first, self.first_right, self.first_wrong = f.question(self.test, order_index=0)
        self.second, self.second_right, self.second_wrong = f.question(self.test, order_index=1)
        self.student = f.student()
        self.url = reverse("assessments:lesson_test", args=[self.lesson.pk])
        f.achievement("first_lesson")
        f.achievement("test_master")

    def test_guest_is_sent_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_questions_are_shown(self):
        self.client.force_login(self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["questions"]), 2)

    def test_all_correct_gives_full_score_and_completes_the_lesson(self):
        self.client.force_login(self.student)
        response = self.client.post(
            self.url,
            {
                f"q_{self.first.pk}": str(self.first_right.pk),
                f"q_{self.second.pk}": str(self.second_right.pk),
            },
        )
        self.assertEqual(response.context["score"], 100)
        self.assertTrue(response.context["is_passed"])

        attempt = TestAttempt.objects.get()
        self.assertEqual(int(attempt.score), 100)
        self.assertTrue(attempt.is_passed)

    def test_all_wrong_fails(self):
        self.client.force_login(self.student)
        response = self.client.post(
            self.url,
            {
                f"q_{self.first.pk}": str(self.first_wrong.pk),
                f"q_{self.second.pk}": str(self.second_wrong.pk),
            },
        )
        self.assertEqual(response.context["score"], 0)
        self.assertFalse(response.context["is_passed"])

    def test_half_correct_is_below_the_threshold(self):
        self.client.force_login(self.student)
        response = self.client.post(
            self.url,
            {
                f"q_{self.first.pk}": str(self.first_right.pk),
                f"q_{self.second.pk}": str(self.second_wrong.pk),
            },
        )
        self.assertEqual(response.context["score"], 50)
        self.assertFalse(response.context["is_passed"])

    def test_forged_option_is_ignored(self):
        """Вариант из другого вопроса не должен засчитываться."""
        other_test = f.test_for(f.lesson(self.lesson.module, order_index=5))
        _, alien_option, _ = f.question(other_test)

        self.client.force_login(self.student)
        response = self.client.post(
            self.url,
            {
                f"q_{self.first.pk}": str(alien_option.pk),
                f"q_{self.second.pk}": str(self.second_right.pk),
            },
        )
        self.assertEqual(response.context["score"], 50)

    def test_unanswered_question_counts_as_wrong(self):
        self.client.force_login(self.student)
        response = self.client.post(self.url, {f"q_{self.first.pk}": str(self.first_right.pk)})
        self.assertEqual(response.context["score"], 50)

    def test_answers_are_recorded_for_analytics(self):
        self.client.force_login(self.student)
        self.client.post(
            self.url,
            {
                f"q_{self.first.pk}": str(self.first_right.pk),
                f"q_{self.second.pk}": str(self.second_wrong.pk),
            },
        )
        self.assertEqual(AnswerSubmission.objects.count(), 2)
        self.assertEqual(AnswerSubmission.objects.filter(is_correct=True).count(), 1)

    def test_lesson_without_test_redirects_back(self):
        bare = f.lesson(self.lesson.module, order_index=9)
        self.client.force_login(self.student)
        response = self.client.get(reverse("assessments:lesson_test", args=[bare.pk]))
        self.assertEqual(response.status_code, 302)


class PracticeListTests(TestCase):
    def setUp(self):
        self.course, self.lessons = f.course_with_lessons(lessons=1)
        self.student = f.student()
        self.url = reverse("assessments:practice")

    def test_autocheckable_and_manual_are_separated(self):
        auto = f.assignment(self.course, auto=True)
        manual = f.assignment(self.course, auto=False)

        self.client.force_login(self.student)
        response = self.client.get(self.url)
        self.assertEqual([a.pk for a in response.context["assignments"]], [auto.pk])
        self.assertEqual([a.pk for a in response.context["manual_assignments"]], [manual.pk])

    def test_sql_task_without_reference_is_manual(self):
        """Иначе студент получал бы редактор, кнопка в котором отвечает ошибкой."""
        from assessments.models import Assignment

        task = Assignment.objects.create(
            course=self.course, title="SQL без эталона", level="basic",
            type="sql", expected_result=None, max_score=10,
        )
        self.client.force_login(self.student)
        response = self.client.get(self.url)
        self.assertIn(task.pk, [a.pk for a in response.context["manual_assignments"]])

    def test_solved_task_is_marked(self):
        task = f.assignment(self.course, auto=True)
        f.submission(task, self.student, status="graded", score=100)

        self.client.force_login(self.student)
        response = self.client.get(self.url)
        self.assertTrue(response.context["assignments"][0].is_solved)


class CheckAssignmentTests(TestCase):
    def setUp(self):
        self.course, self.lessons = f.course_with_lessons(lessons=1)
        self.student = f.student()
        self.task = f.assignment(self.course, auto=True, max_score=100)
        self.url = reverse("assessments:check", args=[self.task.pk])

    def post(self, payload):
        return self.client.post(self.url, json.dumps(payload), content_type="application/json")

    def test_correct_result_is_scored_by_the_server(self):
        """Балл ставит сервер: браузер присылает результат, а не оценку."""
        self.client.force_login(self.student)
        response = self.post({"sql": "SELECT 1 AS n;", "columns": ["n"], "rows": [[1]]})
        self.assertTrue(response.json()["passed"])

        submission = Submission.objects.get()
        self.assertEqual(int(submission.score), 100)
        self.assertEqual(submission.status, "graded")

    def test_wrong_result_scores_zero_and_explains(self):
        self.client.force_login(self.student)
        response = self.post({"sql": "SELECT 2;", "columns": ["n"], "rows": [[2]]})
        data = response.json()
        self.assertFalse(data["passed"])
        self.assertNotEqual(data["hint"], "")
        self.assertEqual(int(Submission.objects.get().score), 0)

    def test_manual_task_has_no_autocheck(self):
        manual = f.assignment(self.course, auto=False)
        self.client.force_login(self.student)
        response = self.client.post(
            reverse("assessments:check", args=[manual.pk]),
            json.dumps({"sql": "", "columns": [], "rows": []}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Submission.objects.exists())

    def test_broken_payload_is_rejected(self):
        self.client.force_login(self.student)
        response = self.client.post(self.url, "не json", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Submission.objects.exists())

    def test_guest_cannot_submit(self):
        response = self.post({"sql": "SELECT 1;", "columns": ["n"], "rows": [[1]]})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Submission.objects.exists())

    def test_get_is_rejected(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_feedback_is_saved_for_the_teacher(self):
        self.client.force_login(self.student)
        self.post({"sql": "SELECT 2;", "columns": ["n"], "rows": [[2]]})
        self.assertIn("Автопроверка", Submission.objects.get().feedback)

    def test_xp_for_solving_is_given_once(self):
        self.client.force_login(self.student)
        self.post({"sql": "SELECT 1;", "columns": ["n"], "rows": [[1]]})
        self.student.refresh_from_db()
        after_first = self.student.xp

        self.post({"sql": "SELECT 1;", "columns": ["n"], "rows": [[1]]})
        self.student.refresh_from_db()
        self.assertEqual(self.student.xp, after_first)
