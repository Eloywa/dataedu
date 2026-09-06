"""Формулы учебной аналитики — без базы.

Проверяются не «примеры значений», а свойства формул: границы, монотонность,
поведение при отсутствующих данных. Пример проходит и на случайной формуле;
свойство ломается, как только формулу поменяли по существу.
"""

from django.test import SimpleTestCase

from learning.analytics import (
    compute_risk,
    divergence,
    final_score,
    grade_5,
    mastery_zone,
    objective_difficulty,
    pass_fail,
    risk_zone,
    subjective_difficulty,
)


class RiskTests(SimpleTestCase):
    def test_perfect_student_has_no_risk(self):
        self.assertEqual(compute_risk(completion=100, avg_score=100, days_inactive=0), 0)

    def test_worst_case_is_full_risk(self):
        self.assertEqual(compute_risk(completion=0, avg_score=0, days_inactive=60), 100)

    def test_missing_data_counts_as_worst(self):
        """`None` — это не «ноль риска», а «оснований считать, что всё хорошо, нет»."""
        self.assertEqual(
            compute_risk(0, None, None), compute_risk(0, 0, 999)
        )

    def test_risk_falls_as_progress_grows(self):
        values = [compute_risk(pct, 70, 3) for pct in range(0, 101, 10)]
        self.assertEqual(values, sorted(values, reverse=True))

    def test_inactivity_saturates_after_two_weeks(self):
        """Дальше двух недель разницы нет: и месяц, и год — «не заходит»."""
        self.assertEqual(compute_risk(50, 50, 14), compute_risk(50, 50, 400))

    def test_weights_sum_to_whole(self):
        """Каждая составляющая по отдельности даёт свой вес, вместе — сотню."""
        only_completion = compute_risk(0, 100, 0)
        only_score = compute_risk(100, 0, 0)
        only_idle = compute_risk(100, 100, 14)
        self.assertEqual(only_completion + only_score + only_idle, 100)

    def test_zones_cover_whole_range(self):
        labels = {risk_zone(v)["label"] for v in range(0, 101)}
        self.assertEqual(labels, {"низкий", "средний", "высокий"})


class DifficultyTests(SimpleTestCase):
    def test_objective_difficulty_grows_when_results_worsen(self):
        easy = objective_difficulty(avg_score=95, avg_attempts=1.0, failed_share=0.0)
        hard = objective_difficulty(avg_score=40, avg_attempts=3.0, failed_share=0.8)
        self.assertLess(easy, hard)

    def test_objective_difficulty_needs_at_least_one_signal(self):
        self.assertIsNone(objective_difficulty(None, None, None))

    def test_subjective_difficulty_maps_five_point_scale(self):
        self.assertEqual(subjective_difficulty(1), 0)
        self.assertEqual(subjective_difficulty(5), 100)
        self.assertIsNone(subjective_difficulty(None))

    def test_divergence_is_signed(self):
        """Знак важен: он и отличает «недооценивают» от «переоценивают»."""
        harder_than_feels = divergence(objective=80, subjective=20)
        easier_than_feels = divergence(objective=20, subjective=80)
        self.assertGreater(harder_than_feels["delta"], 0)
        self.assertLess(easier_than_feels["delta"], 0)
        self.assertNotEqual(harder_than_feels["label"], easier_than_feels["label"])

    def test_divergence_needs_both_sides(self):
        self.assertIsNone(divergence(objective=50, subjective=None))
        self.assertIsNone(divergence(objective=None, subjective=50))

    def test_mastery_zone_handles_missing(self):
        self.assertIsNotNone(mastery_zone(0))
        self.assertIsNotNone(mastery_zone(100))


class FinalScoreTests(SimpleTestCase):
    """Итоговая отметка ведомости: веса 0.5 / 0.3 / 0.2."""

    def test_all_perfect_is_hundred(self):
        self.assertEqual(final_score(1.0, 1.0, 1.0), 100)

    def test_weights(self):
        self.assertEqual(final_score(1.0, 0.0, 0.0), 50)
        self.assertEqual(final_score(0.0, 1.0, 0.0), 30)
        self.assertEqual(final_score(0.0, 0.0, 1.0), 20)

    def test_missing_part_redistributes_weight(self):
        """Если в курсе нет заданий, оставшиеся составляющие делят вес между собой.

        Это отличается от «не сдал»: требование, которого не предъявляли, провалить
        нельзя. `None` здесь означает «в курсе этого нет», а не «студент не сделал».
        """
        self.assertEqual(final_score(1.0, 1.0, None), 100)

    def test_nothing_to_grade_gives_no_mark(self):
        self.assertIsNone(final_score(None, None, None))

    def test_grade_scale_boundaries(self):
        self.assertEqual(grade_5(85)["mark"], 5)
        self.assertEqual(grade_5(84)["mark"], 4)
        self.assertEqual(grade_5(70)["mark"], 4)
        self.assertEqual(grade_5(69)["mark"], 3)
        self.assertEqual(grade_5(55)["mark"], 3)
        self.assertEqual(grade_5(54)["mark"], 2)

    def test_pass_boundary_matches_lowest_positive_mark(self):
        """Две шкалы не должны расходиться: «неуд», но «зачтено» читалось бы как ошибка."""
        for value in range(0, 101):
            passed = pass_fail(value)["passed"]
            positive = grade_5(value)["mark"] is not None and grade_5(value)["mark"] >= 3
            self.assertEqual(passed, positive, f"расхождение на {value}")

    def test_no_score_is_not_a_pass(self):
        self.assertIsNone(grade_5(None)["mark"])
        self.assertFalse(pass_fail(None)["passed"])
