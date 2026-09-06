import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Achievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(verbose_name="код", unique=True, max_length=50)
    title = models.CharField(verbose_name="название", max_length=150)
    description = models.TextField(verbose_name="описание", blank=True, null=True)
    icon = models.CharField(verbose_name="значок", max_length=100, blank=True, null=True)
    xp_reward = models.IntegerField(verbose_name="награда XP", default=0)

    class Meta:
        verbose_name = "достижение"
        verbose_name_plural = "достижения"
        db_table = "achievements"

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="achievements",
        verbose_name="пользователь",
    )
    achievement = models.ForeignKey(
        Achievement, on_delete=models.CASCADE, related_name="awarded_to", verbose_name="достижение"
    )
    awarded_at = models.DateTimeField(verbose_name="получено", default=timezone.now)

    class Meta:
        verbose_name = "полученное достижение"
        verbose_name_plural = "полученные достижения"
        db_table = "user_achievements"
        unique_together = (("user", "achievement"),)

    def __str__(self):
        return f"{self.user_id} · {self.achievement_id}"
