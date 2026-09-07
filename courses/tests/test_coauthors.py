"""Соавторство курса.

Соавтор получает те же права на курс, что и автор: правит содержание в админке
и видит курс в отчётах. Автор при этом остаётся один — он числится за курсом в
каталоге и ему уходят вопросы студентов.

Это изменение модели доступа, поэтому проверяется не только то, что соавтор
что-то может, но и то, что посторонний преподаватель по-прежнему не может
ничего. Правило записано в одном месте — `Course.is_authored_by`; здесь
проверяются все дороги, которые к нему ведут.
"""

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from core.tests import factories as f
from courses.models import Course
from learning import reports
from messaging.services import teacher_for


def staff(user):
    """Преподаватель в админке: права на объекты выдаёт группа «Преподаватели»,
    здесь достаточно выдать их напрямую."""
    user.is_staff = True
    user.save(update_fields=["is_staff"])
    user.user_permissions.add(*Permission.objects.filter(content_type__app_label="courses"))
    return user


class RuleTests(TestCase):
    def setUp(self):
        self.author = f.teacher()
        self.mate = f.teacher()
        self.stranger = f.teacher()
        self.course = f.course(author=self.author)
        self.course.coauthors.add(self.mate)

    def test_author_and_coauthor_own_the_course(self):
        self.assertTrue(self.course.is_authored_by(self.author))
        self.assertTrue(self.course.is_authored_by(self.mate))

    def test_stranger_does_not(self):
        self.assertFalse(self.course.is_authored_by(self.stranger))

    def test_student_does_not(self):
        self.assertFalse(self.course.is_authored_by(f.student()))

    def test_queryset_matches_the_rule(self):
        mine = Course.objects.authored_by(self.mate)
        self.assertEqual(list(mine), [self.course])
        self.assertEqual(list(Course.objects.authored_by(self.stranger)), [])

    def test_several_coauthors_do_not_duplicate_the_course(self):
        """Соединение с таблицей соавторов задваивает строки — отсюда distinct."""
        self.course.coauthors.add(f.teacher(), f.teacher())
        self.assertEqual(Course.objects.authored_by(self.author).count(), 1)

    def test_superuser_sees_everything(self):
        boss = f.admin()
        boss.is_superuser = True
        boss.save(update_fields=["is_superuser"])
        f.course(author=self.stranger)
        self.assertEqual(Course.objects.authored_by(boss).count(), Course.objects.count())


class ReportTests(TestCase):
    def setUp(self):
        self.author = f.teacher()
        self.mate = f.teacher()
        self.stranger = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.author)
        self.course.coauthors.add(self.mate)

    def test_coauthor_sees_the_course_in_reports(self):
        self.assertIn(self.course, reports.visible_courses(self.mate))

    def test_stranger_does_not(self):
        self.assertNotIn(self.course, reports.visible_courses(self.stranger))

    def test_coauthor_sees_the_students(self):
        """Смысл соавторства — доступ к аналитике, а она идёт через студентов курса."""
        student = f.student()
        f.enroll(student, self.course)
        rows = reports.student_rows(self.mate)
        self.assertEqual([r["user"] for r in rows], [student])

    def test_coauthor_list_has_no_duplicates(self):
        self.course.coauthors.add(f.teacher())
        titles = [c.title for c in reports.visible_courses(self.mate)]
        self.assertEqual(len(titles), len(set(titles)))


class AdminTests(TestCase):
    def setUp(self):
        self.author = staff(f.teacher())
        self.mate = staff(f.teacher())
        self.stranger = staff(f.teacher())
        self.course, self.lessons = f.course_with_lessons(author=self.author)
        self.course.coauthors.add(self.mate)

    def open_course(self, user):
        self.client.force_login(user)
        return self.client.get(reverse("admin:courses_course_change", args=[self.course.pk]))

    def test_coauthor_can_open_the_course(self):
        self.assertEqual(self.open_course(self.mate).status_code, 200)

    def test_stranger_cannot(self):
        self.assertIn(self.open_course(self.stranger).status_code, (302, 403))

    def test_coauthor_sees_the_course_in_the_list(self):
        self.client.force_login(self.mate)
        html = self.client.get(reverse("admin:courses_course_changelist")).content.decode()
        self.assertIn(self.course.title, html)

    def test_stranger_sees_an_empty_list(self):
        self.client.force_login(self.stranger)
        html = self.client.get(reverse("admin:courses_course_changelist")).content.decode()
        self.assertNotIn(self.course.title, html)

    def test_coauthor_reaches_nested_objects(self):
        """Урок лежит через модуль: проверяется составной путь до курса."""
        lesson = self.lessons[0]
        self.mate.user_permissions.add(
            *Permission.objects.filter(content_type__app_label="courses")
        )
        self.client.force_login(self.mate)
        response = self.client.get(reverse("admin:courses_lesson_change", args=[lesson.pk]))
        self.assertEqual(response.status_code, 200)

    def test_stranger_does_not_reach_nested_objects(self):
        lesson = self.lessons[0]
        self.client.force_login(self.stranger)
        response = self.client.get(reverse("admin:courses_lesson_change", args=[lesson.pk]))
        self.assertIn(response.status_code, (302, 403))


class MessagingTests(TestCase):
    def test_author_gets_the_questions(self):
        author = f.teacher()
        course = f.course(author=author)
        course.coauthors.add(f.teacher())
        self.assertEqual(teacher_for(course), author)

    def test_coauthor_takes_over_when_there_is_no_author(self):
        """Курс может остаться без автора — вопрос студента не должен пропасть."""
        mate = f.teacher()
        course = f.course(author=None)
        course.coauthors.add(mate)
        self.assertEqual(teacher_for(course), mate)

    def test_nobody_to_write_to(self):
        self.assertIsNone(teacher_for(f.course(author=None)))
