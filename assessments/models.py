import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from courses.models import LEVEL_CHOICES, Course

# Тип вопроса: набор из перечисления `question_type` исходной базы. Сейчас
# платформа умеет только одиночный выбор, остальные оставлены как задел схемы.
QUESTION_TYPE_CHOICES = [
    ("single", "Одиночный выбор"),
    ("multiple", "Множественный выбор"),
    ("text", "Свободный ответ"),
    ("sql", "SQL-запрос"),
]

# Тип задания. `ddl` добавлен уже в Django-версии: такие задания автопроверке не
# поддаются (запрос не возвращает строк) и идут преподавателю — см. is_autocheckable.
TASK_TYPE_CHOICES = [
    ("sql", "SQL-запрос"),
    ("ddl", "Создание структуры (DDL)"),
    ("file", "Файл"),
    ("text", "Текст"),
]

SUBMISSION_STATUS_CHOICES = [
    ("submitted", "На проверке"),
    ("graded", "Оценено"),
    ("returned", "На доработке"),
]


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(
        "courses.Lesson", on_delete=models.CASCADE, related_name="tests", verbose_name="урок"
    )
    title = models.CharField(verbose_name="название", max_length=200)
    pass_score = models.IntegerField(
        verbose_name="порог сдачи, %",
    )
    time_limit_sec = models.IntegerField(verbose_name="ограничение, сек", blank=True, null=True)

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"
        db_table = "tests"

    def __str__(self):
        return self.title


class Question(models.Model):
    """Вопрос теста.

    Поле `topic` добавлено на этапе 11: без связи «вопрос → тема» карта освоения по
    темам построить нельзя — таблица `topics` была, но связывалась только с курсом
    целиком, а курс покрывает много тем сразу. Поле необязательное: у вопроса без
    темы просто нет вклада в карту, и в отчёте видно, сколько таких.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="questions", verbose_name="тест"
    )
    text = models.TextField(
        verbose_name="формулировка",
    )
    type = models.CharField(
        verbose_name="тип", max_length=50, choices=QUESTION_TYPE_CHOICES, default="single"
    )
    points = models.IntegerField(
        verbose_name="баллов",
    )
    order_index = models.IntegerField(
        verbose_name="порядок",
    )
    topic = models.ForeignKey(
        "courses.Topic",
        on_delete=models.SET_NULL,
        related_name="questions",
        blank=True,
        null=True,
        verbose_name="тема",
        help_text="Для карты освоения по темам. Без темы вопрос в карту не попадает.",
    )

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
        db_table = "questions"
        ordering = ["order_index"]

    def __str__(self):
        return self.text[:60]


class AnswerOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options", verbose_name="вопрос"
    )
    text = models.TextField(
        verbose_name="текст",
    )
    is_correct = models.BooleanField(verbose_name="верный", default=False)
    order_index = models.IntegerField(
        verbose_name="порядок",
    )

    class Meta:
        verbose_name = "вариант ответа"
        verbose_name_plural = "варианты ответов"
        db_table = "answer_options"
        ordering = ["order_index"]

    def __str__(self):
        return self.text[:60]


class TestAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="test_attempts",
        verbose_name="студент",
    )
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="attempts", verbose_name="тест"
    )
    score = models.DecimalField(
        verbose_name="балл", max_digits=5, decimal_places=2, blank=True, null=True
    )
    is_passed = models.BooleanField(verbose_name="сдан", blank=True, null=True)
    started_at = models.DateTimeField(verbose_name="начата", default=timezone.now)
    finished_at = models.DateTimeField(verbose_name="завершена", blank=True, null=True)

    class Meta:
        verbose_name = "попытка теста"
        verbose_name_plural = "попытки тестов"
        db_table = "test_attempts"
        indexes = [
            # Лучшая попытка студента по тесту — основа ведомости и страницы урока.
            models.Index(fields=["user", "test", "-score"], name="idx_attempt_user_test"),
            models.Index(fields=["test", "is_passed"], name="idx_attempt_test_passed"),
        ]

    def __str__(self):
        return f"{self.test_id} · {self.user_id}"


class AnswerSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.ForeignKey(
        TestAttempt, on_delete=models.CASCADE, related_name="answers", verbose_name="попытка"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="submissions", verbose_name="вопрос"
    )
    answer_option = models.ForeignKey(
        AnswerOption,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="выбранный вариант",
    )
    text_answer = models.TextField(verbose_name="текст ответа", blank=True, null=True)
    is_correct = models.BooleanField(verbose_name="верно", blank=True, null=True)

    class Meta:
        verbose_name = "ответ на вопрос"
        verbose_name_plural = "ответы на вопросы"
        db_table = "answer_submissions"

    def __str__(self):
        return f"{self.question_id}: {'верно' if self.is_correct else 'неверно'}"


class AssignmentQuerySet(models.QuerySet):
    """Разделение заданий на автопроверяемые и ручные — на стороне базы.

    Раньше это решалось перебором в Python: выбирались все задания курса и
    отсеивались свойством `is_autocheckable`. Пока заданий два десятка, разницы нет;
    на каталоге в несколько сотен это лишняя выборка целиком ради флага, который
    база умеет проверить сама по индексу.

    Условие повторяет `is_autocheckable` и обязано с ним совпадать — на это есть тест.
    """

    def autocheckable(self):
        return self.filter(type="sql", expected_result__isnull=False)

    def manual(self):
        return self.exclude(type="sql", expected_result__isnull=False)

    def visible_to(self, user):
        """Задания курсов, которые пользователь вправе открыть (см. `Course.visible_to`)."""
        return self.filter(course__in=Course.objects.visible_to(user))


class Assignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="assignments", verbose_name="курс"
    )
    lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=models.SET_NULL,
        related_name="assignments",
        blank=True,
        null=True,
        verbose_name="урок",
    )
    title = models.CharField(verbose_name="название", max_length=200)
    description = models.TextField(verbose_name="условие", blank=True, null=True)
    level = models.CharField(verbose_name="уровень", max_length=50, choices=LEVEL_CHOICES)
    type = models.CharField(verbose_name="тип", max_length=50, choices=TASK_TYPE_CHOICES)
    expected_sql = models.TextField(verbose_name="эталонный запрос", blank=True, null=True)
    # Заготовка данных для задачи (создаётся в PGlite у студента и при расчёте эталона)
    setup_sql = models.TextField(verbose_name="подготовка данных", blank=True, null=True)
    # Предрасчитанный эталонный результат: {"columns": [...], "rows": [[...], ...]}
    expected_result = models.JSONField(verbose_name="эталонный результат", blank=True, null=True)
    max_score = models.IntegerField(
        verbose_name="максимум баллов",
    )
    is_final = models.BooleanField(verbose_name="итоговое", default=False)
    opens_after = models.ForeignKey(
        "courses.Module",
        on_delete=models.SET_NULL,
        related_name="opened_assignments",
        blank=True,
        null=True,
        verbose_name="билет открывается после блока",
        help_text=(
            "Для итогового проекта: студент вытянет билет, когда пройдёт все уроки этого "
            "блока. Пусто — сразу после записи на курс."
        ),
    )
    created_at = models.DateTimeField(verbose_name="создано", default=timezone.now)

    objects = AssignmentQuerySet.as_manager()

    class Meta:
        verbose_name = "задание"
        verbose_name_plural = "задания"
        db_table = "assignments"
        indexes = [
            # Очередь проверки и список заданий всегда идут в разрезе курса и типа.
            models.Index(fields=["course", "type"], name="idx_assignment_course_type"),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        """Урок и блок должны быть из того же курса, что и задание.

        Иначе переход с урока вёл бы на задание чужого курса, а его балл считался бы в
        ведомости совсем другой дисциплины.
        """
        if self.lesson_id and self.lesson.module.course_id != self.course_id:
            raise ValidationError({"lesson": "Урок должен быть из курса этого задания."})
        if self.opens_after_id and self.opens_after.course_id != self.course_id:
            raise ValidationError({"opens_after": "Блок должен быть из курса этого задания."})

    @property
    def is_autocheckable(self):
        """Можно ли проверить задание автоматически.

        Недостаточно `type == "sql"`: нужен ещё посчитанный эталон. DDL-задания
        (`type = "ddl"`) сравнением результата не проверяются — запрос студента не
        возвращает строк; файловые — тем более. Такие идут на проверку преподавателя.

        Условие обязано совпадать с `AssignmentQuerySet.autocheckable()`, иначе
        страница задания и очередь проверки разойдутся в том, что считать ручным.
        """
        return self.type == "sql" and self.expected_result is not None


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name="submissions", verbose_name="задание"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="студент",
    )
    sql_query = models.TextField(verbose_name="запрос студента", blank=True, null=True)
    file_url = models.TextField(verbose_name="файл", blank=True, null=True)
    text_answer = models.TextField(verbose_name="текстовый ответ", blank=True, null=True)
    score = models.DecimalField(
        verbose_name="балл", max_digits=5, decimal_places=2, blank=True, null=True
    )
    feedback = models.TextField(verbose_name="отзыв", blank=True, null=True)
    status = models.CharField(
        verbose_name="статус", max_length=50, choices=SUBMISSION_STATUS_CHOICES
    )
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        db_column="graded_by",
        related_name="graded_submissions",
        blank=True,
        null=True,
        verbose_name="проверил",
    )
    submitted_at = models.DateTimeField(verbose_name="сдано", default=timezone.now)
    graded_at = models.DateTimeField(verbose_name="проверено", blank=True, null=True)

    class Meta:
        verbose_name = "сдача задания"
        verbose_name_plural = "сдачи заданий"
        db_table = "submissions"
        indexes = [
            # Очередь проверки: «непроверенное, свежее сверху».
            models.Index(fields=["status", "-submitted_at"], name="idx_submission_status"),
            models.Index(fields=["user", "assignment"], name="idx_submission_user_task"),
        ]

    def __str__(self):
        return f"{self.assignment_id} · {self.user_id} ({self.status})"


class ProjectTopic(models.Model):
    """Тема итогового проекта: то, что написано на билете.

    Темы — не задания, и это принципиально. Ведомость суммирует баллы всех заданий курса,
    поэтому двенадцать итоговых заданий обрушили бы отметку каждому студенту: выполнить он
    может только одно. Итоговое задание остаётся одно, с общими требованиями и общей
    сдачей, а тема лишь уточняет предметную область.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="project_topics",
        verbose_name="курс",
    )
    title = models.CharField(verbose_name="название", max_length=200)
    description = models.TextField(verbose_name="предметная область и требования")
    is_active = models.BooleanField(
        verbose_name="в наборе",
        default=True,
        help_text="Снятая тема больше не выпадает, но остаётся у тех, кто её уже вытянул.",
    )

    class Meta:
        verbose_name = "тема проекта"
        verbose_name_plural = "темы проектов"
        db_table = "project_topics"
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(fields=["course", "title"], name="uniq_topic_title_per_course")
        ]

    def __str__(self):
        return self.title


class ProjectDraw(models.Model):
    """Вытянутый билет: какая тема досталась студенту.

    Один билет на студента в курсе держит уникальное ограничение, а не проверка в коде:
    двойной щелчок и вторая вкладка приходят почти одновременно, и обе проверки успели бы
    увидеть, что билета ещё нет.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_draws",
        verbose_name="студент",
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="project_draws",
        verbose_name="курс",
    )
    # PROTECT: удаление темы молча отняло бы билет у студента, который по ней уже работает.
    # Чтобы тема больше не выпадала, её снимают с набора.
    topic = models.ForeignKey(
        ProjectTopic, on_delete=models.PROTECT, related_name="draws", verbose_name="тема"
    )
    drawn_at = models.DateTimeField(verbose_name="вытянут", default=timezone.now)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="changed_project_draws",
        blank=True,
        null=True,
        verbose_name="заменил",
    )
    note = models.TextField(verbose_name="причина замены", blank=True)

    class Meta:
        verbose_name = "билет итогового проекта"
        verbose_name_plural = "билеты итогового проекта"
        db_table = "project_draws"
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="uniq_draw_per_user_course")
        ]

    def __str__(self):
        return f"{self.user} · {self.topic}"

    def clean(self):
        if self.topic_id and self.topic.course_id != self.course_id:
            raise ValidationError({"topic": "Тема должна быть из этого же курса."})
