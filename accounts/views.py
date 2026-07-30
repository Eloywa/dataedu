import json

from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .legal import VERSIONS
from .models import Consent, Role, User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get("next") or "core:home")
        error = "Неверный логин или пароль."

    return render(request, "accounts/login.html", {"error": error})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("core:home")


def register_view(request):
    """Регистрация.

    Запрашивается минимум: логин и пароль. Отображаемое имя необязательно и может быть
    псевдонимом, email необязателен — настоящее ФИО платформа не спрашивает вовсе.
    Согласие с политикой обработки данных обязательно и фиксируется с версией документа.

    На апробации свободную регистрацию закрывают (`REGISTRATION_OPEN=0`), а логины
    выдают пачкой командой `create_pilot_accounts`.
    """
    if request.user.is_authenticated:
        return redirect("core:home")

    if not settings.REGISTRATION_OPEN:
        return render(request, "accounts/register_closed.html", status=403)

    error = None
    form = {}
    if request.method == "POST":
        form = {
            "username": request.POST.get("username", "").strip(),
            "display_name": request.POST.get("display_name", "").strip(),
            "email": request.POST.get("email", "").strip().lower(),
        }
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm", "")
        consent = request.POST.get("consent") == "on"

        if not form["username"] or not password:
            error = "Логин и пароль обязательны."
        elif not all(ch.isalnum() or ch in "._-" for ch in form["username"]):
            error = "Логин может содержать только латиницу, цифры, точку, дефис и подчёркивание."
        elif len(password) < 8:
            error = "Пароль должен быть не короче 8 символов."
        elif password != confirm:
            error = "Пароли не совпадают."
        elif not consent:
            error = "Без согласия с политикой обработки данных регистрация невозможна."
        elif User.objects.filter(username__iexact=form["username"]).exists():
            error = "Этот логин уже занят."
        elif form["email"] and User.objects.filter(email__iexact=form["email"]).exists():
            error = "Этот email уже указан в другой учётной записи."
        else:
            role = Role.objects.filter(code="student").first()
            with transaction.atomic():
                user = User.objects.create_user(
                    username=form["username"],
                    password=password,
                    email=form["email"] or None,
                    display_name=form["display_name"],
                    role=role,
                )
                # Согласие фиксируется в той же транзакции: аккаунта без записи о
                # согласии в базе быть не должно.
                for document, version in VERSIONS.items():
                    Consent.objects.create(user=user, document=document, version=version)
            login(request, user)
            return redirect("core:home")

    return render(request, "accounts/register.html", {"error": error, "form": form})


@login_required
def settings_view(request):
    error = None
    done = False
    if request.method == "POST":
        current = request.POST.get("current", "")
        new = request.POST.get("new", "")
        confirm = request.POST.get("confirm", "")

        if not request.user.check_password(current):
            error = "Текущий пароль неверный."
        elif len(new) < 8:
            error = "Новый пароль должен быть не короче 8 символов."
        elif new != confirm:
            error = "Пароли не совпадают."
        elif new == current:
            error = "Новый пароль совпадает с текущим."
        else:
            request.user.set_password(new)
            request.user.save(update_fields=["password"])
            update_session_auth_hash(request, request.user)  # не разлогинивать
            done = True

    return render(
        request,
        "accounts/settings.html",
        {
            "error": error,
            "done": done,
            "consents": request.user.consents.order_by("document", "-granted_at"),
            "retention_days": settings.METRICS_RETENTION_DAYS,
        },
    )


def _collect_user_data(user):
    """Собрать всё, что платформа хранит об этом пользователе.

    Право на доступ к своим данным (ст. 14 152-ФЗ) реализуется выгрузкой в JSON —
    машиночитаемо и полно. Пароль (его хеш) в выгрузку не попадает.
    """
    return {
        "выгружено": timezone.now().isoformat(),
        "учётная_запись": {
            "логин": user.username,
            "отображаемое_имя": user.display_name,
            "email": user.email,
            "роль": user.role.name if user.role else None,
            "xp": user.xp,
            "уровень": user.level,
            "создана": user.created_at.isoformat() if user.created_at else None,
            "последний_вход": user.last_seen_at.isoformat() if user.last_seen_at else None,
        },
        "согласия": [
            {
                "документ": c.get_document_display(),
                "версия": c.version,
                "дано": c.granted_at.isoformat(),
            }
            for c in user.consents.order_by("granted_at")
        ],
        "записи_на_курсы": [
            {
                "курс": e.course.title,
                "статус": e.status,
                "записан": e.enrolled_at.isoformat() if e.enrolled_at else None,
                "завершён": e.completed_at.isoformat() if e.completed_at else None,
            }
            for e in user.enrollments.select_related("course")
        ],
        "пройденные_уроки": [
            {
                "урок": p.lesson.title,
                "статус": p.status,
                "времени_сек": p.time_spent_sec,
                "заходов": p.visits,
                "завершён": p.completed_at.isoformat() if p.completed_at else None,
            }
            for p in user.lesson_progress.select_related("lesson")
        ],
        "попытки_тестов": [
            {
                "тест": a.test.title,
                "балл": str(a.score) if a.score is not None else None,
                "зачтён": a.is_passed,
                "начата": a.started_at.isoformat() if a.started_at else None,
                "завершена": a.finished_at.isoformat() if a.finished_at else None,
            }
            for a in user.test_attempts.select_related("test")
        ],
        "решения_заданий": [
            {
                "задание": s.assignment.title,
                "sql": s.sql_query,
                "балл": str(s.score) if s.score is not None else None,
                "статус": s.status,
                "отправлено": s.submitted_at.isoformat() if s.submitted_at else None,
            }
            for s in user.submissions.select_related("assignment")
        ],
        "рефлексии": [
            {
                "урок": r.lesson.title if r.lesson else None,
                "понятность": r.clarity_rating,
                "субъективная_трудность": r.difficulty_rating,
                "комментарий": r.comment,
                "создана": r.created_at.isoformat() if r.created_at else None,
            }
            for r in user.reflections.select_related("lesson")
        ],
        "достижения": [
            {
                "достижение": ua.achievement.title,
                "получено": ua.awarded_at.isoformat() if ua.awarded_at else None,
            }
            for ua in user.achievements.select_related("achievement")
        ],
        "оценки_курсов": [
            {
                "курс": r.course.title,
                "оценка": r.rating,
                "отзыв": r.comment,
            }
            for r in user.course_ratings.select_related("course")
        ],
        "лента_активности": [
            {
                "тип": a.type,
                "объект": a.entity_type,
                "детали": a.metadata,
                "когда": a.created_at.isoformat() if a.created_at else None,
            }
            for a in user.activities.order_by("created_at")
        ],
    }


@login_required
def export_data(request):
    """Выгрузка своих данных одним JSON-файлом."""
    payload = json.dumps(_collect_user_data(request.user), ensure_ascii=False, indent=2)
    response = HttpResponse(payload, content_type="application/json; charset=utf-8")
    stamp = timezone.now().strftime("%Y-%m-%d")
    response["Content-Disposition"] = (
        f'attachment; filename="dataedu-{request.user.username}-{stamp}.json"'
    )
    return response


@login_required
def delete_account(request):
    """Удаление своей учётной записи (право на прекращение обработки, ст. 20-21 152-ФЗ).

    Удаление настоящее, не «мягкое»: все учебные записи уходят каскадом
    (записи на курсы, прогресс, попытки, решения, рефлексии, достижения, лента).
    Курсы, если пользователь был их автором, остаются — авторство обнуляется
    (`SET_NULL`), иначе удаление преподавателя снесло бы учебный материал у всех.

    Требуется подтверждение паролем: удаление необратимо.
    """
    error = None
    if request.method == "POST":
        if not request.user.check_password(request.POST.get("password", "")):
            error = "Пароль неверный — учётная запись не удалена."
        elif request.POST.get("confirm") != "УДАЛИТЬ":
            error = "Для подтверждения введите слово УДАЛИТЬ."
        else:
            user = request.user
            logout(request)
            user.delete()
            return render(request, "accounts/deleted.html")

    return render(request, "accounts/delete_account.html", {"error": error})
