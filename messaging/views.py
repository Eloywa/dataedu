"""Переписка студента с преподавателем.

Живость сделана **опросом**, а не SSE с `LISTEN/NOTIFY`, как в Next-версии. Причина
не в лени: синхронный Django держит на каждое SSE-соединение отдельный рабочий поток
и отдельное соединение с базой, и тридцать открытых вкладок кладут пул. Асинхронный
контур (ASGI + Channels + Redis) снял бы это, но потянул бы за собой брокер и вторую
среду выполнения — ровно то, от чего этап 9.5 избавлялся ради простоты установки.
Опрос раз в несколько секунд для учебной переписки неотличим по ощущению и не стоит
ни одной новой зависимости.
"""

import uuid

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET, require_POST

from accounts.models import User
from courses.models import Course

from . import services


def _uuid_or_none(raw):
    """UUID из строки запроса. Мусор вместо идентификатора — не повод отдавать 500."""
    try:
        return uuid.UUID(str(raw))
    except (ValueError, TypeError, AttributeError):
        return None


def _peer_and_course(request):
    """Собеседник и курс из строки запроса. Возвращает `(peer, course)` или `(None, None)`."""
    peer_id = _uuid_or_none(request.GET.get("peer") or request.POST.get("peer"))
    course_id = _uuid_or_none(request.GET.get("course") or request.POST.get("course"))
    if peer_id is None or course_id is None:
        return None, None
    peer = User.objects.filter(pk=peer_id).first()
    course = Course.objects.filter(pk=course_id).first()
    if peer is None or course is None:
        return None, None
    return peer, course


def _safe_next(request, fallback):
    """Куда вернуться после отправки. Чужой хост в `next` — открытый редирект."""
    target = request.POST.get("next") or ""
    if target and url_has_allowed_host_and_scheme(
        target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return target
    return fallback


def _thread_payload(user, messages):
    return [
        {
            "id": str(m.id),
            "body": m.body,
            "mine": m.sender_id == user.pk,
            "at": m.created_at.isoformat(),
        }
        for m in messages
    ]


@login_required
def inbox(request):
    """Список диалогов и активный тред.

    Открыт и студенту, и преподавателю: страница показывает переписку того, кто
    её открыл, поэтому разделять представления по ролям незачем.
    """
    dialogs = services.conversations(request.user)

    peer, course = _peer_and_course(request)
    active = None
    if peer is not None and course is not None:
        active = next(
            (d for d in dialogs if d["peer"].pk == peer.pk and d["course"].pk == course.pk), None
        )
    if active is None and dialogs:
        active = dialogs[0]

    messages = []
    if active is not None:
        messages = services.thread(request.user, active["peer"], active["course"])
        services.mark_thread_read(request.user, active["peer"], active["course"])
        # Счётчик в списке слева должен совпасть с тем, что человек только что открыл.
        active["unread"] = 0

    return render(
        request,
        "messaging/inbox.html",
        {
            "dialogs": dialogs,
            "active": active,
            "messages": messages,
            "error": request.GET.get("error"),
        },
    )


@login_required
@require_POST
def send(request):
    """Отправить сообщение и вернуться туда, откуда пришли."""
    peer, course = _peer_and_course(request)
    fallback = reverse("messaging:inbox")
    if peer is not None and course is not None:
        fallback = f"{fallback}?peer={peer.pk}&course={course.pk}"
    target = _safe_next(request, fallback)

    if peer is None or course is None:
        raise Http404("Диалог не найден")

    _, error = services.send_message(request.user, peer, course, request.POST.get("body"))
    if error:
        sep = "&" if "?" in target else "?"
        return redirect(f"{target}{sep}error={error}#chat")
    return redirect(f"{target}#chat")


@login_required
@require_GET
def thread_json(request):
    """Тред в JSON — для дозагрузки без перезагрузки страницы.

    Заодно отмечает входящие прочитанными: открытый на экране тред и есть прочтение.
    Выборка идёт только по сообщениям, где пользователь — одна из сторон, поэтому
    подстановка чужого `peer` в строку запроса ничего не открывает.
    """
    peer, course = _peer_and_course(request)
    if peer is None or course is None:
        return JsonResponse({"ok": False, "messages": []}, status=400)

    messages = services.thread(request.user, peer, course)
    services.mark_thread_read(request.user, peer, course)
    return JsonResponse({"ok": True, "messages": _thread_payload(request.user, messages)})


@login_required
@require_GET
def unread_json(request):
    """Число непрочитанных — для живого бейджа в шапке."""
    return JsonResponse({"unread": services.unread_count(request.user)})
