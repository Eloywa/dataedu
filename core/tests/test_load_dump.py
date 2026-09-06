"""Загрузка содержимого из дампа первой версии.

Команда — единственный способ получить работающую платформу на чистой машине,
поэтому проверяется и разбор формата, и повторяемость запуска.
"""

from django.core.management import call_command
from django.test import TestCase

from accounts.models import User
from core.management.commands.load_dump import parse_dump, unescape
from courses.models import Course, Lesson, Module
from learning.models import Enrollment

DUMP = """--
-- PostgreSQL database dump
--

COPY public.roles (id, code, name, description) FROM stdin;
11111111-1111-1111-1111-111111111111\tstudent\tСтудент\t\\N
22222222-2222-2222-2222-222222222222\tteacher\tПреподаватель\tВедёт курсы
\\.

COPY public.users (id, email, password_hash, full_name, role_id, avatar_url, xp, level, is_active, last_seen_at, created_at, updated_at) FROM stdin;
aaaaaaaa-0000-0000-0000-000000000001\tanna@stud.ru\tscrypt$xxx\tАнна\t11111111-1111-1111-1111-111111111111\t\\N\t120\t3\tt\t\\N\t2026-01-01 10:00:00+03\t2026-01-01 10:00:00+03
aaaaaaaa-0000-0000-0000-000000000002\tanna@other.ru\tscrypt$yyy\tАнна вторая\t11111111-1111-1111-1111-111111111111\t\\N\t0\t1\tt\t\\N\t2026-01-02 10:00:00+03\t2026-01-02 10:00:00+03
bbbbbbbb-0000-0000-0000-000000000001\tpetrova@dataedu.ru\tscrypt$zzz\tПетрова\t22222222-2222-2222-2222-222222222222\t\\N\t0\t1\tt\t\\N\t2026-01-01 10:00:00+03\t2026-01-01 10:00:00+03
\\.

COPY public.courses (id, title, slug, description, semester, author_id, is_published, created_at, level, cover_url) FROM stdin;
cccccccc-0000-0000-0000-000000000001\tОсновы SQL\tosnovy-sql\tПервый курс\t1\tbbbbbbbb-0000-0000-0000-000000000001\tt\t2026-01-01 10:00:00+03\tbasic\t\\N
\\.

COPY public.modules (id, course_id, title, description, order_index, week_number) FROM stdin;
dddddddd-0000-0000-0000-000000000001\tcccccccc-0000-0000-0000-000000000001\tНеделя 1\t\\N\t0\t1
\\.

COPY public.lessons (id, module_id, title, theory_content, order_index, est_minutes, xp_reward) FROM stdin;
eeeeeeee-0000-0000-0000-000000000001\tdddddddd-0000-0000-0000-000000000001\tSELECT\tСтрока\\nвторая строка\t0\t20\t10
\\.

COPY public.enrollments (id, user_id, course_id, status, enrolled_at, completed_at) FROM stdin;
ffffffff-0000-0000-0000-000000000001\taaaaaaaa-0000-0000-0000-000000000001\tcccccccc-0000-0000-0000-000000000001\tactive\t2026-01-05 10:00:00+03\t\\N
\\.
"""


class UnescapeTests(TestCase):
    def test_null_marker(self):
        self.assertIsNone(unescape("\\N"))

    def test_newline_and_tab(self):
        self.assertEqual(unescape("a\\nb\\tc"), "a\nb\tc")

    def test_double_backslash_stays_a_backslash(self):
        """Порядок раскрытия важен: иначе `\\\\n` стал бы переводом строки."""
        self.assertEqual(unescape("C:\\\\nowhere"), "C:\\nowhere")

    def test_plain_text_is_untouched(self):
        self.assertEqual(unescape("обычный текст"), "обычный текст")


class ParseDumpTests(TestCase):
    def test_all_copy_blocks_are_found(self):
        tables = parse_dump(DUMP)
        self.assertEqual(
            set(tables), {"roles", "users", "courses", "modules", "lessons", "enrollments"}
        )

    def test_columns_and_rows_are_parsed(self):
        columns, rows = parse_dump(DUMP)["roles"]
        self.assertEqual(columns, ["id", "code", "name", "description"])
        self.assertEqual(len(rows), 2)
        self.assertIsNone(rows[0][3])

    def test_text_with_newlines_survives(self):
        _, rows = parse_dump(DUMP)["lessons"]
        self.assertIn("\n", rows[0][3])

    def test_file_without_copy_blocks_gives_nothing(self):
        self.assertEqual(parse_dump("-- пусто\nCREATE TABLE x (id int);"), {})


class LoadDumpTests(TestCase):
    def setUp(self, path=None):
        self.path = self._write(DUMP)

    def _write(self, text):
        import tempfile
        from pathlib import Path

        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".sql", delete=False, encoding="utf-8"
        )
        handle.write(text)
        handle.close()
        return Path(handle.name)

    def test_content_is_loaded(self):
        call_command("load_dump", path=str(self.path), verbosity=0)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Module.objects.count(), 1)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_login_is_derived_from_email(self):
        call_command("load_dump", path=str(self.path), verbosity=0)
        self.assertTrue(User.objects.filter(username="anna").exists())

    def test_colliding_logins_get_a_suffix(self):
        """`anna@stud.ru` и `anna@other.ru` дают «anna» и «anna2»."""
        call_command("load_dump", path=str(self.path), verbosity=0)
        self.assertTrue(User.objects.filter(username="anna2").exists())

    def test_passwords_are_not_carried_over(self):
        """Хеши scrypt из Next-версии Django не понимает — пароль неустановлен."""
        call_command("load_dump", path=str(self.path), verbosity=0)
        self.assertFalse(User.objects.get(username="anna").has_usable_password())

    def test_teachers_get_admin_access(self):
        call_command("load_dump", path=str(self.path), verbosity=0)
        self.assertTrue(User.objects.get(username="petrova").is_staff)
        self.assertFalse(User.objects.get(username="anna").is_staff)

    def test_relations_are_preserved(self):
        call_command("load_dump", path=str(self.path), verbosity=0)
        lesson = Lesson.objects.get()
        self.assertEqual(lesson.module.course.slug, "osnovy-sql")
        self.assertEqual(lesson.module.course.author.username, "petrova")

    def test_multiline_theory_survives_the_load(self):
        call_command("load_dump", path=str(self.path), verbosity=0)
        self.assertIn("\n", Lesson.objects.get().theory_content)

    def test_second_run_does_not_duplicate(self):
        """Развёртывание часто повторяют — команда обязана быть повторяемой."""
        call_command("load_dump", path=str(self.path), verbosity=0)
        call_command("load_dump", path=str(self.path), verbosity=0)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(User.objects.count(), 3)

    def test_missing_file_is_reported(self):
        from django.core.management.base import CommandError

        with self.assertRaises(CommandError):
            call_command("load_dump", path="нет-такого-файла.sql", verbosity=0)

    def test_file_without_copy_blocks_is_reported(self):
        from django.core.management.base import CommandError

        empty = self._write("-- ничего интересного\n")
        with self.assertRaises(CommandError):
            call_command("load_dump", path=str(empty), verbosity=0)

    def test_flush_clears_content_but_keeps_superuser(self):
        call_command("load_dump", path=str(self.path), verbosity=0)
        root = User.objects.create_superuser(username="root", password="x")

        call_command("load_dump", path=str(self.path), flush=True, verbosity=0)
        self.assertTrue(User.objects.filter(pk=root.pk).exists())
        self.assertEqual(Course.objects.count(), 1)
