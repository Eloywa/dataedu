import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

# Уровень сложности. Набор значений взят из перечисления `task_level` исходной
# базы — менять его нельзя, не переливая данные. Подписи живут здесь и только здесь:
# фильтры шаблонов читают их отсюда же, чтобы список не разъезжался в двух местах.
LEVEL_CHOICES = [
    ("basic", "Начальный"),
    ("medium", "Средний"),
    ("advanced", "Продвинутый"),
]


class Topic(models.Model):
    """Тема каталога (тег курса)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(verbose_name="код", unique=True, max_length=50)
    name = models.CharField(verbose_name="название", max_length=100)

    class Meta:
        verbose_name = "тема"
        verbose_name_plural = "темы"
        db_table = "topics"

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name="название", max_length=200)
    slug = models.CharField(verbose_name="адрес (slug)", unique=True, max_length=200)
    description = models.TextField(verbose_name="описание", blank=True, null=True)
    semester = models.CharField(verbose_name="семестр", max_length=20, blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="authored_courses",
        blank=True,
        null=True,
        verbose_name="автор",
    )
    is_published = models.BooleanField(verbose_name="опубликован", default=False)
    created_at = models.DateTimeField(verbose_name="создан", default=timezone.now)
    level = models.CharField(verbose_name="уровень", max_length=50, choices=LEVEL_CHOICES)
    cover_url = models.TextField(verbose_name="обложка", blank=True, null=True)

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        db_table = "courses"

    def __str__(self):
        return self.title


class CourseTopic(models.Model):
    """Связь курс↔тема (составной ключ, без отдельного id)."""

    pk = models.CompositePrimaryKey("course_id", "topic_id")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_topics", verbose_name="курс"
    )
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="topic_courses", verbose_name="тема"
    )

    class Meta:
        verbose_name = "тема курса"
        verbose_name_plural = "темы курсов"
        db_table = "course_topics"

    def __str__(self):
        return f"{self.course_id} · {self.topic_id}"


class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="modules", verbose_name="курс"
    )
    title = models.CharField(verbose_name="название", max_length=200)
    description = models.TextField(verbose_name="описание", blank=True, null=True)
    order_index = models.IntegerField(
        verbose_name="порядок",
    )
    week_number = models.IntegerField(verbose_name="неделя", blank=True, null=True)

    class Meta:
        verbose_name = "модуль"
        verbose_name_plural = "модули"
        db_table = "modules"
        unique_together = (("course", "order_index"),)
        ordering = ["order_index"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lessons", verbose_name="модуль"
    )
    title = models.CharField(verbose_name="название", max_length=200)
    theory_content = models.TextField(verbose_name="теория", blank=True, null=True)
    order_index = models.IntegerField(
        verbose_name="порядок",
    )
    est_minutes = models.IntegerField(verbose_name="время, мин", blank=True, null=True)
    xp_reward = models.IntegerField(verbose_name="награда XP", default=0)

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        db_table = "lessons"
        unique_together = (("module", "order_index"),)
        ordering = ["order_index"]

    def __str__(self):
        return self.title


class CourseRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="ratings", verbose_name="курс"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_ratings",
        verbose_name="автор",
    )
    rating = models.IntegerField(
        verbose_name="оценка",
    )
    comment = models.TextField(verbose_name="отзыв", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="оставлен", default=timezone.now)

    class Meta:
        verbose_name = "отзыв о курсе"
        verbose_name_plural = "отзывы о курсах"
        db_table = "course_ratings"
        unique_together = (("course", "user"),)

    def __str__(self):
        return f"{self.course_id}: {self.rating}"
