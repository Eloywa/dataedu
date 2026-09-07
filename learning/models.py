import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

ENROLLMENT_STATUS_CHOICES = [
    ("active", "Учится"),
    ("completed", "Завершил"),
    ("dropped", "Бросил"),
]

PROGRESS_STATUS_CHOICES = [
    ("not_started", "Не начат"),
    ("in_progress", "В процессе"),
    ("completed", "Завершён"),
]

# Типы событий ленты. Совпадают с ключами в gamification.services — там же они
# и порождаются; расхождение сделало бы часть событий безымянными в отчётах.
ACTIVITY_TYPE_CHOICES = [
    ("login", "Вход"),
    ("lesson_view", "Просмотр урока"),
    ("lesson_complete", "Завершение урока"),
    ("test_start", "Начало теста"),
    ("test_finish", "Завершение теста"),
    ("sql_run", "Запрос в тренажёре"),
    ("sql_error", "Ошибка в SQL"),
    ("submission", "Сдача задания"),
    ("achievement", "Достижение"),
    ("reflection", "Рефлексия"),
]


class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="студент",
    )
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="enrollments", verbose_name="курс"
    )
    status = models.CharField(
        verbose_name="статус", max_length=50, choices=ENROLLMENT_STATUS_CHOICES
    )
    enrolled_at = models.DateTimeField(verbose_name="записан", default=timezone.now)
    completed_at = models.DateTimeField(verbose_name="завершён", blank=True, null=True)

    class Meta:
        verbose_name = "запись на курс"
        verbose_name_plural = "записи на курсы"
        db_table = "enrollments"
        unique_together = (("user", "course"),)
        indexes = [
            # Отчёты всегда начинаются с «кто записан на этот курс».
            models.Index(fields=["course", "user"], name="idx_enrollment_course_user"),
        ]

    def __str__(self):
        return f"{self.user_id} → {self.course_id}"


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
    name = models.CharField(
        "название", max_length=100, help_text="Номер группы, например «ИСТ-21»."
    )
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
    note = models.TextField(
        "заметка", blank=True, help_text="Для себя: семестр, поток, что угодно."
    )
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_progress",
        verbose_name="студент",
    )
    lesson = models.ForeignKey(
        "courses.Lesson", on_delete=models.CASCADE, related_name="progress", verbose_name="урок"
    )
    status = models.CharField(verbose_name="статус", max_length=50, choices=PROGRESS_STATUS_CHOICES)
    time_spent_sec = models.IntegerField(verbose_name="время, сек", default=0)
    visits = models.IntegerField(verbose_name="заходов", default=0)
    started_at = models.DateTimeField(verbose_name="начат", blank=True, null=True)
    completed_at = models.DateTimeField(verbose_name="завершён", blank=True, null=True)

    class Meta:
        verbose_name = "прогресс по уроку"
        verbose_name_plural = "прогресс по урокам"
        db_table = "lesson_progress"
        unique_together = (("user", "lesson"),)
        indexes = [
            # «Сколько уроков курса пройдено» — самый частый запрос платформы:
            # он на панели, в ведомости, в каталоге и на странице курса.
            models.Index(fields=["user", "status"], name="idx_progress_user_status"),
            models.Index(fields=["lesson", "status"], name="idx_progress_lesson_status"),
        ]

    def __str__(self):
        return f"{self.user_id} · {self.lesson_id} ({self.status})"


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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reflections",
        verbose_name="студент",
    )
    lesson = models.ForeignKey(
        "courses.Lesson", on_delete=models.CASCADE, related_name="reflections", verbose_name="урок"
    )
    clarity_rating = models.SmallIntegerField(verbose_name="понятность", blank=True, null=True)
    difficulty_rating = models.SmallIntegerField(verbose_name="трудность", blank=True, null=True)
    comment = models.TextField(verbose_name="комментарий", blank=True, null=True)
    comment_is_anonymous = models.BooleanField(
        "комментарий анонимно",
        default=False,
        help_text="Преподаватель увидит текст комментария без указания автора. "
        "На оценки понятности и трудности не влияет — они всегда привязаны к студенту.",
    )
    created_at = models.DateTimeField(verbose_name="оставлена", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name="изменена", blank=True, null=True)

    class Meta:
        verbose_name = "рефлексия"
        verbose_name_plural = "рефлексии"
        db_table = "reflections"
        unique_together = (("user", "lesson"),)

    def __str__(self):
        return f"{self.user_id} · {self.lesson_id}"


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities",
        verbose_name="пользователь",
    )
    type = models.CharField(verbose_name="тип", max_length=50, choices=ACTIVITY_TYPE_CHOICES)
    entity_type = models.CharField(verbose_name="объект", max_length=50, blank=True, null=True)
    entity_id = models.UUIDField(verbose_name="идентификатор объекта", blank=True, null=True)
    metadata = models.JSONField(verbose_name="подробности", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="когда", default=timezone.now)

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "события"
        db_table = "activities"
        indexes = [
            # Лента профиля и «дней без активности» на панели: и то и другое —
            # выборка последних событий пользователя.
            models.Index(fields=["user", "-created_at"], name="idx_activity_user_recent"),
            # Чистка по сроку хранения (`purge_metrics`) идёт по одному времени.
            models.Index(fields=["created_at"], name="idx_activity_created"),
        ]

    def __str__(self):
        return f"{self.type} · {self.user_id}"
