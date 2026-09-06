"""Сравнение результатов SQL и диагностика автопроверки — без базы."""

from decimal import Decimal

from django.test import SimpleTestCase

from assessments.grading import diagnose, jsonable, normalize_rows, rows_equal


class RowsEqualTests(SimpleTestCase):
    def test_row_order_does_not_matter(self):
        """Без ORDER BY порядок строк не определён — требовать его нельзя."""
        self.assertTrue(rows_equal(["a"], [[1], [2]], ["a"], [[2], [1]]))

    def test_duplicates_matter(self):
        """Мультимножество, а не множество: лишний дубль — это другой результат."""
        self.assertFalse(rows_equal(["a"], [[1], [1]], ["a"], [[1]]))

    def test_types_are_normalised(self):
        """PGlite возвращает числа строками — разница типов не должна мешать."""
        self.assertTrue(rows_equal(["n"], [["1"]], ["n"], [[1]]))
        self.assertTrue(rows_equal(["n"], [[Decimal("2.5")]], ["n"], [["2.5"]]))

    def test_column_count_matters(self):
        self.assertFalse(rows_equal(["a"], [[1]], ["a", "b"], [[1, 2]]))

    def test_nulls_do_not_break_comparison(self):
        """Сортировка кортежей падала бы на None рядом со строкой — здесь Counter."""
        self.assertTrue(
            rows_equal(["a", "b"], [["x", None], ["x", "y"]], ["a", "b"], [["x", "y"], ["x", None]])
        )

    def test_booleans_are_normalised(self):
        self.assertEqual(normalize_rows([[True]]), normalize_rows([["true"]]))

    def test_empty_result_equals_empty(self):
        self.assertTrue(rows_equal(["a"], [], ["a"], []))


class JsonableTests(SimpleTestCase):
    def test_decimal_becomes_string(self):
        self.assertEqual(jsonable([[Decimal("1.50")]]), [["1.50"]])

    def test_simple_types_survive(self):
        self.assertEqual(jsonable([[1, "x", True, None]]), [[1, "x", True, None]])


class DiagnoseTests(SimpleTestCase):
    def test_correct_answer_passes(self):
        report = diagnose(["n"], [[1]], ["n"], [[1]])
        self.assertTrue(report["passed"])
        self.assertEqual(report["hint"], "")
        self.assertTrue(all(c["ok"] for c in report["checks"]))

    def test_wrong_column_count_is_named(self):
        report = diagnose(["a", "b"], [[1, 2]], ["a"], [[1]])
        self.assertFalse(report["passed"])
        columns = next(c for c in report["checks"] if c["label"] == "столбцы")
        self.assertFalse(columns["ok"])
        self.assertIn("SELECT", report["hint"])

    def test_extra_rows_hint_points_at_where(self):
        report = diagnose(["a"], [[1], [2]], ["a"], [[1]])
        self.assertFalse(report["passed"])
        self.assertIn("WHERE", report["hint"])

    def test_missing_rows_hint_points_at_where(self):
        report = diagnose(["a"], [[1]], ["a"], [[1], [2]])
        self.assertIn("WHERE", report["hint"])

    def test_duplicates_hint_suggests_distinct(self):
        report = diagnose(["a"], [[1], [1]], ["a"], [[1]])
        self.assertIn("DISTINCT", report["hint"])

    def test_diagnostics_never_reveal_the_reference(self):
        """Подсказка сообщает формы и количества, но не содержимое эталона."""
        secret = "СЕКРЕТНОЕ_ЗНАЧЕНИЕ"
        report = diagnose(["a"], [["другое"]], ["a"], [[secret]])
        blob = report["hint"] + "".join(c["detail"] for c in report["checks"])
        self.assertNotIn(secret, blob)

    def test_row_count_check_reports_both_numbers(self):
        report = diagnose(["a"], [[1]], ["a"], [[1], [2], [3]])
        rows = next(c for c in report["checks"] if c["label"] == "число строк")
        self.assertIn("3", rows["detail"])
        self.assertIn("1", rows["detail"])

    def test_content_check_is_skipped_when_columns_differ(self):
        """Несовпадение уже объяснено предыдущей проверкой — дублировать незачем."""
        report = diagnose(["a", "b"], [[1, 2]], ["a"], [[1]])
        labels = [c["label"] for c in report["checks"]]
        self.assertNotIn("состав строк", labels)

    def test_empty_answer_against_non_empty_reference(self):
        report = diagnose(["a"], [], ["a"], [[1]])
        self.assertFalse(report["passed"])
        self.assertNotEqual(report["hint"], "")
