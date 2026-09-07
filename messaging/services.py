"""Логика переписки: кто кому вправе писать, тред, диалоги, непрочитанное.

Отделено от представлений, чтобы правила доставки проверялись без HTTP: «студент
студенту писать не может» — это правило предметной области, а не веб-слоя.
"""

from django.db.models import Case, Count, F, Q, UUIDField, When, Window
from django.db.models.functions import RowNumber
from django.utils import timezone

from .models import Message

# Верхняя граница длины сообщения. Чат здесь — короткий вопрос преподавателю, а не
# файлообменник; ограничение заодно защищает страницу от полотна на мегабайт.
MAX_BODY = 2000

# Сколько сообщений показывать в треде. Переписка по одному предмету за семестр
# столько не набирает, а верхняя граница защищает страницу от разрастания.
THREAD_LIMIT = 300


def can_write(sender, recipient):
    """Вправе ли `sender` написать `recipient`. Возвращает текст ошибки или None.

    Правило одно: в паре обязан быть преподаватель. Переписка студент↔студент
    закрыта намеренно — платформа учебная, и приватный обмен между студентами
    к учебному процессу отношения не имеет, а модерировать его никто не будет.
    """
    if recipient is None or not recipient.is_active:
        return "Получатель недоступен"
    if recipient.pk == sender.pk:
        return "Нельзя писать самому себе"
    if not sender.is_teacher and not recipient.is_teacher:
        return "Писать можно только преподавателю"
    return None


def send_message(sender, recipient, course, body):
    """Отправить сообщение. Возвращает `(message, error)` — ровно одно не None."""
    text = (body or "").strip()
    if not text:
        return None, "Пустое сообщение"
    if len(text) > MAX_BODY:
        return None, f"Сообщение длиннее {MAX_BODY} символов"

    error = can_write(sender, recipient)
    if error:
        return None, error

    message = Message.objects.create(
        sender=sender, recipient=recipient, course=course, body=text, created_at=timezone.now()
    )
    return message, None


def thread(user, peer, course, limit=THREAD_LIMIT):
    """Переписка двух собеседников по одному курсу, по возрастанию времени.

    Срез берётся с конца: при длинной переписке нужны последние сообщения, а не
    первые, поэтому запрос идёт по убыванию и разворачивается уже в Python.
    """
    qs = (
        Message.objects.filter(course=course)
        .filter(Q(sender=user, recipient=peer) | Q(sender=peer, recipient=user))
        .order_by("-created_at")[:limit]
    )
    return list(reversed(list(qs)))


def mark_thread_read(user, peer, course):
    """Отметить прочитанными входящие от собеседника по этому курсу."""
    return Message.objects.filter(
        recipient=user, sender=peer, course=course, read_at__isnull=True
    ).update(read_at=timezone.now())


def unread_count(user):
    """Сколько всего непрочитанных — для бейджа в шапке."""
    if not user.is_authenticated:
        return 0
    return Message.objects.filter(recipient=user, read_at__isnull=True).count()


def conversations(user):
    """Диалоги пользователя: пара «собеседник + курс», последнее сообщение, непрочитанные.

    Три запроса независимо от объёма переписки. Наивная реализация — «выбрать все
    свои сообщения и свернуть в Python» — работает ровно до первого преподавателя,
    у которого за семестр накопилось несколько тысяч сообщений: страница инбокса
    начинает вытаскивать их все, чтобы показать двадцать строк.

    Последнее сообщение в каждом диалоге ищет оконная функция: нумеруем сообщения
    внутри пары «собеседник + курс» по убыванию времени и берём первое. Собеседник
    вычисляется выражением `CASE`, потому что в одной паре пользователь бывает и
    отправителем, и получателем.
    """
    peer_expr = Case(
        When(sender_id=user.pk, then=F("recipient_id")),
        default=F("sender_id"),
        output_field=UUIDField(),
    )

    last_ids = list(
        Message.objects.filter(Q(sender=user) | Q(recipient=user))
        .exclude(course__isnull=True)
        .annotate(peer_id=peer_expr)
        .annotate(
            row=Window(
                expression=RowNumber(),
                partition_by=[F("peer_id"), F("course_id")],
                order_by=F("created_at").desc(),
            )
        )
        .filter(row=1)
        .values_list("id", flat=True)
    )
    if not last_ids:
        return []

    unread = {
        (r["sender_id"], r["course_id"]): r["n"]
        for r in Message.objects.filter(recipient=user, read_at__isnull=True)
        .exclude(course__isnull=True)
        .values("sender_id", "course_id")
        .annotate(n=Count("id"))
    }

    dialogs = []
    for m in (
        Message.objects.filter(id__in=last_ids)
        .select_related("sender", "recipient", "course")
        .order_by("-created_at")
    ):
        peer = m.recipient if m.sender_id == user.pk else m.sender
        dialogs.append(
            {
                "peer": peer,
                "course": m.course,
                "last_body": m.body,
                "last_at": m.created_at,
                "unread": unread.get((peer.pk, m.course_id), 0),
            }
        )
    return dialogs


def teacher_for(course):
    """Кому студент пишет по курсу.

    Сначала автор — он за курс отвечает. Если автор не задан или его учётная
    запись выключена, письмо уходит соавтору: с появлением соавторства курс
    может остаться без автора, и вопрос студента не должен уходить в никуда.
    Возвращает None, если писать некому — тогда форма ответа не показывается.
    """

    def suitable(user):
        return user is not None and user.is_active and user.is_teacher

    if suitable(course.author):
        return course.author
    return next((u for u in course.coauthors.all() if suitable(u)), None)
