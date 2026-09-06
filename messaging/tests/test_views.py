"""Страницы переписки: доступ, отправка, живые эндпоинты."""

import json

from django.test import TestCase
from django.urls import reverse

from core.tests import factories as f
from messaging.models import Message


class InboxAccessTests(TestCase):
    def setUp(self):
        self.url = reverse("messaging:inbox")

    def test_guest_is_sent_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_student_sees_own_dialogs_only(self):
        teacher = f.teacher()
        course = f.course(author=teacher)
        me = f.student()
        stranger = f.student()
        f.message(me, teacher, course, "мой вопрос")
        f.message(stranger, teacher, course, "чужой вопрос")

        self.client.force_login(me)
        response = self.client.get(self.url)
        self.assertContains(response, "мой вопрос")
        self.assertNotContains(response, "чужой вопрос")

    def test_empty_inbox_renders(self):
        self.client.force_login(f.student())
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_opening_thread_marks_it_read(self):
        teacher = f.teacher()
        course = f.course(author=teacher)
        student = f.student()
        f.message(student, teacher, course, "вопрос")

        self.client.force_login(teacher)
        self.client.get(f"{self.url}?peer={student.pk}&course={course.pk}")
        self.assertEqual(Message.objects.filter(read_at__isnull=True).count(), 0)

    def test_broken_query_string_does_not_crash(self):
        self.client.force_login(f.student())
        response = self.client.get(f"{self.url}?peer=не-uuid&course=тоже")
        self.assertEqual(response.status_code, 200)


class SendTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course = f.course(author=self.teacher)
        self.student = f.student()
        self.url = reverse("messaging:send")

    def payload(self, **extra):
        data = {"peer": str(self.teacher.pk), "course": str(self.course.pk), "body": "вопрос"}
        data.update(extra)
        return data

    def test_student_sends_to_teacher(self):
        self.client.force_login(self.student)
        response = self.client.post(self.url, self.payload())
        self.assertEqual(response.status_code, 302)
        message = Message.objects.get()
        self.assertEqual(message.sender, self.student)
        self.assertEqual(message.recipient, self.teacher)
        self.assertEqual(message.course, self.course)

    def test_guest_cannot_send(self):
        response = self.client.post(self.url, self.payload())
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])
        self.assertEqual(Message.objects.count(), 0)

    def test_get_is_rejected(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_student_to_student_is_rejected(self):
        peer = f.student()
        self.client.force_login(self.student)
        response = self.client.post(self.url, self.payload(peer=str(peer.pk)))
        self.assertEqual(response.status_code, 302)
        self.assertIn("error=", response["Location"])
        self.assertEqual(Message.objects.count(), 0)

    def test_unknown_peer_gives_404(self):
        self.client.force_login(self.student)
        response = self.client.post(
            self.url, self.payload(peer="00000000-0000-0000-0000-000000000000")
        )
        self.assertEqual(response.status_code, 404)

    def test_returns_to_given_page(self):
        self.client.force_login(self.student)
        target = reverse("courses:course_detail", args=[self.course.slug])
        response = self.client.post(self.url, self.payload(next=target))
        self.assertTrue(response["Location"].startswith(target))

    def test_external_next_is_ignored(self):
        """`next` приходит из формы: чужой адрес там — открытый редирект."""
        self.client.force_login(self.student)
        response = self.client.post(self.url, self.payload(next="https://evil.example/steal"))
        self.assertNotIn("evil.example", response["Location"])
        self.assertIn(reverse("messaging:inbox"), response["Location"])


class ThreadJsonTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course = f.course(author=self.teacher)
        self.student = f.student()
        self.url = reverse("messaging:thread_json")

    def test_returns_thread_and_marks_read(self):
        f.message(self.student, self.teacher, self.course, "вопрос")
        self.client.force_login(self.teacher)
        response = self.client.get(
            self.url, {"peer": str(self.student.pk), "course": str(self.course.pk)}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["ok"])
        self.assertEqual(len(data["messages"]), 1)
        self.assertFalse(data["messages"][0]["mine"])
        self.assertEqual(Message.objects.filter(read_at__isnull=True).count(), 0)

    def test_stranger_sees_nothing_in_someone_elses_pair(self):
        """Подстановка чужой пары в строку запроса не открывает чужую переписку."""
        f.message(self.student, self.teacher, self.course, "секрет")
        outsider = f.student()
        self.client.force_login(outsider)
        response = self.client.get(
            self.url, {"peer": str(self.teacher.pk), "course": str(self.course.pk)}
        )
        self.assertEqual(json.loads(response.content)["messages"], [])

    def test_missing_arguments_give_400(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(self.url).status_code, 400)

    def test_guest_is_redirected(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class UnreadJsonTests(TestCase):
    def test_returns_current_count(self):
        teacher = f.teacher()
        course = f.course(author=teacher)
        student = f.student()
        f.message(student, teacher, course, "раз")
        f.message(student, teacher, course, "два")

        self.client.force_login(teacher)
        response = self.client.get(reverse("messaging:unread_json"))
        self.assertEqual(json.loads(response.content), {"unread": 2})


class HeaderBadgeTests(TestCase):
    def test_badge_shows_on_every_page(self):
        teacher = f.teacher()
        course = f.course(author=teacher)
        f.message(f.student(), teacher, course, "вопрос")

        self.client.force_login(teacher)
        response = self.client.get(reverse("courses:catalog"))
        self.assertEqual(response.context["unread_messages"], 1)

    def test_guest_costs_no_query(self):
        response = self.client.get(reverse("courses:catalog"))
        self.assertEqual(response.context["unread_messages"], 0)


class CourseWidgetTests(TestCase):
    """Виджет вопроса на странице курса."""

    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher)
        self.student = f.student()

    def url(self):
        return reverse("courses:course_detail", args=[self.course.slug])

    def test_enrolled_student_sees_widget(self):
        f.enroll(self.student, self.course)
        self.client.force_login(self.student)
        response = self.client.get(self.url())
        self.assertEqual(response.context["chat_peer"], self.teacher)

    def test_not_enrolled_student_has_no_widget(self):
        self.client.force_login(self.student)
        self.assertIsNone(self.client.get(self.url()).context["chat_peer"])

    def test_teacher_has_no_widget_on_own_course(self):
        f.enroll(self.teacher, self.course)
        self.client.force_login(self.teacher)
        self.assertIsNone(self.client.get(self.url()).context["chat_peer"])

    def test_widget_absent_when_course_has_no_author(self):
        orphan, _ = f.course_with_lessons(author=None)
        f.enroll(self.student, orphan)
        self.client.force_login(self.student)
        response = self.client.get(reverse("courses:course_detail", args=[orphan.slug]))
        self.assertIsNone(response.context["chat_peer"])

    def test_opening_course_marks_incoming_read(self):
        f.enroll(self.student, self.course)
        f.message(self.teacher, self.student, self.course, "ответ")
        self.client.force_login(self.student)
        self.client.get(self.url())
        self.assertEqual(Message.objects.filter(read_at__isnull=True).count(), 0)
