from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from accounts import legal
from courses.models import Lesson
from gamification import services
from learning import reports
from learning.models import Enrollment, LessonProgress


def home(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, "core/home.html")

    if user.is_teacher:
        # Число непроверенных работ — единственная цифра, ради которой стоит идти
        # в базу с главной: она говорит, есть ли сегодня что разбирать.
        return render(
            request,
            "core/home_teacher.html",
            {"pending": reports.submission_summary(user)["pending"]},
        )

    # Студент: найти курс «в процессе» и следующий незавершённый урок
    enrollments = Enrollment.objects.filter(user=user).select_related("course").order_by("-enrolled_at")
    current = None
    for e in enrollments:
        course = e.course
        lessons = list(
            Lesson.objects.filter(module__course=course).order_by("module__order_index", "order_index")
        )
        if not lessons:
            continue
        completed = set(
            LessonProgress.objects.filter(
                user=user, lesson__module__course=course, status="completed"
            ).values_list("lesson_id", flat=True)
        )
        nxt = next((l for l in lessons if l.id not in completed), None)
        if nxt is not None:
            done, total = len(completed), len(lessons)
            current = {
                "course": course,
                "next_lesson": nxt,
                "done": done,
                "total": total,
                "pct": round(done * 100 / total),
            }
            break

    return render(
        request,
        "core/home_student.html",
        {"current": current, "enroll_count": enrollments.count()},
    )


def trainer(request):
    """SQL-тренажёр: страница-обёртка; вся работа — в браузере (PGlite)."""
    return render(request, "core/trainer.html")


@require_POST
def trainer_log(request):
    """Отметка об удачном запуске запроса: событие + «Первый запрос».

    SQL сюда не передаётся — запрос исполняется только в браузере; серверу нужен
    лишь факт запуска (аналитика этапа 11 и достижение).
    """
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False})
    achievement = services.record_sql_run(request.user)
    return JsonResponse({"ok": True, "achievement": achievement})


def privacy(request):
    """Политика обработки данных — публикуемый документ (ст. 18.1 ч. 2 152-ФЗ)."""
    return render(
        request,
        "legal/privacy.html",
        {"version": legal.PRIVACY_VERSION, "retention_days": settings.METRICS_RETENTION_DAYS},
    )


def terms(request):
    """Пользовательское соглашение."""
    return render(request, "legal/terms.html", {"version": legal.TERMS_VERSION})
