import json

from django.conf import settings
from django.db.models import Count
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from accounts import legal
from assessments.models import Assignment, Question, Test
from courses.models import Course, Lesson, Module
from courses.theory import render_theory
from gamification import services
from learning import reports
from learning.models import Enrollment, LessonProgress


def home(request):
    user = request.user
    if not user.is_authenticated:
        # Цифры на лендинге берутся из базы, а не вписываются в шаблон руками:
        # прежние «9 недель · 18 уроков» разошлись с содержимым и обещали меньше,
        # чем платформа на самом деле даёт.
        return render(
            request,
            "core/home.html",
            {
                "course_count": Course.objects.filter(is_published=True).count(),
                "lesson_count": Lesson.objects.filter(module__course__is_published=True).count(),
                "test_count": Test.objects.filter(
                    lesson__module__course__is_published=True
                ).count(),
            },
        )

    if user.is_teacher:
        # Число непроверенных работ — единственная цифра, ради которой стоит идти
        # в базу с главной: она говорит, есть ли сегодня что разбирать.
        return render(
            request,
            "core/home_teacher.html",
            {"pending": reports.submission_summary(user)["pending"]},
        )

    # Студент: найти курс «в процессе» и следующий незавершённый урок
    enrollments = (
        Enrollment.objects.filter(user=user).select_related("course").order_by("-enrolled_at")
    )
    current = None
    for e in enrollments:
        course = e.course
        lessons = list(
            Lesson.objects.filter(module__course=course).order_by(
                "module__order_index", "order_index"
            )
        )
        if not lessons:
            continue
        completed = set(
            LessonProgress.objects.filter(
                user=user, lesson__module__course=course, status="completed"
            ).values_list("lesson_id", flat=True)
        )
        nxt = next((item for item in lessons if item.id not in completed), None)
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
    """Отметка о работе в тренажёре: удачный запуск или класс ошибки.

    Ни SQL, ни текст ошибки сюда не передаются — запрос исполняется только в
    браузере, а в тексте ошибки PostgreSQL оказываются придуманные студентом
    данные. Серверу нужен факт запуска (аналитика этапа 11 и достижение
    «Первый запрос») и код класса ошибки для отчёта «на чём спотыкаются».
    """
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False})

    # Тело может не прийти вовсе: до этапа 15 отметка отправлялась пустым POST,
    # и открытая у студента вкладка со старым скриптом не должна падать.
    try:
        payload = json.loads(request.body or b"{}")
    except (ValueError, TypeError):
        payload = {}

    if payload.get("event") == "error":
        services.record_sql_error(request.user, payload.get("error"))
        return JsonResponse({"ok": True})

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


def styleguide(request):
    """Страница-пример: все базовые компоненты редизайна в одном месте.

    Нужна по двум причинам. Первая — дизайн правится здесь, а не на семи разных
    экранах: видно сразу, что кнопка, метка статуса и таблица сделаны в одной
    системе. Вторая — обе темы и узкая ширина проверяются одним открытием
    страницы, а не обходом платформы.

    Открыта только в разработке и сотрудникам: это внутренний инструмент, и
    в каталоге страниц платформы ему места нет.
    """
    if not settings.DEBUG and not request.user.is_staff:
        raise Http404

    # Содержимое берётся из базы, а не выдумывается: пример компонента на
    # придуманном тексте врёт о длине строк и о том, как раскладка держит
    # настоящие названия вроде «Проектирование БД и ER-модель».
    course = Course.objects.filter(is_published=True).order_by("title").first()
    lessons = (
        list(
            Lesson.objects.filter(module__course=course)
            .select_related("module")
            .order_by("module__order_index", "order_index")[:3]
        )
        if course
        else []
    )
    modules = (
        list(
            Module.objects.filter(course=course)
            .annotate(lesson_count=Count("lessons"))
            .order_by("order_index")[:3]
        )
        if course
        else []
    )
    assignment = (
        Assignment.objects.filter(type="sql").exclude(setup_sql="").order_by("title").first()
    )
    question = (
        Question.objects.filter(test__lesson__module__course=course)
        .prefetch_related("options")
        .order_by("order_index")
        .first()
    )

    # Врезка показывается прогнанной через тот же рендер, что и теория урока:
    # иначе страница-пример доказывала бы только то, что CSS написан, а не то,
    # что разметка из markdown доходит до него.
    sample_html, _ = render_theory(
        '!!! note "Обратите внимание"\n'
        "    Запрос выполняется в браузере: база PostgreSQL собрана в WebAssembly\n"
        "    и живёт на вашем устройстве. Сервер её не видит.\n"
    )

    return render(
        request,
        "core/styleguide.html",
        {
            "course": course,
            "lessons": lessons,
            "modules": modules,
            "assignment": assignment,
            "question": question,
            "sample_html": sample_html,
        },
    )
