import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Achievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(unique=True, max_length=50)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    xp_reward = models.IntegerField(default=0)

    class Meta:
        db_table = "achievements"

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="awarded_to")
    awarded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "user_achievements"
        unique_together = (("user", "achievement"),)
