import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Message(models.Model):
    """Сообщение в переписке студента с преподавателем курса.

    Переписка привязана к **курсу**, а не только к паре собеседников: один студент
    может слушать у одного преподавателя два предмета, и общий тред смешал бы вопросы
    по разным дисциплинам. Пара «собеседник + курс» и образует диалог.

    `course` допускает NULL ради целостности при удалении курса (`SET_NULL`): переписка
    переживает курс, но в списке диалогов такие сообщения не показываются — диалог
    определяется курсом.

    Прочитанность хранится на самом сообщении (`read_at`), а не счётчиком у диалога:
    счётчик пришлось бы держать в согласии с таблицей, а так «непрочитано» —
    это просто выборка по `read_at IS NULL`.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="отправитель",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
        verbose_name="получатель",
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.SET_NULL,
        related_name="messages",
        blank=True,
        null=True,
        verbose_name="курс",
    )
    body = models.TextField("текст")
    created_at = models.DateTimeField("отправлено", default=timezone.now)
    read_at = models.DateTimeField("прочитано", blank=True, null=True)

    class Meta:
        db_table = "messages"
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["sender", "recipient", "created_at"], name="idx_messages_pair"),
            models.Index(fields=["recipient", "read_at"], name="idx_messages_recipient"),
        ]

    def __str__(self):
        return f"{self.sender_id} → {self.recipient_id}: {self.body[:40]}"
