"""Выборки отчётов: изоляция авторства, правильность агрегатов, число запросов.

Проверка числа запросов (`assertNumQueries`) здесь не украшение: без неё возврат
запроса внутрь цикла проходит незаметно — отчёт остаётся правильным, просто
перестаёт открываться на большом потоке.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.tests import factories as f
from learning import reports


class VisibilityTests(TestCase):
    def setUp(self):
        self.mine = f.teacher()
        self.theirs = f.teacher()
        self.my_course = f.course(author=self.mine)
        self.their_course = f.course(author=self.theirs)

    def test_teacher_sees_only_own_courses(self):
        self.assertEqual(list(reports.visible_courses(self.mine)), [self.my_course])

    def test_superuser_sees_everything(self):
        visible = set(reports.visible_courses(f.admin()))
        self.assertIn(self.my_course, visible)
        self.assertIn(self.their_course, visible)

    def test_groups_are_isolated_too(self):
        mine = f.group(self.mine)
        f.group(self.theirs)
        self.assertEqual(list(reports.visible_groups(self.mine)), [mine])


class StudentRowsTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher, lessons=4)
        self.student = f.student()
        f.enroll(self.student, self.course)

    def test_completion_is_share_of_finished_lessons(self):
        f.complete(self.student, self.lessons[0])
        f.complete(self.student, self.lessons[1])
        row = reports.student_rows(self.teacher)[0]
        self.assertEqual(row["lessons_done"], 2)
        self.assertEqual(row["lessons_total"], 4)
        self.assertEqual(row["completion"], 50)

    def test_lesson_in_progress_does_not_count(self):
        f.complete(self.student, self.lessons[0], status="in_progress")
        self.assertEqual(reports.student_rows(self.teacher)[0]["lessons_done"], 0)

    def test_average_score_is_across_attempts(self):
        test = f.test_for(self.lessons[0])
        f.attempt(self.student, test, score=100)
        f.attempt(self.student, test, score=50)
        self.assertEqual(reports.student_rows(self.teacher)[0]["avg_score"], 75)

    def test_no_attempts_gives_no_average(self):
        self.assertIsNone(reports.student_rows(self.teacher)[0]["avg_score"])

    def test_days_inactive_from_last_event(self):
        f.activity(self.student, "login", when=timezone.now() - timedelta(days=5))
        self.assertEqual(reports.student_rows(self.teacher)[0]["days_inactive"], 5)

    def test_riskiest_first(self):
        lazy = f.student()
        f.enroll(lazy, self.course)
        f.complete_course(self.student, self.lessons)
        f.activity(self.student, "login")

        rows = reports.student_rows(self.teacher)
        self.assertEqual(rows[0]["user"], lazy)
        self.assertGreater(rows[0]["risk"], rows[1]["risk"])

    def test_other_teachers_students_are_invisible(self):
        other = f.teacher()
        other_course, _ = f.course_with_lessons(author=other)
        f.enroll(f.student(), other_course)
        self.assertEqual(len(reports.student_rows(self.teacher)), 1)

    def test_course_filter_narrows_rows(self):
        second, _ = f.course_with_lessons(author=self.teacher)
        f.enroll(self.student, second)
        self.assertEqual(len(reports.student_rows(self.teacher)), 2)
        self.assertEqual(len(reports.student_rows(self.teacher, second)), 1)

    def test_teacher_without_courses_gets_empty(self):
        self.assertEqual(reports.student_rows(f.teacher()), [])

    def test_query_count_is_flat(self):
        """Двадцать студентов должны стоить столько же запросов, сколько один.

        Шесть запросов: курсы, записи, уроки по курсам, пройденное, баллы, активность.
        Число зафиксировано намеренно — если оно вырастет, значит запрос вернулся
        внутрь цикла, и отчёт перестанет открываться на реальном потоке.
        """
        with self.assertNumQueries(6):
            reports.student_rows(self.teacher)

        for _ in range(20):
            person = f.student()
            f.enroll(person, self.course)
            f.complete(person, self.lessons[0])
            f.activity(person, "login")

        with self.assertNumQueries(6):
            rows = reports.student_rows(self.teacher)
        self.assertEqual(len(rows), 21)


class SummaryTests(TestCase):
    def test_empty_summary_is_zeroed(self):
        summary = reports.summarize([])
        self.assertEqual(summary["total"], 0)
        self.assertEqual(summary["avg_completion"], 0)

    def test_zones_are_counted(self):
        rows = [
            {"completion": 100, "risk": 10, "zone": {"tone": "success"}},
            {"completion": 50, "risk": 50, "zone": {"tone": "warning"}},
            {"completion": 0, "risk": 90, "zone": {"tone": "danger"}},
        ]
        summary = reports.summarize(rows)
        self.assertEqual((summary["low"], summary["medium"], summary["high"]), (1, 1, 1))
        self.assertEqual(summary["avg_completion"], 50)


class DifficultyRowsTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher, lessons=2)
        self.student = f.student()
        f.enroll(self.student, self.course)

    def test_lesson_without_reflection_is_skipped(self):
        """Сравнивать не с чем: субъективной оценки нет."""
        f.attempt(self.student, f.test_for(self.lessons[0]), score=50)
        self.assertEqual(reports.lesson_difficulty_rows(self.teacher), [])

    def test_lesson_with_reflection_appears(self):
        f.reflection(self.student, self.lessons[0], clarity=4, difficulty=5)
        f.attempt(self.student, f.test_for(self.lessons[0]), score=40)
        rows = reports.lesson_difficulty_rows(self.teacher)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["lesson"], self.lessons[0])
        self.assertEqual(rows[0]["n_reflections"], 1)
        self.assertIsNotNone(rows[0]["objective"])
        self.assertIsNotNone(rows[0]["subjective"])

    def test_biggest_divergence_comes_first(self):
        second_student = f.student()
        # Урок 0: объективно трудный, субъективно лёгкий — большое расхождение.
        f.reflection(self.student, self.lessons[0], difficulty=1)
        f.attempt(self.student, f.test_for(self.lessons[0]), score=10)
        # Урок 1: и объективно, и субъективно средний.
        f.reflection(second_student, self.lessons[1], difficulty=3)
        f.attempt(second_student, f.test_for(self.lessons[1]), score=50)

        rows = reports.lesson_difficulty_rows(self.teacher)
        self.assertEqual(rows[0]["lesson"], self.lessons[0])

    def test_query_count_is_flat(self):
        for lesson in self.lessons:
            f.reflection(f.student(), lesson)
            f.attempt(f.student(), f.test_for(lesson), score=70)
        with self.assertNumQueries(5):
            reports.lesson_difficulty_rows(self.teacher)


class ManualQueueTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher)
        self.student = f.student()

    def test_only_non_autocheckable_tasks_are_queued(self):
        auto = f.assignment(self.course, auto=True)
        manual = f.assignment(self.course, auto=False)
        f.submission(auto, self.student)
        mine = f.submission(manual, self.student)

        queue = reports.manual_queue(self.teacher)
        self.assertEqual(queue, [mine])

    def test_graded_work_leaves_the_queue(self):
        manual = f.assignment(self.course, auto=False)
        f.submission(manual, self.student, status="graded", score=90)
        self.assertEqual(reports.manual_queue(self.teacher), [])

    def test_other_teachers_queue_is_invisible(self):
        other_course, _ = f.course_with_lessons(author=f.teacher())
        f.submission(f.assignment(other_course, auto=False), self.student)
        self.assertEqual(reports.manual_queue(self.teacher), [])

    def test_queue_orm_filter_matches_the_property(self):
        """Условие в базе и свойство модели обязаны совпадать (см. AssignmentQuerySet)."""
        from assessments.models import Assignment

        f.assignment(self.course, auto=True)
        f.assignment(self.course, auto=False)
        Assignment.objects.create(
            course=self.course, title="SQL без эталона", level="basic",
            type="sql", expected_result=None, max_score=10,
        )

        by_orm = set(Assignment.objects.manual().values_list("id", flat=True))
        by_property = {a.id for a in Assignment.objects.all() if not a.is_autocheckable}
        self.assertEqual(by_orm, by_property)


class GradebookTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher, lessons=2)
        self.student = f.student()
        f.enroll(self.student, self.course)

    def test_best_attempt_counts_not_the_average(self):
        """Пересдача существует ровно для того, чтобы улучшить отметку."""
        test = f.test_for(self.lessons[0])
        f.attempt(self.student, test, score=20, passed=False)
        f.attempt(self.student, test, score=90, passed=True)
        row = reports.gradebook_rows(self.course)[0]
        self.assertEqual(row["tests_pct"], 90)

    def test_untaken_test_pulls_the_mark_down(self):
        """Знаменатель — все тесты курса, иначе «сдал один» равнялось бы «сдал все»."""
        first = f.test_for(self.lessons[0])
        f.test_for(self.lessons[1])
        f.attempt(self.student, first, score=100, passed=True)
        row = reports.gradebook_rows(self.course)[0]
        self.assertEqual(row["tests_pct"], 50)

    def test_pending_work_counts_as_zero_and_is_shown(self):
        task = f.assignment(self.course, max_score=100)
        f.submission(task, self.student, status="submitted")
        row = reports.gradebook_rows(self.course)[0]
        self.assertEqual(row["pending"], 1)
        self.assertEqual(row["assignments_done"], 0)

    def test_course_without_anything_gradable_has_no_mark(self):
        empty = f.course(author=self.teacher)
        f.enroll(self.student, empty)
        row = reports.gradebook_rows(empty)[0]
        self.assertIsNone(row["score"])
        self.assertIsNone(row["grade"]["mark"])

    def test_full_completion_gives_top_mark(self):
        test = f.test_for(self.lessons[0])
        f.attempt(self.student, test, score=100, passed=True)
        f.complete_course(self.student, self.lessons)
        task = f.assignment(self.course, max_score=100)
        f.submission(task, self.student, status="graded", score=100)

        row = reports.gradebook_rows(self.course)[0]
        self.assertEqual(row["score"], 100)
        self.assertEqual(row["grade"]["mark"], 5)
        self.assertTrue(row["verdict"]["passed"])

    def test_group_narrows_to_its_members(self):
        outsider = f.student()
        f.enroll(outsider, self.course)
        group = f.group(self.teacher, students=[self.student])

        self.assertEqual(len(reports.gradebook_rows(self.course)), 2)
        rows = reports.gradebook_rows(self.course, group)
        self.assertEqual([r["user"] for r in rows], [self.student])

    def test_group_member_not_enrolled_is_not_in_the_sheet(self):
        """В ведомость попадает пересечение состава группы и записанных на курс."""
        stranger = f.student()
        group = f.group(self.teacher, students=[self.student, stranger])
        rows = reports.gradebook_rows(self.course, group)
        self.assertEqual([r["user"] for r in rows], [self.student])

    def test_summary_counts_marks(self):
        f.complete_course(self.student, self.lessons)
        rows = reports.gradebook_rows(self.course)
        summary = reports.gradebook_summary(rows)
        self.assertEqual(summary["total"], 1)
        self.assertIsNotNone(summary["avg_score"])


class ItemAnalysisTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher, lessons=1)
        self.test = f.test_for(self.lessons[0])
        self.student = f.student()

    def test_share_of_correct_answers(self):
        question, right, wrong = f.question(self.test)
        attempt = f.attempt(self.student, self.test)
        f.answer(attempt, question, right, is_correct=True)
        f.answer(attempt, question, wrong, is_correct=False)

        rows = reports.item_analysis_rows(self.teacher)
        self.assertEqual(rows[0]["responses"], 2)
        self.assertEqual(rows[0]["pct_correct"], 50)

    def test_unanswered_questions_are_skipped(self):
        f.question(self.test)
        self.assertEqual(reports.item_analysis_rows(self.teacher), [])

    def test_hardest_first(self):
        easy, easy_right, _ = f.question(self.test, order_index=0)
        hard, _, hard_wrong = f.question(self.test, order_index=1)
        attempt = f.attempt(self.student, self.test)
        f.answer(attempt, easy, easy_right, is_correct=True)
        f.answer(attempt, hard, hard_wrong, is_correct=False)

        rows = reports.item_analysis_rows(self.teacher)
        self.assertEqual(rows[0]["question"], hard)


class TopicMasteryTests(TestCase):
    def test_untagged_questions_are_counted_separately(self):
        teacher = f.teacher()
        course, lessons = f.course_with_lessons(author=teacher, lessons=1)
        test = f.test_for(lessons[0])
        topic = f.topic()
        tagged, right, _ = f.question(test, order_index=0, topic_obj=topic)
        f.question(test, order_index=1)

        attempt = f.attempt(f.student(), test)
        f.answer(attempt, tagged, right, is_correct=True)

        rows, stats = reports.topic_mastery_rows(teacher)
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["untagged"], 1)
        self.assertEqual(rows[0]["topic_name"], topic.name)
        self.assertEqual(rows[0]["pct_correct"], 100)
