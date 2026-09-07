"""Учёт ошибок в SQL и отчёт «на чём спотыкаются».

Разбор ошибки живёт в браузере (`static/js/sql/errors.js`) — там, где выполняется
запрос. Сервер принимает только код класса. Отсюда два рода проверок: что словарь
кодов на двух сторонах не разъехался, и что сервер не верит присланному на слово.
"""

import json
import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from core.tests import factories as f
from gamification import services
from learning import reports
from learning.models import Activity
from learning.sqlerrors import ERROR_ADVICE, ERROR_TITLES

ERRORS_JS = Path(settings.BASE_DIR) / "static" / "js" / "sql" / "errors.js"


class VocabularyTests(SimpleTestCase):
    """Словарь продублирован в JS и в Python — значит, его надо сверять.

    Перенести разбор на сервер было бы дороже: пришлось бы отправлять туда текст
    ошибки, в котором лежат данные студента. Дублирование дешевле, но только
    вместе с этой проверкой — иначе новый класс ошибки появится в подсказках и
    молча пропадёт из отчёта.
    """

    def js_codes(self):
        text = ERRORS_JS.read_text(encoding="utf-8")
        return set(re.findall(r'code:\s*"([a-z_]+)"', text))

    def test_every_js_code_has_a_title(self):
        missing = self.js_codes() - set(ERROR_TITLES)
        self.assertEqual(missing, set(), f"классы без названия на сервере: {missing}")

    def test_every_title_is_produced_by_the_classifier(self):
        # "other" в правилах не объявлен: это ветка «ничего не подошло».
        extra = set(ERROR_TITLES) - self.js_codes() - {"other"}
        self.assertEqual(extra, set(), f"названия без правила разбора: {extra}")

    def test_every_class_has_advice(self):
        self.assertEqual(set(ERROR_TITLES), set(ERROR_ADVICE))


class RecordingTests(TestCase):
    def setUp(self):
        self.student = f.student()

    def test_known_code_is_recorded(self):
        services.record_sql_error(self.student, "group_by")
        event = Activity.objects.get(user=self.student, type="sql_error")
        self.assertEqual(event.metadata, {"code": "group_by"})
        self.assertEqual(event.entity_type, "trainer")

    def test_unknown_code_is_ignored(self):
        """Код приходит из браузера: в поле metadata нельзя положить что угодно."""
        services.record_sql_error(self.student, "'; DROP TABLE activities; --")
        services.record_sql_error(self.student, None)
        self.assertFalse(Activity.objects.filter(type="sql_error").exists())

    def test_assignment_is_remembered(self):
        task = f.assignment(f.course())
        services.record_sql_error(self.student, "syntax", assignment_id=task.id)
        event = Activity.objects.get(type="sql_error")
        self.assertEqual(event.entity_type, "assignment")
        self.assertEqual(event.entity_id, task.id)


class EndpointTests(TestCase):
    def setUp(self):
        self.student = f.student()
        self.course = f.course()
        self.task = f.assignment(self.course)
        self.client.force_login(self.student)

    def post(self, url, payload):
        return self.client.post(url, json.dumps(payload), content_type="application/json")

    def test_trainer_reports_error_class(self):
        response = self.post(reverse("core:trainer_log"), {"event": "error", "error": "no_table"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Activity.objects.filter(type="sql_error").count(), 1)
        self.assertFalse(Activity.objects.filter(type="sql_run").exists())

    def test_trainer_run_still_works_without_a_body(self):
        """Открытая вкладка со старым скриптом слала пустой POST — она не должна падать."""
        response = self.client.post(reverse("core:trainer_log"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Activity.objects.filter(type="sql_run").exists())

    def test_assignment_error_is_tied_to_the_task(self):
        url = reverse("assessments:report_error", args=[self.task.id])
        self.assertEqual(self.post(url, {"error": "types"}).status_code, 200)
        self.assertEqual(Activity.objects.get(type="sql_error").entity_id, self.task.id)

    def test_anonymous_is_not_logged(self):
        self.client.logout()
        self.post(reverse("core:trainer_log"), {"event": "error", "error": "syntax"})
        self.assertFalse(Activity.objects.exists())


class ReportTests(TestCase):
    def setUp(self):
        self.teacher = f.teacher()
        self.course, self.lessons = f.course_with_lessons(author=self.teacher)
        self.task = f.assignment(self.course, lesson_obj=self.lessons[0])
        self.student = f.student()
        f.enroll(self.student, self.course)

    def make(self, code, times=1, on_task=True):
        for _ in range(times):
            services.record_sql_error(
                self.student, code, assignment_id=self.task.id if on_task else None
            )

    def test_classes_are_ranked_and_shared(self):
        self.make("group_by", 3)
        self.make("syntax", 1)
        data = reports.sql_error_rows(self.teacher)

        self.assertEqual(data["total"], 4)
        self.assertEqual(data["classes"][0]["code"], "group_by")
        self.assertEqual(data["classes"][0]["share"], 75)
        self.assertTrue(data["classes"][0]["advice"])

    def test_lessons_show_the_prevailing_class(self):
        self.make("group_by", 3)
        self.make("syntax", 1)
        rows = reports.sql_error_rows(self.teacher)["lessons"]

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["lesson"], self.lessons[0].title)
        self.assertEqual(rows[0]["n"], 4)
        self.assertEqual(rows[0]["top_label"], ERROR_TITLES["group_by"])
        self.assertEqual(rows[0]["top_share"], 75)

    def test_trainer_errors_count_but_have_no_lesson(self):
        """В тренажёре урока нет — событие идёт в общую разбивку и только в неё."""
        self.make("syntax", 2, on_task=False)
        data = reports.sql_error_rows(self.teacher)
        self.assertEqual(data["total"], 2)
        self.assertEqual(data["lessons"], [])

    def test_other_teachers_students_are_invisible(self):
        stranger_course = f.course(author=f.teacher())
        outsider = f.student()
        f.enroll(outsider, stranger_course)
        services.record_sql_error(outsider, "syntax")

        self.assertEqual(reports.sql_error_rows(self.teacher)["total"], 0)

    def test_empty_report_does_not_divide_by_zero(self):
        data = reports.sql_error_rows(self.teacher)
        self.assertEqual(data, {"total": 0, "classes": [], "lessons": []})

    def test_report_is_set_based(self):
        """Обход событий по одному дал бы тем больше запросов, чем хуже дела.

        Четыре: курсы преподавателя, разбивка по классам, разбивка по заданиям и
        добор самих заданий. Список студентов уходит подзапросом внутрь второго
        и третьего, отдельного обращения не требует.
        """
        self.make("group_by", 12)
        self.make("syntax", 8)
        with self.assertNumQueries(4):
            reports.sql_error_rows(self.teacher)
