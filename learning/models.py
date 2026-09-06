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
        indexes = [
            # Отчёты всегда начинаются с «кто записан на этот курс».
            models.Index(fields=["course", "user"], name="idx_enrollment_course_user"),
        ]


class StudyGroup(models.Model):
    """Учебная группа: «ИСТ-21», «МО-22» и т. п.

    Записи на курс (`Enrollment`) для ведомости недостаточно: один курс могут слушать
    сразу две группы, а ведомость сдаётся по одной. Группа задаёт **состав**, курс —
    **дисциплину**; отчёт строится на их пересечении.

    Название группы обезличенных данных не образует: это номер потока, а не сведения
    о человеке. Соответствие «код участника ↔ студент» по-прежнему остаётся вне
    платформы (см. §17.14), поэтому группа ничего к объёму обрабатываемого не добавляет.

    Владелец нужен для той же изоляции авторства, что и у курсов (§17.9): преподаватель
    видит и правит только свои группы. Группа без владельца (`teacher = NULL`, остаётся
    после удаления учётной записи) видна только суперпользователю.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("название", max_length=100, help_text="Номер группы, например «ИСТ-21».")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="owned_groups",
        blank=True,
        null=True,
        verbose_name="преподаватель",
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="study_groups",
        blank=True,
        db_table="study_group_students",
        verbose_name="студенты",
        help_text="Кто входит в группу. В ведомость попадут те из них, кто записан на выбранный курс.",
    )
    note = models.TextField("заметка", blank=True, help_text="Для себя: семестр, поток, что угодно.")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "study_groups"
        verbose_name = "учебная группа"
        verbose_name_plural = "учебные группы"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["teacher", "name"], name="uniq_group_name_per_teacher")
        ]

    def __str__(self):
        return self.name


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
        indexes = [
            # «Сколько уроков курса пройдено» — самый частый запрос платформы:
            # он на панели, в ведомости, в каталоге и на странице курса.
            models.Index(fields=["user", "status"], name="idx_progress_user_status"),
            models.Index(fields=["lesson", "status"], name="idx_progress_lesson_status"),
        ]


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
        indexes = [
            # Лента профиля и «дней без активности» на панели: и то и другое —
            # выборка последних событий пользователя.
            models.Index(fields=["user", "-created_at"], name="idx_activity_user_recent"),
            # Чистка по сроку хранения (`purge_metrics`) идёт по одному времени.
            models.Index(fields=["created_at"], name="idx_activity_created"),
        ]
