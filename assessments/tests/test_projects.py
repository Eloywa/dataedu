"""Билеты итогового проекта: кто может тянуть, как выбирается тема, что видит преподаватель."""

import json
import random
import sqlite3
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import models
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from assessments import projects
from assessments.management.commands.seed_course_content import FINAL_DESCRIPTION, TASKS, TOPICS
from assessments.management.commands.seed_practice import SETUP
from assessments.models import Assignment, ProjectDraw, ProjectTopic, Submission
from core.tests import factories as f
from courses.models import Course
from learning import reports
from learning.models import StudyGroup


def topic(course, title=None, **extra):
    return ProjectTopic.objects.create(
        course=course,
        title=title or f"Тема {ProjectTopic.objects.count() + 1}",
        description="Описание темы.",
        **extra,
    )


class Base(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher, lessons=1, modules=2)
        self.final = f.assignment(self.course, auto=False, is_final=True, type_override="file")
        self.student = f.student()
        f.enroll(self.student, self.course)
        self.detail = reverse("assessments:assignment_detail", args=[self.final.pk])
        self.draw_url = reverse("assessments:draw_ticket", args=[self.final.pk])
        self.client.force_login(self.student)


class DrawTests(Base):
    def test_student_gets_a_ticket(self):
        only = topic(self.course)
        response = self.client.post(self.draw_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("drawn=1", response["Location"])
        self.assertEqual(ProjectDraw.objects.get(user=self.student).topic, only)

    def test_second_draw_changes_nothing(self):
        topic(self.course), topic(self.course)
        self.client.post(self.draw_url)
        first = ProjectDraw.objects.get(user=self.student).topic
        for _ in range(5):
            self.client.post(self.draw_url)
        self.assertEqual(ProjectDraw.objects.filter(user=self.student).count(), 1)
        self.assertEqual(ProjectDraw.objects.get(user=self.student).topic, first)

    def test_draw_needs_post(self):
        topic(self.course)
        self.assertEqual(self.client.get(self.draw_url).status_code, 405)
        self.assertFalse(ProjectDraw.objects.exists())

    def test_guest_is_sent_to_login(self):
        topic(self.course)
        self.client.logout()
        self.assertIn("/login/", self.client.post(self.draw_url)["Location"])
        self.assertFalse(ProjectDraw.objects.exists())

    def test_student_outside_the_course_cannot_draw(self):
        topic(self.course)
        self.client.force_login(f.student())
        self.client.post(self.draw_url)
        self.assertFalse(ProjectDraw.objects.exists())

    def test_teacher_does_not_draw(self):
        topic(self.course)
        self.client.force_login(self.teacher)
        self.client.post(self.draw_url)
        self.assertFalse(ProjectDraw.objects.exists())

    def test_ordinary_task_has_no_tickets(self):
        topic(self.course)
        task = f.assignment(self.course, self.lessons[0])
        self.client.post(reverse("assessments:draw_ticket", args=[task.pk]))
        self.assertFalse(ProjectDraw.objects.exists())

    def test_retired_topic_does_not_come_up(self):
        topic(self.course, title="Снятая", is_active=False)
        kept = topic(self.course, title="В наборе")
        self.client.post(self.draw_url)
        self.assertEqual(ProjectDraw.objects.get(user=self.student).topic, kept)

    def test_simultaneous_draw_returns_the_one_ticket(self):
        """Вторая вкладка успела между проверкой и записью: билет всё равно один."""
        chosen = topic(self.course)
        real_pick = projects.pick_topic

        def other_tab_wins(course, user, rng=None):
            picked = real_pick(course, user, rng=rng)
            ProjectDraw.objects.create(user=user, course=course, topic=picked)
            return picked

        with mock.patch.object(projects, "pick_topic", side_effect=other_tab_wins):
            result = projects.draw_ticket(self.student, self.final)

        self.assertEqual(result.topic, chosen)
        self.assertEqual(ProjectDraw.objects.filter(user=self.student).count(), 1)


class FairnessTests(Base):
    def students_in_group(self, count, group=None):
        result = []
        for _ in range(count):
            person = f.student()
            f.enroll(person, self.course)
            if group:
                group.students.add(person)
            result.append(person)
        return result

    def test_no_repeats_until_every_topic_is_taken(self):
        for _ in range(4):
            topic(self.course)
        titles = [
            projects.draw_ticket(person, self.final).topic.title
            for person in self.students_in_group(4)
        ]
        self.assertEqual(len(set(titles)), 4)

    def test_repeats_stay_even(self):
        for _ in range(3):
            topic(self.course)
        counts = {}
        for person in self.students_in_group(7):
            title = projects.draw_ticket(person, self.final).topic.title
            counts[title] = counts.get(title, 0) + 1
        self.assertEqual(sorted(counts.values()), [2, 2, 3])

    def test_choice_is_random_among_the_rarest(self):
        for _ in range(5):
            topic(self.course)
        seen = {
            projects.pick_topic(self.course, self.student, rng=random.Random(seed)).pk
            for seed in range(40)
        }
        self.assertGreater(len(seen), 1)

    def test_balance_is_counted_inside_the_students_group(self):
        """Тема, занятая в чужой группе, в своей ещё считается свободной."""
        first, second = topic(self.course, title="Первая"), topic(self.course, title="Вторая")
        mine = StudyGroup.objects.create(name="ПИ-1", teacher=self.teacher)
        other = StudyGroup.objects.create(name="ПИ-2", teacher=self.teacher)
        mine.students.add(self.student)
        for person in self.students_in_group(3, group=other):
            ProjectDraw.objects.create(user=person, course=self.course, topic=first)
        neighbour = self.students_in_group(1, group=mine)[0]
        ProjectDraw.objects.create(user=neighbour, course=self.course, topic=second)

        self.assertEqual(projects.pick_topic(self.course, self.student), first)

    def test_student_in_two_groups_is_counted_once(self):
        first, second = topic(self.course, title="Первая"), topic(self.course, title="Вторая")
        group_a = StudyGroup.objects.create(name="А", teacher=self.teacher)
        group_b = StudyGroup.objects.create(name="Б", teacher=self.teacher)
        group_a.students.add(self.student)
        group_b.students.add(self.student)
        both = self.students_in_group(1, group=group_a)[0]
        group_b.students.add(both)
        ProjectDraw.objects.create(user=both, course=self.course, topic=first)
        single = self.students_in_group(1, group=group_a)[0]
        ProjectDraw.objects.create(user=single, course=self.course, topic=second)

        # По одному билету на тему: выбор должен идти из обеих, а не только из второй.
        seen = {
            projects.pick_topic(self.course, self.student, rng=random.Random(seed)).pk
            for seed in range(30)
        }
        self.assertEqual(seen, {first.pk, second.pk})

    def test_no_active_topics_means_no_ticket(self):
        topic(self.course, is_active=False)
        self.assertIsNone(projects.draw_ticket(self.student, self.final))


class OpeningTests(Base):
    def setUp(self):
        super().setUp()
        topic(self.course)
        self.first_block = self.course.modules.order_by("order_index").first()
        Assignment.objects.filter(pk=self.final.pk).update(opens_after=self.first_block)

    def test_closed_until_the_block_is_passed(self):
        response = self.client.get(self.detail)
        self.assertContains(response, "Билет пока закрыт")
        self.assertContains(response, self.first_block.title)
        self.client.post(self.draw_url)
        self.assertFalse(ProjectDraw.objects.exists())

    def test_opens_after_the_block(self):
        f.complete(self.student, self.lessons[0])
        self.assertContains(self.client.get(self.detail), "Вытянуть билет")
        self.client.post(self.draw_url)
        self.assertTrue(ProjectDraw.objects.filter(user=self.student).exists())

    def test_block_without_lessons_does_not_lock_forever(self):
        empty = f.module(self.course, order_index=9, title="Пустой блок")
        Assignment.objects.filter(pk=self.final.pk).update(opens_after=empty)
        self.assertContains(self.client.get(self.detail), "Вытянуть билет")


class SubmissionRulesTests(Base):
    def post_work(self):
        return self.client.post(
            reverse("assessments:submit", args=[self.final.pk]),
            {"answer": "CREATE TABLE t (id int);"},
        )

    def test_work_waits_for_a_ticket(self):
        topic(self.course)
        self.post_work()
        self.assertFalse(Submission.objects.exists())

    def test_work_is_accepted_after_the_draw(self):
        topic(self.course)
        self.client.post(self.draw_url)
        self.post_work()
        self.assertTrue(Submission.objects.filter(user=self.student).exists())

    def test_without_topics_final_works_as_before(self):
        self.post_work()
        self.assertTrue(Submission.objects.filter(user=self.student).exists())
        self.assertNotContains(self.client.get(self.detail), "Вытянуть билет")

    def test_work_sent_before_tickets_is_left_alone(self):
        f.submission(self.final, self.student)
        topic(self.course)
        response = self.client.get(self.detail)
        self.assertNotContains(response, "Вытянуть билет")
        self.client.post(self.draw_url)
        self.assertFalse(ProjectDraw.objects.exists())
        self.post_work()
        self.assertEqual(Submission.objects.filter(user=self.student).count(), 1)


class PageTests(Base):
    def test_topics_are_hidden_before_the_draw(self):
        """Иначе студент выбирал бы удобную тему и знал, чего ждать."""
        topic(self.course, title="Секретная тема")
        response = self.client.get(self.detail)
        self.assertContains(response, "Вытянуть билет")
        self.assertNotContains(response, "Секретная тема")

    def test_ticket_is_shown_after_the_draw(self):
        topic(self.course, title="Выпавшая тема")
        response = self.client.post(self.draw_url, follow=True)
        self.assertContains(response, "Выпавшая тема")
        self.assertContains(response, "is-new")
        self.assertNotContains(self.client.get(self.detail), "is-new")

    def test_student_sees_why_the_ticket_was_replaced(self):
        topic(self.course)
        self.client.post(self.draw_url)
        ProjectDraw.objects.update(note="Тема совпала с курсовой")
        self.assertContains(self.client.get(self.detail), "Тема совпала с курсовой")

    def test_course_page_shows_the_ticket(self):
        topic(self.course, title="Выпавшая тема")
        self.client.post(self.draw_url)
        response = self.client.get(reverse("courses:course_detail", args=[self.course.slug]))
        self.assertContains(response, "Итоговый проект")
        self.assertContains(response, "Выпавшая тема")

    def test_guest_can_open_the_course_page(self):
        topic(self.course)
        self.client.logout()
        response = self.client.get(reverse("courses:course_detail", args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)

    def test_list_shows_the_ticket(self):
        topic(self.course, title="Выпавшая тема")
        self.client.post(self.draw_url)
        self.assertContains(self.client.get(reverse("assessments:practice")), "Выпавшая тема")

    def test_teacher_sees_the_pool_size_and_not_the_button(self):
        topic(self.course), topic(self.course)
        self.client.force_login(self.teacher)
        response = self.client.get(self.detail)
        self.assertContains(response, "В наборе 2 темы")
        self.assertNotContains(response, "Вытянуть билет")

    def test_data_export_includes_the_ticket(self):
        topic(self.course, title="Выпавшая тема")
        self.client.post(self.draw_url)
        response = self.client.get(reverse("accounts:export_data"))
        data = json.loads(response.content)
        self.assertEqual(data["билеты_итогового_проекта"][0]["тема"], "Выпавшая тема")


class TeacherSideTests(Base):
    def setUp(self):
        super().setUp()
        self.topic = topic(self.course, title="Выпавшая тема")
        self.client.post(self.draw_url)
        self.client.force_login(self.teacher)

    def test_student_card_shows_the_ticket(self):
        response = self.client.get(reverse("teaching:student", args=[self.student.pk]))
        self.assertContains(response, "Выпавшая тема")

    def test_review_queue_shows_the_ticket(self):
        f.submission(self.final, self.student, text_answer="работа")
        self.assertContains(
            self.client.get(reverse("teaching:submissions")), "Билет: Выпавшая тема"
        )

    def test_defence_goes_to_the_course_of_the_ticket(self):
        """Прежде зачёт ложился на первое попавшееся итоговое задание преподавателя."""
        other_course, _ = f.course_with_lessons(author=self.teacher, lessons=1)
        f.assignment(other_course, auto=False, is_final=True)
        self.assertEqual(reports.final_assignment_for(self.teacher, self.student), self.final)

    def test_defence_ignores_courses_the_student_did_not_take(self):
        other_course, _ = f.course_with_lessons(author=self.teacher, lessons=1)
        Assignment.objects.filter(pk=self.final.pk).update(is_final=False)
        f.assignment(other_course, auto=False, is_final=True)
        self.assertIsNone(reports.final_assignment_for(self.teacher, self.student))

    def test_teacher_can_replace_the_ticket(self):
        replacement = topic(self.course, title="Замена")
        draw = ProjectDraw.objects.get(user=self.student)
        call_command("setup_teacher_admin", verbosity=0, stdout=mock.Mock())
        self.teacher.refresh_from_db()
        response = self.client.post(
            reverse("admin:assessments_projectdraw_change", args=[draw.pk]),
            {"topic": replacement.pk, "note": "Болел на момент жребия"},
        )
        self.assertEqual(response.status_code, 302)
        draw.refresh_from_db()
        self.assertEqual(draw.topic, replacement)
        self.assertEqual(draw.changed_by, self.teacher)

    def test_topic_from_another_course_is_rejected(self):
        other_course, _ = f.course_with_lessons(lessons=1)
        draw = ProjectDraw.objects.get(user=self.student)
        draw.topic = topic(other_course)
        with self.assertRaises(ValidationError):
            draw.clean()

    def test_drawn_topic_cannot_be_deleted(self):
        with self.assertRaises(models.ProtectedError):
            self.topic.delete()


class SeedCourseContentTests(TestCase):
    def setUp(self):
        self.course = f.course(slug="databases-for-teachers")
        block = f.module(self.course, order_index=7, title="Связывание таблиц (JOIN)")
        for index, task in enumerate(TASKS):
            f.lesson(block, order_index=index, title=task["lesson"])
        self.final = f.assignment(self.course, auto=False, is_final=True)

    def test_creates_tasks_topics_and_opening(self):
        call_command("seed_course_content", verbosity=0)
        self.final.refresh_from_db()
        self.assertEqual(self.course.project_topics.count(), len(TOPICS))
        self.assertEqual(self.course.assignments.filter(is_final=False).count(), len(TASKS))
        self.assertEqual(self.final.opens_after.title, "Связывание таблиц (JOIN)")
        self.assertEqual(self.final.description, FINAL_DESCRIPTION)
        for task in self.course.assignments.filter(is_final=False):
            with self.subTest(task=task.title):
                self.assertTrue(task.is_autocheckable)
                self.assertIsNotNone(task.lesson)

    def test_running_twice_changes_nothing(self):
        call_command("seed_course_content", verbosity=0)
        call_command("seed_course_content", verbosity=0)
        self.assertEqual(self.course.project_topics.count(), len(TOPICS))
        self.assertEqual(self.course.assignments.filter(is_final=False).count(), len(TASKS))

    def test_missing_course_does_not_fail(self):
        Course.objects.all().delete()
        call_command("seed_course_content", verbosity=0, stderr=mock.Mock())


class SeedContentIntegrityTests(SimpleTestCase):
    """Эталоны вписаны в код: проверяем, что они совпадают с результатом самих запросов.

    Здесь SQLite, а у студента PostgreSQL, но запросы простые и работают одинаково. Значения
    посчитаны в PGlite, а этот тест ловит расхождение при правке запроса или данных.
    """

    def run_task(self, task):
        db = sqlite3.connect(":memory:")
        self.addCleanup(db.close)
        db.executescript(SETUP + task.get("extra_setup", ""))
        statements = [s for s in task["expected_sql"].split(";") if s.strip()]
        for statement in statements[:-1]:
            db.execute(statement)
        return [list(row) for row in db.execute(statements[-1]).fetchall()]

    def test_expected_results_match_the_queries(self):
        for task in TASKS:
            with self.subTest(task=task["title"]):
                expected = sorted(task["expected_result"]["rows"], key=str)
                self.assertEqual(sorted(self.run_task(task), key=str), expected)

    def test_every_topic_has_three_questions(self):
        for title, _area, _entities, questions in TOPICS:
            with self.subTest(topic=title):
                self.assertEqual(len(questions), 3)

    def test_task_data_matches_the_trainer_dataset(self):
        """Данные заданий совпадают с набором «Университет» из тренажёра."""
        scripts = Path(settings.BASE_DIR) / "static" / "js" / "sql" / "datasets.js"
        text = scripts.read_text(encoding="utf-8")
        for name in ("Анна Соколова", "ПИ-101", "Иванов И. И."):
            self.assertIn(name, SETUP)
            self.assertIn(name, text)
