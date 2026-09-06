import hashlib
import hmac

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from gamification import services
from learning.models import Enrollment, LessonProgress, Reflection
from messaging import services as chat

from .models import Course, CourseRating, Lesson, Topic
from .resources import get_course_resources


def _progress(user, course):
    total = Lesson.objects.filter(module__course=course).count()
    if not total or not user.is_authenticated:
        return {"done": 0, "total": total, "pct": 0}
    done = LessonProgress.objects.filter(
        user=user, lesson__module__course=course, status="completed"
    ).count()
    return {"done": done, "total": total, "pct": round(done * 100 / total)}


def catalog(request):
    qs = (
        Course.objects.filter(is_published=True)
        .select_related("author")
        .annotate(
            rating_avg=Avg("ratings__rating"),
            rating_count=Count("ratings", distinct=True),
            lesson_count=Count("modules__lessons", distinct=True),
        )
    )
    q = request.GET.get("q", "").strip()
    level = request.GET.get("level", "")
    topic = request.GET.get("topic", "")
    sort = request.GET.get("sort", "popular")

    if q:
        qs = qs.filter(title__icontains=q)
    if level:
        qs = qs.filter(level=level)
    if topic:
        qs = qs.filter(course_topics__topic__code=topic)

    if sort == "rating":
        qs = qs.order_by("-rating_avg", "title")
    elif sort == "new":
        qs = qs.order_by("-created_at")
    else:
        qs = qs.order_by("-rating_count", "title")

    # Каталог разбит на страницы: «показать всё» работает, пока курсов десяток, и
    # перестаёт работать вместе с ростом платформы. Разбиение снимает и вторую
    # проблему — прогресс считается только для того, что видно на экране.
    page = Paginator(qs.distinct(), settings.PAGE_SIZE).get_page(request.GET.get("page"))
    courses = list(page.object_list)

    enrolled_ids = set()
    progress_by_course = {}
    if request.user.is_authenticated and courses:
        course_ids = [c.id for c in courses]
        enrolled_ids = set(
            Enrollment.objects.filter(user=request.user, course_id__in=course_ids).values_list(
                "course_id", flat=True
            )
        )
        # Пройденные уроки по всем курсам страницы — одним запросом вместо запроса
        # на карточку: раньше открытие каталога стоило по два обращения на курс.
        progress_by_course = dict(
            LessonProgress.objects.filter(
                user=request.user, lesson__module__course_id__in=course_ids, status="completed"
            )
            .values_list("lesson__module__course_id")
            .annotate(n=Count("id"))
        )

    for c in courses:
        c.is_enrolled = c.id in enrolled_ids
        if c.is_enrolled:
            done = progress_by_course.get(c.id, 0)
            total = c.lesson_count or 0
            c.prog = {"done": done, "total": total, "pct": round(done * 100 / total) if total else 0}
        else:
            c.prog = None

    return render(
        request,
        "courses/catalog.html",
        {
            "courses": courses,
            "page": page,
            "topics": Topic.objects.order_by("name"),
            "q": q,
            "level": level,
            "topic": topic,
            "sort": sort,
        },
    )


def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.filter(is_published=True).select_related("author"), slug=slug
    )
    modules = list(course.modules.prefetch_related("lessons").all())

    completed = set()
    enrolled = False
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
        completed = set(
            LessonProgress.objects.filter(
                user=request.user, lesson__module__course=course, status="completed"
            ).values_list("lesson_id", flat=True)
        )

    # Последовательное открытие недель: модуль доступен, когда предыдущий пройден.
    gating = services.course_gating(request.user, course, request.user.is_authenticated and request.user.is_teacher)
    prev_title = None
    ordered_lessons = []
    for m in modules:
        m.gate = gating[m.id]
        m.prev_title = prev_title
        prev_title = m.title
        for lesson in m.lessons.all():
            lesson.done = lesson.id in completed
            if m.gate["unlocked"]:
                ordered_lessons.append(lesson)

    next_lesson = next((l for l in ordered_lessons if not l.done), None)
    if next_lesson is None and ordered_lessons:
        next_lesson = ordered_lessons[0]

    agg = course.ratings.aggregate(avg=Avg("rating"), cnt=Count("id"))
    reviews = list(course.ratings.select_related("user").order_by("-created_at")[:20])
    my_rating = (
        course.ratings.filter(user=request.user).first() if request.user.is_authenticated else None
    )

    progress = _progress(request.user, course) if request.user.is_authenticated else None

    # Вопрос преподавателю прямо со страницы курса: собеседник — автор курса.
    # Виджет показывается только записанному студенту: у преподавателя для этого
    # есть инбокс, а незаписанному писать не о чем.
    chat_peer = None
    chat_messages = []
    if enrolled and request.user.is_authenticated and not request.user.is_teacher:
        chat_peer = chat.teacher_for(course)
        if chat_peer is not None:
            chat_messages = chat.thread(request.user, chat_peer, course)
            chat.mark_thread_read(request.user, chat_peer, course)

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            "modules": modules,
            "enrolled": enrolled,
            "progress": progress,
            "next_lesson": next_lesson,
            "resources": get_course_resources(slug),
            "rating_avg": agg["avg"],
            "rating_count": agg["cnt"],
            "reviews": reviews,
            "my_rating": my_rating,
            "chat_peer": chat_peer,
            "chat_messages": chat_messages,
            "chat_error": request.GET.get("error"),
            # Сертификат открывается только при полном прохождении — см. `certificate`.
            "certificate_ready": bool(enrolled and progress and progress["pct"] >= 100),
        },
    )


def certificate_code(user_id, course_id):
    """Проверочный код сертификата — детерминированно из пользователя и курса.

    Код не хранится в базе: он однозначно восстанавливается из той же пары, что
    его породила, и хранить нечего. Соль — `SECRET_KEY`, поэтому по коду нельзя
    восстановить идентификаторы, а подобрать код к чужой паре, не зная ключа,
    нельзя. Длина — 8 символов: достаточно, чтобы код читался с бумаги и не
    совпадал случайно у двух выпускников курса.
    """
    digest = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        f"{user_id}:{course_id}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return "DE-" + digest[:8].upper()


@login_required
def certificate(request, slug):
    """Сертификат о прохождении курса — открывается при 100% пройденных уроков.

    Печать штатная, браузерная (Ctrl+P), правила — в `@media print`: библиотека
    генерации PDF сюда не заводится по той же причине, что и в ведомости (этап 11.5) —
    системные зависимости ломают простоту установки.
    """
    course = get_object_or_404(Course.objects.filter(is_published=True).select_related("author"), slug=slug)
    enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    progress = _progress(request.user, course)

    if not enrolled or progress["pct"] < 100:
        return render(
            request,
            "courses/certificate_locked.html",
            {"course": course, "progress": progress, "enrolled": enrolled},
            status=403,
        )

    # Дата завершения — когда закрыт последний урок курса, а не «сегодня»: сертификат
    # должен показывать одну и ту же дату при каждом открытии.
    last_done = (
        LessonProgress.objects.filter(
            user=request.user, lesson__module__course=course, status="completed"
        )
        .order_by("-completed_at")
        .values_list("completed_at", flat=True)
        .first()
    )

    return render(
        request,
        "courses/certificate.html",
        {
            "course": course,
            "issued_at": last_done or timezone.now(),
            "lesson_count": progress["total"],
            "code": certificate_code(request.user.pk, course.pk),
        },
    )


@login_required
def enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    if request.method == "POST":
        Enrollment.objects.get_or_create(
            user=request.user, course=course, defaults={"status": "active"}
        )
    return redirect("courses:course_detail", slug=slug)


@login_required
def submit_review(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    if request.method == "POST":
        try:
            rating = int(request.POST.get("rating", "0"))
        except ValueError:
            rating = 0
        comment = request.POST.get("comment", "").strip()
        if 1 <= rating <= 5:
            CourseRating.objects.update_or_create(
                user=request.user,
                course=course,
                defaults={"rating": rating, "comment": comment or None},
            )
    return redirect("courses:course_detail", slug=slug)


def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson.objects.select_related("module__course"), id=lesson_id)
    course = lesson.module.course

    gating = services.course_gating(request.user, course, request.user.is_authenticated and request.user.is_teacher)
    gate = gating.get(lesson.module_id)
    if gate and not gate["unlocked"]:
        modules = list(course.modules.all())
        idx = next((i for i, m in enumerate(modules) if m.id == lesson.module_id), 0)
        return render(
            request,
            "lessons/lesson_locked.html",
            {
                "course": course,
                "lesson": lesson,
                "prev_module": modules[idx - 1] if idx > 0 else None,
            },
        )

    ordered = list(
        Lesson.objects.filter(module__course=course).order_by("module__order_index", "order_index")
    )
    idx = next((i for i, l in enumerate(ordered) if l.id == lesson.id), 0)
    prev_lesson = ordered[idx - 1] if idx > 0 else None
    next_lesson = ordered[idx + 1] if idx < len(ordered) - 1 else None

    done = False
    if request.user.is_authenticated:
        done = LessonProgress.objects.filter(
            user=request.user, lesson=lesson, status="completed"
        ).exists()

    test = lesson.tests.first()
    best_attempt = None
    if test and request.user.is_authenticated:
        best_attempt = test.attempts.filter(user=request.user).order_by("-score").first()

    # Рефлексия: своя, если уже заполнена — форма показывается с прежними ответами.
    reflection = None
    if request.user.is_authenticated and not request.user.is_teacher:
        reflection = Reflection.objects.filter(user=request.user, lesson=lesson).first()

    return render(
        request,
        "lessons/lesson_detail.html",
        {
            "lesson": lesson,
            "course": course,
            "prev_lesson": prev_lesson,
            "next_lesson": next_lesson,
            "done": done,
            "resources": get_course_resources(course.slug),
            "test": test,
            "best_attempt": best_attempt,
            "reflection": reflection,
            "reflection_saved": request.GET.get("reflection") == "saved",
            "reflection_invalid": request.GET.get("reflection") == "invalid",
            "rating_scale": [1, 2, 3, 4, 5],
        },
    )


@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == "POST":
        # Статус, XP урока, событие и «Первый шаг» — одной операцией (идемпотентно).
        services.complete_lesson(request.user, lesson)
    return redirect("courses:lesson_detail", lesson_id=lesson_id)


def _clamp_rating(raw):
    """Оценка 1–5 или None. Значение приходит из формы, поэтому не доверяем."""
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return None
    return value if 1 <= value <= 5 else None


@login_required
@require_POST
def submit_reflection(request, lesson_id):
    """Сохранить рефлексию по уроку (одна на пару «студент — урок», можно менять).

    Преподаватель рефлексию не заполняет: это инструмент обратной связи от студента,
    и его оценки исказили бы данные исследования.
    """
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.user.is_teacher:
        return redirect("courses:lesson_detail", lesson_id=lesson_id)

    clarity = _clamp_rating(request.POST.get("clarity"))
    difficulty = _clamp_rating(request.POST.get("difficulty"))
    if clarity is None or difficulty is None:
        return redirect(
            reverse("courses:lesson_detail", args=[lesson_id]) + "?reflection=invalid#reflection"
        )

    _, created = Reflection.objects.update_or_create(
        user=request.user,
        lesson=lesson,
        defaults={
            "clarity_rating": clarity,
            "difficulty_rating": difficulty,
            "comment": (request.POST.get("comment") or "").strip() or None,
            "comment_is_anonymous": request.POST.get("anonymous") == "on",
            "updated_at": timezone.now(),
        },
    )
    services.record_reflection(request.user, lesson, is_new=created)
    return redirect(
        reverse("courses:lesson_detail", args=[lesson_id]) + "?reflection=saved#reflection"
    )
