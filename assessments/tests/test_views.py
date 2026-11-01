"""Тесты урока и практические задания: оценивание на сервере."""

import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from assessments.manual import MAX_ANSWER_CHARS, MAX_UPLOAD_BYTES
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
        f.enroll(self.student, self.course)
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

    def test_student_outside_the_course_cannot_take_the_test(self):
        self.client.force_login(f.student())
        response = self.client.post(self.url, {f"q_{self.first.pk}": str(self.first_right.pk)})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TestAttempt.objects.exists())

    def test_locked_week_keeps_its_test_closed(self):
        """Экран «урок закрыт» не защищает сам: попытка завершила бы урок с XP."""
        _, lessons = f.course_with_lessons(modules=2, lessons=1)
        closed_test = f.test_for(lessons[1])
        question, right, _ = f.question(closed_test)
        f.enroll(self.student, lessons[1].module.course)

        self.client.force_login(self.student)
        response = self.client.post(
            reverse("assessments:lesson_test", args=[lessons[1].pk]),
            {f"q_{question.pk}": str(right.pk)},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TestAttempt.objects.filter(test=closed_test).exists())

    def test_draft_course_test_is_hidden(self):
        course, lessons = f.course_with_lessons(lessons=1, published=False)
        f.test_for(lessons[0])
        f.enroll(self.student, course)
        self.client.force_login(self.student)
        response = self.client.get(reverse("assessments:lesson_test", args=[lessons[0].pk]))
        self.assertEqual(response.status_code, 404)


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
            course=self.course,
            title="SQL без эталона",
            level="basic",
            type="sql",
            expected_result=None,
            max_score=10,
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

    def test_draft_course_tasks_are_hidden(self):
        draft = f.course(published=False)
        task = f.assignment(draft, auto=True)
        self.client.force_login(self.student)
        response = self.client.get(self.url)
        self.assertNotIn(task.pk, [a.pk for a in response.context["assignments"]])
        self.assertEqual(
            self.client.get(reverse("assessments:assignment_detail", args=[task.pk])).status_code,
            404,
        )


class AssignmentPageTests(TestCase):
    """Страница задания обязана подключать редактор тренажёра.

    Текст `.trainer-input` прозрачный: его показывает слой подсветки, который создаёт
    скрипт. Без обвязки студент не видит собственный запрос — и тест на сервере этого
    не заметит, поэтому связка проверяется отдельно (см. core.tests.test_design).
    """

    def setUp(self):
        self.course, _ = f.course_with_lessons(lessons=1)
        self.task = f.assignment(self.course, auto=True)
        self.client.force_login(f.student())

    def test_autocheck_task_does_not_use_the_trainer_grid(self):
        response = self.client.get(reverse("assessments:assignment_detail", args=[self.task.pk]))
        self.assertContains(response, 'class="assignment-work"')
        self.assertNotContains(response, 'class="trainer"')

    def test_task_with_data_shows_its_tables(self):
        """Без таблиц условие решалось вслепую: не видно ни столбцов, ни данных."""
        task = f.assignment(self.course, auto=True, title="С данными")
        task.setup_sql = "CREATE TABLE t (id int);"
        task.save(update_fields=["setup_sql"])
        response = self.client.get(reverse("assessments:assignment_detail", args=[task.pk]))
        self.assertContains(response, 'id="task-tables"')

    def test_task_without_data_has_nothing_to_show(self):
        response = self.client.get(reverse("assessments:assignment_detail", args=[self.task.pk]))
        self.assertNotContains(response, 'id="task-tables"')


class SubmitWorkTests(TestCase):
    """Сдача работы, которую проверяет преподаватель: DDL, файл, текст."""

    def setUp(self):
        self.teacher = f.teacher()
        self.course, _ = f.course_with_lessons(author=self.teacher, lessons=1)
        self.student = f.student()
        f.enroll(self.student, self.course)
        self.task = f.assignment(self.course, auto=False, max_score=50)
        self.url = reverse("assessments:submit", args=[self.task.pk])
        self.page = reverse("assessments:assignment_detail", args=[self.task.pk])
        self.client.force_login(self.student)

    def upload(self, name, content):
        return SimpleUploadedFile(name, content, content_type="application/octet-stream")

    def test_form_is_shown_to_an_enrolled_student(self):
        self.assertContains(self.client.get(self.page), self.url)

    def test_sql_answer_goes_to_the_teachers_queue(self):
        response = self.client.post(self.url, {"answer": "CREATE TABLE t (id int);"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("submitted=1", response["Location"])

        work = Submission.objects.get()
        self.assertEqual(work.sql_query, "CREATE TABLE t (id int);")
        self.assertEqual(work.status, "submitted")
        self.assertIsNone(work.score)

        self.client.force_login(self.teacher)
        queue = self.client.get(reverse("teaching:submissions"))
        self.assertContains(queue, "CREATE TABLE t (id int);")

    def test_file_task_stores_the_answer_as_text(self):
        task = f.assignment(self.course, auto=False, type_override="file")
        self.client.post(
            reverse("assessments:submit", args=[task.pk]),
            {"upload": self.upload("project.sql", "CREATE TABLE п (id int);".encode())},
        )
        work = Submission.objects.get(assignment=task)
        self.assertEqual(work.text_answer, "CREATE TABLE п (id int);")
        self.assertIsNone(work.sql_query)

    def test_byte_order_mark_is_dropped_from_the_file(self):
        self.client.post(self.url, {"upload": self.upload("a.sql", b"\xef\xbb\xbfSELECT 1;")})
        self.assertEqual(Submission.objects.get().sql_query, "SELECT 1;")

    def test_empty_answer_is_rejected_and_explained(self):
        response = self.client.post(self.url, {"answer": "   "})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ответ пустой")
        self.assertFalse(Submission.objects.exists())

    def test_rejected_answer_keeps_the_typed_text(self):
        too_long = "x" * (MAX_ANSWER_CHARS + 1)
        response = self.client.post(self.url, {"answer": too_long})
        self.assertEqual(response.context["answer_text"], too_long)
        self.assertFalse(Submission.objects.exists())

    def test_bad_files_are_rejected(self):
        cases = [
            ("wrong extension", self.upload("work.pdf", b"%PDF-1.7"), "Подойдёт файл"),
            ("too large", self.upload("a.sql", b"x" * (MAX_UPLOAD_BYTES + 1)), "больше 1 МБ"),
            ("not utf-8", self.upload("a.sql", "выборка".encode("cp1251")), "UTF-8"),
            ("binary", self.upload("a.sql", b"SELECT\x00 1;"), "не похож на текстовый"),
        ]
        for label, upload, message in cases:
            with self.subTest(label):
                response = self.client.post(self.url, {"upload": upload})
                self.assertContains(response, message)
                self.assertFalse(Submission.objects.exists())

    def test_new_edition_replaces_the_previous_one(self):
        self.client.post(self.url, {"answer": "первая редакция"})
        self.client.post(self.url, {"answer": "вторая редакция"})
        self.assertEqual(Submission.objects.get().sql_query, "вторая редакция")

    def test_returned_work_can_be_resubmitted_and_loses_its_score(self):
        f.submission(self.task, self.student, status="returned", score=10, feedback="Доработать")
        self.client.post(self.url, {"answer": "исправлено"})

        work = Submission.objects.get()
        self.assertEqual(work.status, "submitted")
        self.assertIsNone(work.score)
        self.assertEqual(work.feedback, "Доработать")

    def test_graded_work_is_closed(self):
        f.submission(self.task, self.student, status="graded", score=40, sql_query="старое")
        self.assertNotContains(self.client.get(self.page), self.url)

        self.client.post(self.url, {"answer": "новое"})
        work = Submission.objects.get()
        self.assertEqual(work.sql_query, "старое")
        self.assertEqual(int(work.score), 40)

    def test_student_outside_the_course_cannot_submit(self):
        self.client.force_login(f.student())
        response = self.client.get(self.page)
        self.assertNotContains(response, self.url)
        self.assertContains(response, reverse("courses:enroll", args=[self.course.slug]))

        self.client.post(self.url, {"answer": "SELECT 1;"})
        self.assertFalse(Submission.objects.exists())

    def test_autocheck_task_is_not_submitted_this_way(self):
        auto = f.assignment(self.course, auto=True)
        self.client.post(reverse("assessments:submit", args=[auto.pk]), {"answer": "SELECT 1;"})
        self.assertFalse(Submission.objects.exists())

    def test_draft_course_task_is_hidden(self):
        draft = f.course(published=False)
        task = f.assignment(draft, auto=False)
        response = self.client.post(reverse("assessments:submit", args=[task.pk]), {"answer": "x"})
        self.assertEqual(response.status_code, 404)

    def test_guest_is_sent_to_login(self):
        self.client.logout()
        response = self.client.post(self.url, {"answer": "SELECT 1;"})
        self.assertIn("/login/", response["Location"])
        self.assertFalse(Submission.objects.exists())

    def test_get_is_rejected(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_submission_is_logged_without_xp(self):
        """Балла ещё нет, и XP за него начислять рано."""
        self.client.post(self.url, {"answer": "SELECT 1;"})
        self.student.refresh_from_db()
        self.assertEqual(self.student.xp, 0)
        self.assertTrue(self.student.activities.filter(type="submission").exists())

    def test_answer_is_included_in_the_personal_data_export(self):
        task = f.assignment(self.course, auto=False, type_override="file")
        self.client.post(reverse("assessments:submit", args=[task.pk]), {"answer": "мой проект"})
        data = json.loads(self.client.get(reverse("accounts:export_data")).content)
        self.assertEqual(data["решения_заданий"][0]["ответ"], "мой проект")


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

    def test_json_of_the_wrong_shape_is_rejected(self):
        """Корректный JSON — ещё не объект нужной формы, и 500 здесь не должно быть."""
        self.client.force_login(self.student)
        for body in (
            [],
            "строка",
            {"sql": 5, "columns": ["n"], "rows": [[1]]},
            {"sql": "SELECT 1;", "columns": "n", "rows": [[1]]},
            {"sql": "SELECT 1;", "columns": ["n"], "rows": 1},
            {"sql": "SELECT 1;", "columns": ["n"], "rows": [1]},
        ):
            with self.subTest(body=body):
                self.assertEqual(self.post(body).status_code, 400)
        self.assertFalse(Submission.objects.exists())

    def test_null_byte_in_the_query_is_dropped(self):
        """PostgreSQL не хранит нулевой байт в тексте: запись упала бы с ошибкой."""
        self.client.force_login(self.student)
        self.post({"sql": "SELECT\x00 1;", "columns": ["n"], "rows": [[1]]})
        self.assertEqual(Submission.objects.get().sql_query, "SELECT 1;")

    def test_error_report_of_the_wrong_shape_is_handled(self):
        self.client.force_login(self.student)
        url = reverse("assessments:report_error", args=[self.task.pk])
        self.assertEqual(
            self.client.post(url, "[]", content_type="application/json").status_code, 400
        )
        response = self.client.post(url, '{"error": ["x"]}', content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.student.activities.exists())

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
