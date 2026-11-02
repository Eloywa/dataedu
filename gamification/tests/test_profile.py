"""Профиль: аватарка, значки достижений, курсы студента."""

import json
import re
from xml.etree import ElementTree

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from accounts.avatars import AVATARS, avatar_icon
from assessments.models import ProjectDraw, ProjectTopic
from core.tests import factories as f
from gamification.badges import BADGES, DEFAULT_BADGE, badge_for
from gamification.models import Achievement

URL = "gamification:profile"


class DrawingTests(SimpleTestCase):
    def drawings(self):
        yield from ((key, value[1]) for key, value in AVATARS.items())
        yield from BADGES.items()

    def test_every_drawing_is_valid_svg(self):
        """Незакрытый тег не даёт ошибки: страница просто теряет часть разметки."""
        for name, icon in self.drawings():
            with self.subTest(icon=name):
                ElementTree.fromstring(f"<svg>{icon}</svg>")

    def test_colour_comes_from_the_theme(self):
        for name, icon in self.drawings():
            with self.subTest(icon=name):
                self.assertIsNone(re.search(r"#[0-9a-fA-F]{3,8}|fill=|stroke=", icon))

    def test_unknown_badge_gets_the_common_one(self):
        """Преподаватель мог завести достижение с любым значком: дыры быть не должно."""
        self.assertEqual(badge_for("нет-такого"), BADGES[DEFAULT_BADGE])
        self.assertEqual(badge_for(None), BADGES[DEFAULT_BADGE])

    def test_unknown_avatar_means_a_letter(self):
        """Рисунок убрали из набора, а ключ остался в базе."""
        self.assertIsNone(avatar_icon("нет-такого"))
        self.assertIsNone(avatar_icon(""))


class ProfileFormTests(TestCase):
    def setUp(self):
        self.student = f.student(display_name="Было")
        self.client.force_login(self.student)
        self.url = reverse(URL)

    def post(self, **data):
        return self.client.post(self.url, data)

    def test_saves_name_and_avatar(self):
        response = self.post(display_name="  Стало  ", avatar="owl")
        self.assertRedirects(response, f"{self.url}?saved=1")
        self.student.refresh_from_db()
        self.assertEqual(self.student.display_name, "Стало")
        self.assertEqual(self.student.avatar, "owl")

    def test_avatar_and_name_can_be_removed(self):
        self.post(display_name="Стало", avatar="owl")
        self.post(display_name="", avatar="")
        self.student.refresh_from_db()
        self.assertEqual(self.student.avatar, "")
        self.assertEqual(self.student.label, self.student.username)

    def test_unknown_avatar_is_refused(self):
        """Значение приходит из браузера, а в шаблон потом подставляется разметка."""
        response = self.post(display_name="Стало", avatar="<script>")
        self.assertContains(response, "Такой аватарки нет")
        self.student.refresh_from_db()
        self.assertEqual(self.student.avatar, "")
        self.assertEqual(self.student.display_name, "Было")

    def test_too_long_name_is_refused(self):
        response = self.post(display_name="я" * 201, avatar="")
        self.assertContains(response, "Имя длиннее")
        self.student.refresh_from_db()
        self.assertEqual(self.student.display_name, "Было")

    def test_form_stays_open_on_error(self):
        """Иначе сообщение об ошибке оказалось бы внутри свёрнутого блока."""
        closed = self.client.get(self.url)
        self.assertContains(closed, '<details class="profile-edit">')
        self.assertContains(self.post(avatar="нет"), '<details class="profile-edit" open>')

    def test_changes_only_own_profile(self):
        other = f.student(display_name="Другой")
        self.post(display_name="Стало", avatar="fox")
        other.refresh_from_db()
        self.assertEqual((other.display_name, other.avatar), ("Другой", ""))

    def test_guest_cannot_save(self):
        self.client.logout()
        self.assertEqual(self.post(display_name="Гость", avatar="owl").status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.display_name, "Было")


class ProfilePageTests(TestCase):
    def setUp(self):
        self.student = f.student()
        self.client.force_login(self.student)
        self.url = reverse(URL)

    def test_header_shows_the_avatar_and_leads_to_the_profile(self):
        self.student.avatar = "owl"
        self.student.save()
        html = self.client.get(reverse("core:trainer")).content.decode("utf-8")
        self.assertIn(AVATARS["owl"][1], html)
        self.assertIn(f'class="link-muted header-user" href="{self.url}"', html)

    def test_letter_without_avatar(self):
        self.student.display_name = "дмитрий"
        self.student.save()
        html = self.client.get(self.url).content.decode("utf-8")
        self.assertRegex(html, r'class="avatar avatar-lg" aria-hidden="true">Д<')

    def test_every_avatar_is_offered(self):
        html = self.client.get(self.url).content.decode("utf-8")
        for key, (label, icon) in AVATARS.items():
            with self.subTest(avatar=key):
                self.assertIn(f'value="{key}"', html)
                self.assertIn(label, html)
                self.assertIn(icon, html)

    def test_achievement_shows_its_drawn_badge(self):
        Achievement.objects.create(code="flagged", title="Первый шаг", icon="flag", xp_reward=20)
        self.assertContains(self.client.get(self.url), BADGES["flag"])

    def test_earned_achievement_differs_from_locked(self):
        f.achievement("got", title="Получено")
        f.achievement("wait", title="Ждёт")
        f.award(self.student, "got")
        html = self.client.get(self.url).content.decode("utf-8")
        self.assertEqual(html.count('class="ach earned"'), 1)
        self.assertEqual(html.count('class="ach"'), 1)
        self.assertIn("пока не получено", html)

    def test_course_shows_progress_and_ticket(self):
        course, lessons = f.course_with_lessons(lessons=2)
        f.enroll(self.student, course)
        f.complete(self.student, lessons[0])
        topic = ProjectTopic.objects.create(course=course, title="Школьная библиотека")
        ProjectDraw.objects.create(user=self.student, course=course, topic=topic)

        response = self.client.get(self.url)
        self.assertEqual(response.context["courses"][0]["pct"], 50)
        self.assertContains(response, "1 из 2")
        self.assertContains(response, "Школьная библиотека")

    def test_progress_counts_only_this_student(self):
        course, lessons = f.course_with_lessons(lessons=2)
        f.enroll(self.student, course)
        f.complete(f.student(), lessons[0])
        self.assertEqual(self.client.get(self.url).context["courses"][0]["done"], 0)

    def test_certificate_appears_when_the_course_is_finished(self):
        course, lessons = f.course_with_lessons(lessons=1)
        f.enroll(self.student, course)
        certificate = reverse("courses:certificate", args=[course.slug])
        self.assertNotContains(self.client.get(self.url), certificate)
        f.complete(self.student, lessons[0])
        self.assertContains(self.client.get(self.url), certificate)

    def test_no_courses_leads_to_the_catalog(self):
        self.assertContains(self.client.get(self.url), "Вы пока не записаны на курсы")


class AvatarElsewhereTests(TestCase):
    def setUp(self):
        self.student = f.student(avatar="fox")

    def test_teacher_sees_the_avatar_on_the_student_card(self):
        teacher = f.teacher()
        course, _ = f.course_with_lessons(author=teacher, lessons=1)
        f.enroll(self.student, course)
        self.client.force_login(teacher)
        response = self.client.get(reverse("teaching:student", args=[self.student.pk]))
        self.assertContains(response, AVATARS["fox"][1])

    def test_data_export_includes_the_avatar(self):
        self.client.force_login(self.student)
        data = json.loads(self.client.get(reverse("accounts:export_data")).content)
        self.assertEqual(data["учётная_запись"]["аватарка"], "fox")
