"""Вход, регистрация, настройки и правовой контур учётной записи."""

import json

from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.legal import VERSIONS
from accounts.models import Consent, User
from core.tests import factories as f


class LoginTests(TestCase):
    def setUp(self):
        self.user = f.student(username="ivanov")
        self.url = reverse("accounts:login")

    def test_login_by_username(self):
        response = self.client.post(self.url, {"username": "ivanov", "password": f.PASSWORD})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session["_auth_user_id"] is not None), 1)

    def test_wrong_password_keeps_guest(self):
        response = self.client.post(self.url, {"username": "ivanov", "password": "неверно"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["error"])
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_error_message_does_not_reveal_existing_logins(self):
        """Разные тексты для «нет такого» и «пароль не тот» позволяют перебирать логины."""
        missing = self.client.post(self.url, {"username": "нетакого", "password": "x"})
        wrong = self.client.post(self.url, {"username": "ivanov", "password": "x"})
        self.assertEqual(missing.context["error"], wrong.context["error"])

    def test_deactivated_account_cannot_log_in(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        self.client.post(self.url, {"username": "ivanov", "password": f.PASSWORD})
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logged_in_user_is_redirected_away(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_logout_needs_post(self):
        self.client.force_login(self.user)
        self.client.get(reverse("accounts:logout"))
        self.assertIn("_auth_user_id", self.client.session)

        self.client.post(reverse("accounts:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)


class RegisterTests(TestCase):
    def setUp(self):
        f.role("student", "Студент")
        self.url = reverse("accounts:register")

    def form(self, **extra):
        data = {
            "username": "novichok",
            "password": "dlinnyi-parol",
            "confirm": "dlinnyi-parol",
            "consent": "on",
        }
        data.update(extra)
        return data

    def test_registration_creates_student_with_consents(self):
        response = self.client.post(self.url, self.form())
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username="novichok")
        self.assertEqual(user.role.code, "student")
        self.assertEqual(
            set(Consent.objects.filter(user=user).values_list("document", flat=True)),
            set(VERSIONS),
        )

    def test_consent_records_the_document_version(self):
        self.client.post(self.url, self.form())
        consent = Consent.objects.filter(document="privacy").get()
        self.assertEqual(consent.version, VERSIONS["privacy"])

    def test_without_consent_no_account_is_created(self):
        response = self.client.post(self.url, self.form(consent=""))
        self.assertIsNotNone(response.context["error"])
        self.assertFalse(User.objects.filter(username="novichok").exists())

    def test_short_password_is_rejected(self):
        self.client.post(self.url, self.form(password="korot", confirm="korot"))
        self.assertFalse(User.objects.filter(username="novichok").exists())

    def test_mismatched_passwords_are_rejected(self):
        self.client.post(self.url, self.form(confirm="другое"))
        self.assertFalse(User.objects.filter(username="novichok").exists())

    def test_cyrillic_login_is_rejected(self):
        self.client.post(self.url, self.form(username="иванов"))
        self.assertFalse(User.objects.filter(username="иванов").exists())

    def test_taken_login_is_rejected(self):
        f.student(username="zanyat")
        self.client.post(self.url, self.form(username="zanyat"))
        self.assertEqual(User.objects.filter(username="zanyat").count(), 1)

    def test_email_is_optional(self):
        self.client.post(self.url, self.form())
        self.assertIsNone(User.objects.get(username="novichok").email)

    def test_taken_email_is_rejected(self):
        f.student(username="pervyi", email="one@example.org")
        self.client.post(self.url, self.form(email="one@example.org"))
        self.assertFalse(User.objects.filter(username="novichok").exists())

    @override_settings(REGISTRATION_OPEN=False)
    def test_closed_registration_returns_403(self):
        """На апробации логины выдаются пачкой, свободная регистрация закрыта."""
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.client.post(self.url, self.form())
        self.assertFalse(User.objects.filter(username="novichok").exists())


class SettingsTests(TestCase):
    def setUp(self):
        self.user = f.student()
        self.url = reverse("accounts:settings")
        self.client.force_login(self.user)

    def test_password_change(self):
        response = self.client.post(
            self.url,
            {"current": f.PASSWORD, "new": "novyi-parol-9", "confirm": "novyi-parol-9"},
        )
        self.assertTrue(response.context["done"])
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("novyi-parol-9"))

    def test_change_does_not_log_out(self):
        self.client.post(
            self.url,
            {"current": f.PASSWORD, "new": "novyi-parol-9", "confirm": "novyi-parol-9"},
        )
        self.assertIn("_auth_user_id", self.client.session)

    def test_wrong_current_password_blocks_change(self):
        response = self.client.post(
            self.url, {"current": "неверно", "new": "novyi-parol-9", "confirm": "novyi-parol-9"}
        )
        self.assertIsNotNone(response.context["error"])
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(f.PASSWORD))

    def test_same_password_is_rejected(self):
        response = self.client.post(
            self.url, {"current": f.PASSWORD, "new": f.PASSWORD, "confirm": f.PASSWORD}
        )
        self.assertIsNotNone(response.context["error"])

    def test_guest_cannot_open_settings(self):
        self.client.logout()
        self.assertEqual(self.client.get(self.url).status_code, 302)


class DataRightsTests(TestCase):
    """Права субъекта данных: доступ к своим данным и прекращение обработки."""

    def setUp(self):
        self.user = f.student(username="ivanov", display_name="Иванов")
        self.course, self.lessons = f.course_with_lessons(lessons=1)
        f.enroll(self.user, self.course)
        f.complete(self.user, self.lessons[0])
        self.client.force_login(self.user)

    def test_export_returns_own_data_as_json(self):
        response = self.client.get(reverse("accounts:export_data"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response["Content-Disposition"])

        payload = json.loads(response.content)
        self.assertEqual(payload["учётная_запись"]["логин"], "ivanov")
        self.assertEqual(len(payload["записи_на_курсы"]), 1)

    def test_export_never_contains_the_password_hash(self):
        response = self.client.get(reverse("accounts:export_data"))
        self.assertNotIn(self.user.password, response.content.decode("utf-8"))

    def test_deletion_requires_password_and_the_word(self):
        url = reverse("accounts:delete_account")

        self.client.post(url, {"password": "неверно", "confirm": "УДАЛИТЬ"})
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

        self.client.post(url, {"password": f.PASSWORD, "confirm": "удалить"})
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

        self.client.post(url, {"password": f.PASSWORD, "confirm": "УДАЛИТЬ"})
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_deletion_removes_learning_records(self):
        from learning.models import Enrollment, LessonProgress

        self.client.post(
            reverse("accounts:delete_account"),
            {"password": f.PASSWORD, "confirm": "УДАЛИТЬ"},
        )
        self.assertFalse(Enrollment.objects.exists())
        self.assertFalse(LessonProgress.objects.exists())

    def test_deletion_keeps_the_authored_course(self):
        """Иначе удаление преподавателя снесло бы материал у всех студентов."""
        teacher = f.teacher()
        course = f.course(author=teacher)
        self.client.force_login(teacher)
        self.client.post(
            reverse("accounts:delete_account"),
            {"password": f.PASSWORD, "confirm": "УДАЛИТЬ"},
        )
        course.refresh_from_db()
        self.assertIsNone(course.author)


class UserModelTests(TestCase):
    def test_label_falls_back_to_login(self):
        self.assertEqual(f.student(username="ivanov").label, "ivanov")
        self.assertEqual(f.student(display_name="Иванов И.").label, "Иванов И.")

    def test_role_flags(self):
        self.assertTrue(f.teacher().is_teacher)
        self.assertTrue(f.admin().is_teacher)
        self.assertTrue(f.admin().is_admin)
        self.assertFalse(f.student().is_teacher)

    def test_user_without_role_is_not_a_teacher(self):
        user = User.objects.create_user(username="bezroli", password=f.PASSWORD)
        self.assertFalse(user.is_teacher)

    def test_login_is_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", password=f.PASSWORD)
