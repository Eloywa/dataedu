"""Приём эталона, посчитанного в браузере преподавателя.

Эталон приходит из браузера, а не считается на сервере: студент выполняет запрос
в PGlite, и эталон, посчитанный другим движком, может с ним разойтись на мелочах.
Но раз значение приходит извне, доверять ему на слово нельзя — проверяется и право
на конкретное задание, и форма самих данных.
"""

import json

from django.test import TestCase
from django.urls import reverse

from assessments.expected import ExpectedError, compute_expected
from assessments.models import Assignment
from core.tests import factories as f


class SaveExpectedTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.teacher.is_superuser = True  # доступ в админку
        self.teacher.save(update_fields=["is_superuser"])
        self.course, _ = f.course_with_lessons(author=self.teacher)
        self.task = f.assignment(self.course, auto=False)
        self.task.type = "sql"
        self.task.expected_result = None
        self.task.save(update_fields=["type", "expected_result"])
        self.url = reverse("admin:assessments_assignment_save_expected", args=[self.task.pk])

    def post(self, payload, user=None):
        self.client.force_login(user or self.teacher)
        return self.client.post(self.url, json.dumps(payload), content_type="application/json")

    def test_reference_is_saved(self):
        response = self.post({"columns": ["n"], "rows": [[1], [2]]})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])

        self.task.refresh_from_db()
        self.assertEqual(self.task.expected_result, {"columns": ["n"], "rows": [[1], [2]]})
        self.assertTrue(self.task.is_autocheckable)

    def test_empty_result_is_allowed(self):
        """Запрос может честно вернуть ноль строк — это корректный эталон."""
        response = self.post({"columns": ["n"], "rows": []})
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.expected_result["rows"], [])

    def test_result_without_columns_is_rejected(self):
        """Без столбцов сравнивать нечего — так выглядит запрос, который не SELECT."""
        response = self.post({"columns": [], "rows": []})
        self.assertEqual(response.status_code, 400)
        self.task.refresh_from_db()
        self.assertIsNone(self.task.expected_result)

    def test_ragged_rows_are_rejected(self):
        response = self.post({"columns": ["a", "b"], "rows": [[1, 2], [3]]})
        self.assertEqual(response.status_code, 400)

    def test_broken_json_is_rejected(self):
        self.client.force_login(self.teacher)
        response = self.client.post(self.url, "не json", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_is_rejected(self):
        self.client.force_login(self.teacher)
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_student_cannot_save(self):
        response = self.post({"columns": ["n"], "rows": [[1]]}, user=f.student())
        self.assertIn(response.status_code, (302, 403, 404))
        self.task.refresh_from_db()
        self.assertIsNone(self.task.expected_result)

    def test_other_teacher_cannot_save(self):
        """Изоляция авторства: подстановка чужого идентификатора не проходит."""
        stranger = f.teacher()
        stranger.is_staff = True
        stranger.save(update_fields=["is_staff"])
        response = self.post({"columns": ["n"], "rows": [[1]]}, user=stranger)
        self.assertIn(response.status_code, (302, 403, 404))
        self.task.refresh_from_db()
        self.assertIsNone(self.task.expected_result)


class ServerSideComputationTests(TestCase):
    def test_non_postgres_says_what_to_do(self):
        """На файловой базе серверный расчёт невозможен — но сообщать об этом надо
        по-человечески, а не ошибкой подключения к сокету, из которой человек
        решит, что у него не запущен сервер БД."""
        from django.db import connection

        if connection.vendor == "postgresql":
            self.skipTest("прогон идёт на PostgreSQL — серверный расчёт доступен")

        task = f.assignment(f.course(), auto=False)
        task.setup_sql = "CREATE TABLE t (n int);"
        task.expected_sql = "SELECT n FROM t;"

        with self.assertRaises(ExpectedError) as caught:
            compute_expected(task)
        self.assertIn("PostgreSQL", str(caught.exception))
        self.assertIn("браузере", str(caught.exception))


class SeededTasksTests(TestCase):
    """Демо-задания должны работать сразу после наполнения, без ручных шагов."""

    def test_seed_creates_autocheckable_tasks(self):
        from django.core.management import call_command

        f.course(slug="sql-s-nulya")
        call_command("seed_practice", verbosity=0)

        tasks = Assignment.objects.filter(type="sql")
        self.assertGreaterEqual(tasks.count(), 4)
        for task in tasks:
            with self.subTest(task=task.title):
                self.assertTrue(task.is_autocheckable, "эталон не задан")
                self.assertTrue(task.setup_sql.strip(), "нет заготовки данных")
                self.assertTrue(task.expected_result["columns"], "эталон без столбцов")

    def test_seed_is_repeatable(self):
        from django.core.management import call_command

        f.course(slug="sql-s-nulya")
        call_command("seed_practice", verbosity=0)
        first = Assignment.objects.count()
        call_command("seed_practice", verbosity=0)
        self.assertEqual(Assignment.objects.count(), first, "повторный запуск задвоил задания")
