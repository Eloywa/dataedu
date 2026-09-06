"""Чистые правила геймификации: уровни и последовательное открытие недель."""

from django.test import SimpleTestCase

from gamification.gating import compute_gating
from gamification.levels import LEVEL_THRESHOLDS, level_for_xp, level_progress


class LevelTests(SimpleTestCase):
    def test_starts_at_first_level(self):
        self.assertEqual(level_for_xp(0), 1)

    def test_thresholds_are_exact_boundaries(self):
        """На самом пороге уровень уже новый, на единицу ниже — ещё прежний."""
        for i, threshold in enumerate(LEVEL_THRESHOLDS[1:], start=2):
            self.assertEqual(level_for_xp(threshold), i)
            self.assertEqual(level_for_xp(threshold - 1), i - 1)

    def test_level_never_falls_as_xp_grows(self):
        levels = [level_for_xp(xp) for xp in range(0, 1000, 7)]
        self.assertEqual(levels, sorted(levels))

    def test_max_level_is_capped(self):
        top = len(LEVEL_THRESHOLDS)
        self.assertEqual(level_for_xp(10**6), top)
        self.assertTrue(level_progress(10**6)["is_max"])
        self.assertEqual(level_progress(10**6)["pct"], 100)

    def test_progress_inside_level(self):
        # Второй уровень начинается на 60, третий на 120: 90 — ровно середина.
        progress = level_progress(90)
        self.assertEqual(progress["level"], 2)
        self.assertEqual(progress["pct"], 50)
        self.assertEqual(progress["to_next"], 30)


class GatingTests(SimpleTestCase):
    def test_first_module_is_always_open(self):
        flags = compute_gating([(3, 0)])
        self.assertTrue(flags[0]["unlocked"])
        self.assertFalse(flags[0]["is_complete"])

    def test_next_opens_only_after_previous_is_finished(self):
        flags = compute_gating([(2, 1), (2, 0)])
        self.assertTrue(flags[0]["unlocked"])
        self.assertFalse(flags[1]["unlocked"])

        flags = compute_gating([(2, 2), (2, 0)])
        self.assertTrue(flags[1]["unlocked"])

    def test_gap_closes_everything_after_it(self):
        """Пропущенная неделя закрывает не только следующую, но и все дальнейшие."""
        flags = compute_gating([(1, 1), (2, 1), (1, 1), (1, 0)])
        self.assertEqual([f["unlocked"] for f in flags], [True, True, False, False])

    def test_empty_module_is_never_complete(self):
        """Модуль без уроков не считается пройденным — иначе он открывал бы следующий."""
        flags = compute_gating([(0, 0), (1, 0)])
        self.assertFalse(flags[0]["is_complete"])
        self.assertFalse(flags[1]["unlocked"])

    def test_teacher_sees_everything(self):
        flags = compute_gating([(2, 0), (2, 0), (2, 0)], bypass=True)
        self.assertTrue(all(f["unlocked"] for f in flags))

    def test_no_modules_is_not_an_error(self):
        self.assertEqual(compute_gating([]), [])
