import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Topic(models.Model):
    """Тема каталога (тег курса)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "topics"

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.CharField(unique=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="authored_courses",
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    level = models.CharField(max_length=50)
    cover_url = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "courses"

    def __str__(self):
        return self.title


class CourseTopic(models.Model):
    """Связь курс↔тема (составной ключ, без отдельного id)."""

    pk = models.CompositePrimaryKey("course_id", "topic_id")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_topics")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topic_courses")

    class Meta:
        db_table = "course_topics"

    def __str__(self):
        return f"{self.course_id} · {self.topic_id}"


class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order_index = models.IntegerField()
    week_number = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "modules"
        unique_together = (("course", "order_index"),)
        ordering = ["order_index"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    theory_content = models.TextField(blank=True, null=True)
    order_index = models.IntegerField()
    est_minutes = models.IntegerField(blank=True, null=True)
    xp_reward = models.IntegerField(default=0)

    class Meta:
        db_table = "lessons"
        unique_together = (("module", "order_index"),)
        ordering = ["order_index"]

    def __str__(self):
        return self.title


class CourseRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_ratings")
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "course_ratings"
        unique_together = (("course", "user"),)

    def __str__(self):
        return f"{self.course_id}: {self.rating}"
