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
    """Рефлексия студента по уроку: насколько понятно и насколько трудно было.

    **Оценки привязаны к студенту намеренно.** Ядро новизны работы — сопоставление
    объективной трудности урока (время, число попыток, сбросы базы) с субъективной,
    и для этого нужна связь «этот студент оценил урок так, а объективно решал его
    столько». Полная анонимность оценок разрушила бы этот анализ.

    Анонимность вынесена в **комментарий**: галочка `comment_is_anonymous` означает,
    что преподавателю текст показывается без автора. Так честность отзывов сохраняется,
    не ломая аналитику.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reflections")
    lesson = models.ForeignKey("courses.Lesson", on_delete=models.CASCADE, related_name="reflections")
    clarity_rating = models.SmallIntegerField(blank=True, null=True)
    difficulty_rating = models.SmallIntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    comment_is_anonymous = models.BooleanField(
        "комментарий анонимно",
        default=False,
        help_text="Преподаватель увидит текст комментария без указания автора. "
        "На оценки понятности и трудности не влияет — они всегда привязаны к студенту.",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

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
