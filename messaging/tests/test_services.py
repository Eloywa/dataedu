"""Правила переписки: кто кому вправе писать, тред, непрочитанное, диалоги."""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.tests import factories as f
from messaging import services
from messaging.models import Message


class WriteRulesTests(TestCase):
    def setUp(self):
        self.student = f.student()
        self.other_student = f.student()
        self.teacher = f.teacher()
        self.course = f.course(author=self.teacher)

    def test_student_can_write_to_teacher(self):
        self.assertIsNone(services.can_write(self.student, self.teacher))

    def test_teacher_can_write_to_student(self):
        self.assertIsNone(services.can_write(self.teacher, self.student))

    def test_student_to_student_is_forbidden(self):
        """Приватный обмен между студентами платформа не ведёт и не модерирует."""
        self.assertIsNotNone(services.can_write(self.student, self.other_student))

    def test_cannot_write_to_self(self):
        self.assertIsNotNone(services.can_write(self.student, self.student))

    def test_cannot_write_to_deactivated(self):
        self.teacher.is_active = False
        self.teacher.save(update_fields=["is_active"])
        self.assertIsNotNone(services.can_write(self.student, self.teacher))

    def test_admin_counts_as_teacher(self):
        self.assertIsNone(services.can_write(self.student, f.admin()))


class SendTests(TestCase):
    def setUp(self):
        self.student = f.student()
        self.teacher = f.teacher()
        self.course = f.course(author=self.teacher)

    def test_send_stores_trimmed_body(self):
        message, error = services.send_message(
            self.student, self.teacher, self.course, "  как быть с JOIN?  "
        )
        self.assertIsNone(error)
        self.assertEqual(message.body, "как быть с JOIN?")
        self.assertIsNone(message.read_at)

    def test_empty_body_rejected(self):
        message, error = services.send_message(self.student, self.teacher, self.course, "   \n ")
        self.assertIsNone(message)
        self.assertIsNotNone(error)
        self.assertEqual(Message.objects.count(), 0)

    def test_too_long_body_rejected(self):
        message, error = services.send_message(
            self.student, self.teacher, self.course, "я" * (services.MAX_BODY + 1)
        )
        self.assertIsNone(message)
        self.assertEqual(Message.objects.count(), 0)

    def test_body_at_limit_accepted(self):
        message, error = services.send_message(
            self.student, self.teacher, self.course, "я" * services.MAX_BODY
        )
        self.assertIsNone(error)
        self.assertIsNotNone(message)

    def test_forbidden_pair_writes_nothing(self):
        message, error = services.send_message(
            self.student, f.student(), self.course, "привет"
        )
        self.assertIsNone(message)
        self.assertEqual(Message.objects.count(), 0)


class ThreadTests(TestCase):
    def setUp(self):
        self.student = f.student()
        self.teacher = f.teacher()
        self.course = f.course(author=self.teacher)
        self.other_course = f.course(author=self.teacher)

    def test_thread_is_chronological(self):
        now = timezone.now()
        f.message(self.student, self.teacher, self.course, "второе", when=now)
        f.message(self.student, self.teacher, self.course, "первое", when=now - timedelta(hours=1))
        bodies = [m.body for m in services.thread(self.student, self.teacher, self.course)]
        self.assertEqual(bodies, ["первое", "второе"])

    def test_thread_includes_both_directions(self):
        f.message(self.student, self.teacher, self.course, "вопрос")
        f.message(self.teacher, self.student, self.course, "ответ")
        self.assertEqual(len(services.thread(self.student, self.teacher, self.course)), 2)

    def test_thread_is_scoped_to_course(self):
        """Один преподаватель может вести два предмета — треды не смешиваются."""
        f.message(self.student, self.teacher, self.course, "про первый")
        f.message(self.student, self.teacher, self.other_course, "про второй")
        bodies = [m.body for m in services.thread(self.student, self.teacher, self.course)]
        self.assertEqual(bodies, ["про первый"])

    def test_thread_hides_other_peoples_messages(self):
        stranger = f.student()
        f.message(stranger, self.teacher, self.course, "чужое")
        self.assertEqual(services.thread(self.student, self.teacher, self.course), [])

    def test_thread_keeps_latest_when_over_limit(self):
        now = timezone.now()
        for i in range(5):
            f.message(
                self.student, self.teacher, self.course, f"n{i}", when=now + timedelta(minutes=i)
            )
        got = services.thread(self.student, self.teacher, self.course, limit=3)
        self.assertEqual([m.body for m in got], ["n2", "n3", "n4"])


class UnreadTests(TestCase):
    def setUp(self):
        self.student = f.student()
        self.teacher = f.teacher()
        self.course = f.course(author=self.teacher)

    def test_counts_only_incoming_unread(self):
        f.message(self.student, self.teacher, self.course, "вопрос")
        f.message(self.teacher, self.student, self.course, "ответ")
        self.assertEqual(services.unread_count(self.teacher), 1)
        self.assertEqual(services.unread_count(self.student), 1)

    def test_reading_thread_clears_incoming_only(self):
        f.message(self.student, self.teacher, self.course, "вопрос")
        f.message(self.teacher, self.student, self.course, "ответ")
        services.mark_thread_read(self.teacher, self.student, self.course)
        self.assertEqual(services.unread_count(self.teacher), 0)
        # Своё сообщение прочитанным для собеседника не становится.
        self.assertEqual(services.unread_count(self.student), 1)

    def test_reading_does_not_touch_other_courses(self):
        other = f.course(author=self.teacher)
        f.message(self.student, self.teacher, self.course, "первый")
        f.message(self.student, self.teacher, other, "второй")
        services.mark_thread_read(self.teacher, self.student, self.course)
        self.assertEqual(services.unread_count(self.teacher), 1)


class ConversationsTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.first = f.student()
        self.second = f.student()
        self.course = f.course(author=self.teacher)
        self.other_course = f.course(author=self.teacher)

    def test_one_dialog_per_peer_and_course(self):
        f.message(self.first, self.teacher, self.course, "a")
        f.message(self.first, self.teacher, self.other_course, "b")
        f.message(self.second, self.teacher, self.course, "c")
        self.assertEqual(len(services.conversations(self.teacher)), 3)

    def test_shows_last_message_of_each_dialog(self):
        now = timezone.now()
        f.message(self.first, self.teacher, self.course, "старое", when=now - timedelta(days=1))
        f.message(self.teacher, self.first, self.course, "свежее", when=now)
        dialog = services.conversations(self.teacher)[0]
        self.assertEqual(dialog["last_body"], "свежее")
        self.assertEqual(dialog["peer"], self.first)
        self.assertEqual(dialog["course"], self.course)

    def test_unread_counted_per_dialog(self):
        f.message(self.first, self.teacher, self.course, "1")
        f.message(self.first, self.teacher, self.course, "2")
        f.message(self.second, self.teacher, self.course, "3", read=True)
        by_peer = {d["peer"].pk: d["unread"] for d in services.conversations(self.teacher)}
        self.assertEqual(by_peer[self.first.pk], 2)
        self.assertEqual(by_peer[self.second.pk], 0)

    def test_newest_dialog_first(self):
        now = timezone.now()
        f.message(self.first, self.teacher, self.course, "старый", when=now - timedelta(days=2))
        f.message(self.second, self.teacher, self.course, "новый", when=now)
        peers = [d["peer"].pk for d in services.conversations(self.teacher)]
        self.assertEqual(peers[0], self.second.pk)

    def test_messages_without_course_are_not_dialogs(self):
        """Диалог определяется курсом; сообщение без курса показывать негде."""
        f.message(self.first, self.teacher, None, "ничей")
        self.assertEqual(services.conversations(self.teacher), [])

    def test_query_count_does_not_grow_with_history(self):
        """Главное свойство: инбокс не вычитывает всю переписку ради двадцати строк."""
        now = timezone.now()
        for i in range(40):
            f.message(
                self.first, self.teacher, self.course, f"m{i}", when=now + timedelta(minutes=i)
            )
        with self.assertNumQueries(3):
            services.conversations(self.teacher)

    def test_empty_history_makes_no_extra_queries(self):
        with self.assertNumQueries(1):
            self.assertEqual(services.conversations(self.teacher), [])


class TeacherForTests(TestCase):
    def test_author_is_the_addressee(self):
        teacher = f.teacher()
        course = f.course(author=teacher)
        self.assertEqual(services.teacher_for(course), teacher)

    def test_course_without_author_has_nobody_to_write_to(self):
        self.assertIsNone(services.teacher_for(f.course(author=None)))

    def test_deactivated_author_is_not_addressee(self):
        teacher = f.teacher()
        course = f.course(author=teacher)
        teacher.is_active = False
        teacher.save(update_fields=["is_active"])
        course.refresh_from_db()
        self.assertIsNone(services.teacher_for(course))
