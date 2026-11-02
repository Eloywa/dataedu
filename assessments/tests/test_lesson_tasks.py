"""Задания внутри курса: переход с урока, раскладка по блокам и замок закрытой недели."""

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from assessments.models import Submission
from assessments.tasks import task_states
from core.tests import factories as f


class LessonPageTests(TestCase):
    def setUp(self):
        self.course, self.lessons = f.course_with_lessons(lessons=2)
        self.student = f.student()
        f.enroll(self.student, self.course)
        self.url = reverse("courses:lesson_detail", args=[self.lessons[0].pk])

    def test_lesson_links_to_its_task(self):
        task = f.assignment(self.course, self.lessons[0], title="Задание к этому уроку")
        response = self.client.get(self.url)
        self.assertContains(response, "Задание к этому уроку")
        self.assertContains(response, reverse("assessments:assignment_detail", args=[task.pk]))

    def test_task_of_another_lesson_is_not_shown(self):
        f.assignment(self.course, self.lessons[1], title="Задание другого урока")
        self.assertNotContains(self.client.get(self.url), "Задание другого урока")

    def test_final_project_is_not_a_lesson_task(self):
        f.assignment(self.course, self.lessons[0], is_final=True, title="Итоговый проект X")
        self.assertEqual(self.client.get(self.url).context["lesson_tasks"], [])

    def test_lesson_shows_how_the_task_went(self):
        task = f.assignment(self.course, self.lessons[0])
        f.submission(task, self.student, status="graded", score=10)
        self.client.force_login(self.student)
        self.assertContains(self.client.get(self.url), "решено")

    def test_course_page_marks_lessons_with_tasks(self):
        f.assignment(self.course, self.lessons[0])
        response = self.client.get(reverse("courses:course_detail", args=[self.course.slug]))
        self.assertContains(response, "lesson-task-tag", count=1)


class TaskPageTests(TestCase):
    def setUp(self):
        self.course, self.lessons = f.course_with_lessons(lessons=2)
        self.student = f.student()
        f.enroll(self.student, self.course)
        self.client.force_login(self.student)

    def test_task_leads_back_to_lesson_and_on_to_the_next(self):
        task = f.assignment(self.course, self.lessons[0])
        response = self.client.get(reverse("assessments:assignment_detail", args=[task.pk]))
        self.assertContains(response, reverse("courses:lesson_detail", args=[self.lessons[0].pk]))
        self.assertEqual(response.context["next_lesson"], self.lessons[1])

    def test_last_lesson_has_no_next(self):
        task = f.assignment(self.course, self.lessons[1])
        response = self.client.get(reverse("assessments:assignment_detail", args=[task.pk]))
        self.assertIsNone(response.context["next_lesson"])

    def test_task_without_lesson_leads_to_the_list(self):
        task = f.assignment(self.course)
        response = self.client.get(reverse("assessments:assignment_detail", args=[task.pk]))
        self.assertContains(response, "← Задания")


class TaskCourseValidationTests(TestCase):
    def test_lesson_must_be_from_the_same_course(self):
        course, _ = f.course_with_lessons(lessons=1)
        _, foreign = f.course_with_lessons(lessons=1)
        task = f.assignment(course, foreign[0])
        with self.assertRaises(ValidationError):
            task.clean()

    def test_opening_block_must_be_from_the_same_course(self):
        course, _ = f.course_with_lessons(lessons=1)
        other, _ = f.course_with_lessons(lessons=1)
        task = f.assignment(course, is_final=True, opens_after=other.modules.first())
        with self.assertRaises(ValidationError):
            task.clean()


class LockedWeekTests(TestCase):
    """Задание закрытой недели нельзя ни открыть, ни сдать в обход экрана «урок закрыт»."""

    def setUp(self):
        self.course, self.lessons = f.course_with_lessons(lessons=1, modules=2)
        self.student = f.student()
        f.enroll(self.student, self.course)
        self.auto = f.assignment(self.course, self.lessons[1], auto=True)
        self.manual = f.assignment(self.course, self.lessons[1], auto=False)
        self.client.force_login(self.student)

    def detail(self, task):
        return self.client.get(reverse("assessments:assignment_detail", args=[task.pk]))

    def test_task_page_is_closed(self):
        response = self.detail(self.auto)
        self.assertTemplateUsed(response, "lessons/lesson_locked.html")
        self.assertContains(response, "Задание пока закрыто")

    def test_check_is_refused(self):
        response = self.client.post(
            reverse("assessments:check", args=[self.auto.pk]),
            data={"sql": "SELECT 1 AS n", "columns": ["n"], "rows": [[1]]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Submission.objects.exists())

    def test_work_is_not_accepted(self):
        response = self.client.post(
            reverse("assessments:submit", args=[self.manual.pk]),
            {"answer": "CREATE TABLE t (id int);"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Submission.objects.exists())

    def test_opens_after_previous_week(self):
        f.complete(self.student, self.lessons[0])
        self.assertTemplateUsed(self.detail(self.auto), "assessments/assignment_detail.html")

    def test_teacher_is_not_locked_out(self):
        self.client.force_login(f.teacher())
        self.assertTemplateUsed(self.detail(self.auto), "assessments/assignment_detail.html")

    def test_list_shows_locked_task_without_a_link(self):
        response = self.client.get(reverse("assessments:practice"))
        self.assertContains(response, self.auto.title)
        self.assertContains(response, "закрыто")
        self.assertNotContains(
            response, reverse("assessments:assignment_detail", args=[self.auto.pk])
        )


class PracticeGroupingTests(TestCase):
    def test_tasks_are_laid_out_by_block_and_lesson(self):
        course, lessons = f.course_with_lessons(lessons=2, modules=2)
        late = f.assignment(course, lessons[2])
        early = f.assignment(course, lessons[0])
        loose = f.assignment(course)
        final = f.assignment(course, auto=False, is_final=True)

        self.client.force_login(f.student())
        group = self.client.get(reverse("assessments:practice")).context["groups"][0]

        self.assertEqual(
            [block["module"].order_index for block in group["blocks"]], [0, 1], "порядок блоков"
        )
        self.assertEqual(group["blocks"][0]["lessons"][0]["tasks"], [early])
        self.assertEqual(group["blocks"][1]["lessons"][0]["tasks"], [late])
        self.assertEqual(group["loose"], [loose])
        self.assertEqual(group["finals"], [final])


class TaskStateTests(TestCase):
    def setUp(self):
        self.course, _ = f.course_with_lessons(lessons=1)
        self.student = f.student()

    def state(self, task):
        return task_states(self.student, [task]).get(task.id)

    def test_no_submission_means_no_state(self):
        self.assertIsNone(self.state(f.assignment(self.course)))

    def test_failed_attempt_after_success_stays_solved(self):
        task = f.assignment(self.course, auto=True)
        f.submission(task, self.student, status="graded", score=10)
        f.submission(task, self.student, status="graded", score=0)
        self.assertEqual(self.state(task)["label"], "решено")

    def test_failed_attempt(self):
        task = f.assignment(self.course, auto=True)
        f.submission(task, self.student, status="graded", score=0)
        self.assertEqual(self.state(task)["label"], "не решено")

    def test_manual_work_in_review_and_returned(self):
        task = f.assignment(self.course, auto=False)
        f.submission(task, self.student, status="submitted")
        self.assertEqual(self.state(task)["label"], "на проверке")
        f.submission(task, self.student, status="returned")
        self.assertEqual(self.state(task)["label"], "на доработке")

    def test_graded_manual_work(self):
        task = f.assignment(self.course, auto=False)
        f.submission(task, self.student, status="graded", score=80)
        self.assertEqual(self.state(task)["label"], "оценено")
