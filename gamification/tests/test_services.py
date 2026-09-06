"""Начисления, достижения и лента активности."""

from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.tests import factories as f
from gamification import services
from gamification.models import UserAchievement
from learning.models import Activity, LessonProgress


class XpTests(TestCase):
    def test_xp_raises_level(self):
        user = f.student()
        services.add_xp(user, 60)
        user.refresh_from_db()
        self.assertEqual(user.xp, 60)
        self.assertEqual(user.level, 2)

    def test_zero_xp_changes_nothing(self):
        user = f.student()
        services.add_xp(user, 0)
        user.refresh_from_db()
        self.assertEqual(user.xp, 0)


class AchievementTests(TestCase):
    def test_award_is_idempotent(self):
        """Повторная выдача не задваивает ни запись, ни XP."""
        user = f.student()
        f.achievement("first_lesson", xp_reward=25)

        self.assertTrue(services.award_achievement(user, "first_lesson"))
        self.assertFalse(services.award_achievement(user, "first_lesson"))

        user.refresh_from_db()
        self.assertEqual(UserAchievement.objects.filter(user=user).count(), 1)
        self.assertEqual(user.xp, 25)

    def test_unknown_code_is_ignored(self):
        self.assertFalse(services.award_achievement(f.student(), "нет-такого"))

    def test_award_writes_activity(self):
        user = f.student()
        f.achievement("first_query")
        services.award_achievement(user, "first_query")
        self.assertTrue(Activity.objects.filter(user=user, type="achievement").exists())


class CompleteLessonTests(TestCase):
    def setUp(self):
        self.user = f.student()
        self.course, self.lessons = f.course_with_lessons(lessons=2)
        f.achievement("first_lesson", xp_reward=25)

    def test_first_completion_gives_xp_and_achievement(self):
        self.assertTrue(services.complete_lesson(self.user, self.lessons[0]))
        self.user.refresh_from_db()
        # 10 XP за урок (фабрика) + 25 за «Первый шаг».
        self.assertEqual(self.user.xp, 35)
        self.assertTrue(
            LessonProgress.objects.filter(
                user=self.user, lesson=self.lessons[0], status="completed"
            ).exists()
        )

    def test_second_completion_of_same_lesson_gives_nothing(self):
        services.complete_lesson(self.user, self.lessons[0])
        self.user.refresh_from_db()
        before = self.user.xp

        self.assertFalse(services.complete_lesson(self.user, self.lessons[0]))
        self.user.refresh_from_db()
        self.assertEqual(self.user.xp, before)

    def test_completion_upgrades_started_progress(self):
        LessonProgress.objects.create(user=self.user, lesson=self.lessons[0], status="in_progress")
        self.assertTrue(services.complete_lesson(self.user, self.lessons[0]))
        self.assertEqual(LessonProgress.objects.filter(user=self.user).count(), 1)


class FinishTestTests(TestCase):
    def setUp(self):
        self.user = f.student()
        self.course, self.lessons = f.course_with_lessons(lessons=1)
        self.lesson = self.lessons[0]
        self.test = f.test_for(self.lesson)
        f.achievement("first_lesson", xp_reward=25)
        f.achievement("test_master", xp_reward=30)

    def test_pass_gives_xp_once(self):
        first = f.attempt(self.user, self.test, score=100, passed=True)
        services.finish_test(self.user, first, self.lesson)
        self.user.refresh_from_db()
        after_first = self.user.xp

        second = f.attempt(self.user, self.test, score=100, passed=True)
        services.finish_test(self.user, second, self.lesson)
        self.user.refresh_from_db()
        self.assertEqual(self.user.xp, after_first)

    def test_pass_completes_the_lesson(self):
        attempt = f.attempt(self.user, self.test, score=100, passed=True)
        services.finish_test(self.user, attempt, self.lesson)
        self.assertTrue(
            LessonProgress.objects.filter(
                user=self.user, lesson=self.lesson, status="completed"
            ).exists()
        )

    def test_failed_attempt_does_not_complete_the_lesson(self):
        attempt = f.attempt(self.user, self.test, score=20, passed=False)
        services.finish_test(self.user, attempt, self.lesson)
        self.assertFalse(LessonProgress.objects.filter(user=self.user).exists())

    def test_high_score_awards_test_master(self):
        attempt = f.attempt(self.user, self.test, score=80, passed=True)
        services.finish_test(self.user, attempt, self.lesson)
        self.assertTrue(
            UserAchievement.objects.filter(user=self.user, achievement__code="test_master").exists()
        )


class StreakTests(TestCase):
    def test_seven_days_in_a_row_award_the_streak(self):
        user = f.student()
        f.achievement("no_miss_week", xp_reward=50)
        start = timezone.now() - timedelta(days=10)
        for day in range(7):
            f.activity(user, "login", when=start + timedelta(days=day))

        services.check_login_streak(user)
        self.assertTrue(
            UserAchievement.objects.filter(user=user, achievement__code="no_miss_week").exists()
        )

    def test_a_gap_breaks_the_streak(self):
        user = f.student()
        f.achievement("no_miss_week")
        start = timezone.now() - timedelta(days=12)
        for day in [0, 1, 2, 4, 5, 6, 7]:
            f.activity(user, "login", when=start + timedelta(days=day))

        services.check_login_streak(user)
        self.assertFalse(UserAchievement.objects.filter(user=user).exists())

    def test_several_logins_a_day_are_one_day(self):
        user = f.student()
        f.achievement("no_miss_week")
        moment = timezone.now() - timedelta(days=1)
        for _ in range(10):
            f.activity(user, "login", when=moment)

        services.check_login_streak(user)
        self.assertFalse(UserAchievement.objects.filter(user=user).exists())


class ActivityFeedTests(TestCase):
    def test_only_meaningful_events_are_shown(self):
        user = f.student()
        course, lessons = f.course_with_lessons(lessons=1)
        f.activity(user, "login")
        f.activity(user, "lesson_complete", entity_type="lesson", entity_id=lessons[0].pk)

        groups = services.get_recent_activity(user)
        texts = [item["text"] for group in groups for item in group["items"]]
        self.assertEqual(len(texts), 1)
        self.assertIn(lessons[0].title, texts[0])

    def test_repeated_events_collapse(self):
        user = f.student()
        f.activity(user, "sql_run")
        f.activity(user, "sql_run")
        groups = services.get_recent_activity(user)
        items = [item for group in groups for item in group["items"]]
        self.assertEqual(len(items), 1)


class ProfilePageTests(TestCase):
    def test_profile_shows_level_and_stats(self):
        user = f.student()
        course, lessons = f.course_with_lessons(lessons=2)
        f.complete(user, lessons[0])
        services.add_xp(user, 60)

        self.client.force_login(user)
        response = self.client.get(reverse("gamification:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["progress"]["level"], 2)
        self.assertEqual(response.context["stats"]["lessons"], 1)

    def test_guest_is_redirected(self):
        response = self.client.get(reverse("gamification:profile"))
        self.assertEqual(response.status_code, 302)


class TrainerLogTests(TestCase):
    def test_first_query_awards_achievement(self):
        user = f.student()
        f.achievement("first_query", title="Первый запрос")
        self.client.force_login(user)

        response = self.client.post(reverse("core:trainer_log"))
        self.assertEqual(response.json()["achievement"], "Первый запрос")

        # Второй запуск достижение уже не выдаёт.
        self.assertIsNone(self.client.post(reverse("core:trainer_log")).json()["achievement"])

    def test_guest_is_not_logged(self):
        response = self.client.post(reverse("core:trainer_log"))
        self.assertFalse(response.json()["ok"])
        self.assertEqual(Activity.objects.count(), 0)
