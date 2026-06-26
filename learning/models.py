import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=50)
    enrolled_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "enrollments"
        unique_together = (("user", "course"),)


class LessonProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey("courses.Lesson", on_delete=models.CASCADE, related_name="progress")
    status = models.CharField(max_length=50)
    time_spent_sec = models.IntegerField(default=0)
    visits = models.IntegerField(default=0)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "lesson_progress"
        unique_together = (("user", "lesson"),)


class Reflection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reflections")
    lesson = models.ForeignKey("courses.Lesson", on_delete=models.CASCADE, related_name="reflections")
    clarity_rating = models.SmallIntegerField(blank=True, null=True)
    difficulty_rating = models.SmallIntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "reflections"
        unique_together = (("user", "lesson"),)


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="activities")
    type = models.CharField(max_length=50)
    entity_type = models.CharField(max_length=50, blank=True, null=True)
    entity_id = models.UUIDField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "activities"
