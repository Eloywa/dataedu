import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey("courses.Lesson", on_delete=models.CASCADE, related_name="tests")
    title = models.CharField(max_length=200)
    pass_score = models.IntegerField()
    time_limit_sec = models.IntegerField(blank=True, null=True)

    class Meta:
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
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    type = models.CharField(max_length=50)
    points = models.IntegerField()
    order_index = models.IntegerField()
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
        db_table = "questions"
        ordering = ["order_index"]

    def __str__(self):
        return self.text[:60]


class AnswerOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order_index = models.IntegerField()

    class Meta:
        db_table = "answer_options"
        ordering = ["order_index"]

    def __str__(self):
        return self.text[:60]


class TestAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="test_attempts")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="attempts")
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_passed = models.BooleanField(blank=True, null=True)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(blank=True, null=True)

    class Meta:
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
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="submissions")
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.SET_NULL, blank=True, null=True)
    text_answer = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = "answer_submissions"


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


class Assignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="assignments")
    lesson = models.ForeignKey(
        "courses.Lesson", on_delete=models.SET_NULL, related_name="assignments", blank=True, null=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    expected_sql = models.TextField(blank=True, null=True)
    # Заготовка данных для задачи (создаётся в PGlite у студента и при расчёте эталона)
    setup_sql = models.TextField(blank=True, null=True)
    # Предрасчитанный эталонный результат: {"columns": [...], "rows": [[...], ...]}
    expected_result = models.JSONField(blank=True, null=True)
    max_score = models.IntegerField()
    is_final = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    objects = AssignmentQuerySet.as_manager()

    class Meta:
        db_table = "assignments"
        indexes = [
            # Очередь проверки и список заданий всегда идут в разрезе курса и типа.
            models.Index(fields=["course", "type"], name="idx_assignment_course_type"),
        ]

    def __str__(self):
        return self.title

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
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions")
    sql_query = models.TextField(blank=True, null=True)
    file_url = models.TextField(blank=True, null=True)
    text_answer = models.TextField(blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        db_column="graded_by",
        related_name="graded_submissions",
        blank=True,
        null=True,
    )
    submitted_at = models.DateTimeField(default=timezone.now)
    graded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "submissions"
        indexes = [
            # Очередь проверки: «непроверенное, свежее сверху».
            models.Index(fields=["status", "-submitted_at"], name="idx_submission_status"),
            models.Index(fields=["user", "assignment"], name="idx_submission_user_task"),
        ]
