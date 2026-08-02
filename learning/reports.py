"""Сбор данных для дашборда преподавателя.

Здесь только запросы и склейка; вся математика — в `learning/analytics.py`.
Разделение не косметическое: формулы риска и трудности проверяются отдельно от БД,
а здесь остаётся то, что можно проверить только на данных.

Все отчёты принимают `teacher` и **ограничены его курсами**: преподаватель видит
только своих студентов, как и в админке (§17.9). Суперпользователь видит всё.
"""

from django.db.models import Avg, Count, Max, Q
from django.utils import timezone

from assessments.models import AnswerSubmission, Assignment, Question, Submission, Test, TestAttempt
from courses.models import Course, Lesson
from learning.analytics import (
    compute_risk,
    divergence,
    final_score,
    grade_5,
    mastery_zone,
    objective_difficulty,
    pass_fail,
    risk_zone,
    subjective_difficulty,
)
from learning.models import Activity, Enrollment, LessonProgress, Reflection, StudyGroup


def visible_courses(teacher):
    """Курсы, которые преподаватель вправе видеть."""
    qs = Course.objects.all()
    if not teacher.is_superuser:
        qs = qs.filter(author=teacher)
    return qs.order_by("title")


def visible_groups(teacher):
    """Учебные группы, которыми распоряжается преподаватель."""
    qs = StudyGroup.objects.all()
    if not teacher.is_superuser:
        qs = qs.filter(teacher=teacher)
    return qs.order_by("name")


# --- Зоны риска --------------------------------------------------------------


def student_rows(teacher, course=None):
    """Строки таблицы студентов: прогресс, средний балл, простой, индекс риска."""
    courses = visible_courses(teacher)
    if course is not None:
        courses = courses.filter(pk=course.pk)
    course_ids = list(courses.values_list("id", flat=True))
    if not course_ids:
        return []

    lessons_per_course = dict(
        Lesson.objects.filter(module__course_id__in=course_ids)
        .values_list("module__course_id")
        .annotate(n=Count("id"))
    )

    enrollments = (
        Enrollment.objects.filter(course_id__in=course_ids)
        .select_related("user", "course")
        .order_by("user__username")
    )

    now = timezone.now()
    rows = []
    for e in enrollments:
        total = lessons_per_course.get(e.course_id, 0)
        done = LessonProgress.objects.filter(
            user=e.user, lesson__module__course_id=e.course_id, status="completed"
        ).count()
        completion = round(done * 100 / total) if total else 0

        avg_score = TestAttempt.objects.filter(
            user=e.user, test__lesson__module__course_id=e.course_id
        ).aggregate(v=Avg("score"))["v"]
        avg_score = round(float(avg_score)) if avg_score is not None else None

        last_event = (
            Activity.objects.filter(user=e.user).order_by("-created_at").values_list("created_at", flat=True).first()
        )
        days_inactive = (now - last_event).days if last_event else None

        risk = compute_risk(completion, avg_score, days_inactive)
        rows.append(
            {
                "user": e.user,
                "course": e.course,
                "completion": completion,
                "lessons_done": done,
                "lessons_total": total,
                "avg_score": avg_score,
                "days_inactive": days_inactive,
                "risk": risk,
                "zone": risk_zone(risk),
            }
        )

    rows.sort(key=lambda r: -r["risk"])
    return rows


def summarize(rows):
    """Сводка по таблице студентов для плиток дашборда."""
    if not rows:
        return {"total": 0, "high": 0, "medium": 0, "low": 0, "avg_completion": 0, "avg_risk": 0}
    high = sum(1 for r in rows if r["zone"]["tone"] == "danger")
    medium = sum(1 for r in rows if r["zone"]["tone"] == "warning")
    return {
        "total": len(rows),
        "high": high,
        "medium": medium,
        "low": len(rows) - high - medium,
        "avg_completion": round(sum(r["completion"] for r in rows) / len(rows)),
        "avg_risk": round(sum(r["risk"] for r in rows) / len(rows)),
    }


# --- Сопоставление объективной и субъективной трудности (ядро новизны) -------


def lesson_difficulty_rows(teacher, course=None):
    """Для каждого урока — объективная и субъективная трудность и их расхождение.

    Урок попадает в отчёт, только если по нему есть **обе** величины: сравнивать
    не с чем, если студенты не оставляли рефлексию или урок ещё никто не проходил.
    Число ответов (`n_reflections`) выводится рядом — при двух-трёх рефлексиях
    вывод нельзя считать надёжным, и преподаватель должен это видеть.
    """
    courses = visible_courses(teacher)
    if course is not None:
        courses = courses.filter(pk=course.pk)
    course_ids = list(courses.values_list("id", flat=True))
    if not course_ids:
        return []

    lessons = (
        Lesson.objects.filter(module__course_id__in=course_ids)
        .select_related("module", "module__course")
        .order_by("module__course__title", "module__order_index", "order_index")
    )

    rows = []
    for lesson in lessons:
        refl = Reflection.objects.filter(lesson=lesson).aggregate(
            n=Count("id"), difficulty=Avg("difficulty_rating"), clarity=Avg("clarity_rating")
        )
        if not refl["n"]:
            continue

        attempts = TestAttempt.objects.filter(test__lesson=lesson)
        avg_score = attempts.aggregate(v=Avg("score"))["v"]
        avg_score = float(avg_score) if avg_score is not None else None

        # Среднее число попыток на студента: сколько раз в среднем брались за тест.
        per_user = attempts.values("user_id").annotate(n=Count("id"))
        avg_attempts = (sum(x["n"] for x in per_user) / len(per_user)) if per_user else None

        subs = Submission.objects.filter(assignment__lesson=lesson)
        n_subs = subs.count()
        failed_share = (
            subs.filter(score__lt=1).count() / n_subs if n_subs else None
        )

        objective = objective_difficulty(avg_score, avg_attempts, failed_share)
        subjective = subjective_difficulty(refl["difficulty"])
        div = divergence(objective, subjective)

        rows.append(
            {
                "lesson": lesson,
                "course": lesson.module.course,
                "week": lesson.module.week_number,
                "n_reflections": refl["n"],
                "clarity": round(refl["clarity"], 1) if refl["clarity"] else None,
                "subjective": subjective,
                "objective": objective,
                "avg_score": round(avg_score) if avg_score is not None else None,
                "avg_attempts": round(avg_attempts, 1) if avg_attempts else None,
                "failed_share": round(failed_share * 100) if failed_share is not None else None,
                "divergence": div,
            }
        )

    # Сначала самые расходящиеся — именно они требуют внимания преподавателя.
    rows.sort(key=lambda r: -abs(r["divergence"]["delta"]) if r["divergence"] else 0)
    return rows


# --- Анализ вопросов и карта тем --------------------------------------------


def item_analysis_rows(teacher, limit=25):
    """Доля верных ответов по каждому вопросу — самые трудные сверху."""
    course_ids = list(visible_courses(teacher).values_list("id", flat=True))
    qs = (
        Question.objects.filter(test__lesson__module__course_id__in=course_ids)
        .annotate(
            responses=Count("submissions"),
            correct=Count("submissions", filter=Q(submissions__is_correct=True)),
        )
        .filter(responses__gt=0)
        .select_related("test__lesson", "test__lesson__module__course", "topic")
    )
    rows = []
    for q in qs:
        pct = round(q.correct * 100 / q.responses)
        rows.append(
            {
                "question": q,
                "lesson": q.test.lesson,
                "course": q.test.lesson.module.course if q.test.lesson else None,
                "topic": q.topic,
                "responses": q.responses,
                "pct_correct": pct,
                "zone": mastery_zone(pct),
            }
        )
    rows.sort(key=lambda r: (r["pct_correct"], -r["responses"]))
    return rows[:limit]


def topic_mastery_rows(teacher):
    """Карта освоения по темам: доля верных ответов на вопросы каждой темы."""
    course_ids = list(visible_courses(teacher).values_list("id", flat=True))
    base = AnswerSubmission.objects.filter(
        question__test__lesson__module__course_id__in=course_ids
    )

    rows = []
    agg = (
        base.exclude(question__topic__isnull=True)
        .values("question__topic__id", "question__topic__name")
        .annotate(
            responses=Count("id"),
            correct=Count("id", filter=Q(is_correct=True)),
            questions=Count("question_id", distinct=True),
        )
        .order_by()
    )
    for a in agg:
        pct = round(a["correct"] * 100 / a["responses"]) if a["responses"] else None
        rows.append(
            {
                "topic_name": a["question__topic__name"],
                "questions": a["questions"],
                "responses": a["responses"],
                "pct_correct": pct,
                "zone": mastery_zone(pct),
            }
        )
    rows.sort(key=lambda r: r["pct_correct"] if r["pct_correct"] is not None else 999)

    scoped = Question.objects.filter(test__lesson__module__course_id__in=course_ids)
    total = scoped.count()
    untagged = scoped.filter(topic__isnull=True).count()
    return rows, {"untagged": untagged, "tagged": total - untagged, "total": total}


def activity_breakdown(teacher):
    """Разбивка событий по типам — сколько чего происходило."""
    LABELS = {
        "login": "Входы",
        "lesson_view": "Просмотры уроков",
        "lesson_complete": "Завершения уроков",
        "test_finish": "Завершено тестов",
        "sql_run": "Запросы в тренажёре",
        "submission": "Сдачи заданий",
        "reflection": "Рефлексии",
        "achievement": "Достижения",
    }
    course_ids = list(visible_courses(teacher).values_list("id", flat=True))
    user_ids = Enrollment.objects.filter(course_id__in=course_ids).values_list("user_id", flat=True)
    agg = (
        Activity.objects.filter(user_id__in=user_ids)
        .values("type")
        .annotate(n=Count("id"))
        .order_by("-n")
    )
    return [{"label": LABELS.get(a["type"], a["type"]), "n": a["n"]} for a in agg]


# --- Ведомость по группе (этап 11.5) ----------------------------------------


def gradebook_rows(course, group=None):
    """Строки ведомости: что каждый студент сдал по курсу и какая выходит отметка.

    Курс обязателен — ведомость сдаётся по дисциплине, «итог по всем курсам сразу»
    смысла не имеет. Группа необязательна: без неё в отчёт попадают все записанные
    на курс, с ней — пересечение состава группы и записанных.

    **Считается не среднее по попыткам, а лучший результат по каждому тесту.** На
    дашборде риска среднее уместно (там важно, как студент работал), в ведомости —
    нет: пересдача существует ровно для того, чтобы улучшить отметку. Тест, за
    который студент не брался, идёт нулём — это и есть «не сдал».

    Права доступа здесь не проверяются: вызывающий обязан передать курс и группу,
    уже отфильтрованные через `visible_courses` / `visible_groups`.
    """
    lesson_ids = list(Lesson.objects.filter(module__course=course).values_list("id", flat=True))
    test_ids = list(Test.objects.filter(lesson__module__course=course).values_list("id", flat=True))
    assignments = dict(Assignment.objects.filter(course=course).values_list("id", "max_score"))
    max_total = sum(assignments.values())

    users = {
        e.user_id: e.user
        for e in Enrollment.objects.filter(course=course).select_related("user")
    }
    if group is not None:
        in_group = set(group.students.values_list("id", flat=True))
        users = {uid: u for uid, u in users.items() if uid in in_group}
    user_ids = list(users)
    if not user_ids:
        return []

    # Дальше — по одному запросу на составляющую вместо запроса на студента:
    # в группе три десятка человек, и построчные обращения к БД дали бы сотни запросов.
    done_lessons = dict(
        LessonProgress.objects.filter(user_id__in=user_ids, lesson_id__in=lesson_ids, status="completed")
        .values_list("user_id")
        .annotate(n=Count("id"))
    )

    best_test = {}
    for row in (
        TestAttempt.objects.filter(user_id__in=user_ids, test_id__in=test_ids)
        .values("user_id", "test_id")
        .annotate(best=Max("score"))
    ):
        if row["best"] is not None:
            best_test.setdefault(row["user_id"], {})[row["test_id"]] = float(row["best"])

    best_assignment = {}
    for row in (
        Submission.objects.filter(user_id__in=user_ids, assignment_id__in=assignments)
        .values("user_id", "assignment_id")
        .annotate(best=Max("score"))
    ):
        if row["best"] is not None:
            best_assignment.setdefault(row["user_id"], {})[row["assignment_id"]] = float(row["best"])

    # Работы, отправленные, но ещё не проверенные. Они уходят в итог нулём, поэтому
    # отметка при непустой очереди предварительная — преподаватель должен это видеть.
    pending = dict(
        Submission.objects.filter(user_id__in=user_ids, assignment_id__in=assignments)
        .exclude(status="graded")
        .values_list("user_id")
        .annotate(n=Count("assignment_id", distinct=True))
    )

    started = dict(
        Enrollment.objects.filter(course=course, user_id__in=user_ids).values_list("user_id", "enrolled_at")
    )

    rows = []
    for uid, user in users.items():
        tests = best_test.get(uid, {})
        subs = best_assignment.get(uid, {})

        lessons_done = done_lessons.get(uid, 0)
        lessons_share = lessons_done / len(lesson_ids) if lesson_ids else None

        # Знаменатель — все тесты курса, а не только пройденные: непройденный тест
        # обязан тянуть отметку вниз, иначе «сдал один тест на 100» = «сдал все».
        tests_share = (sum(tests.values()) / (100 * len(test_ids))) if test_ids else None

        earned = sum(min(subs.get(aid, 0), score) for aid, score in assignments.items())
        assignments_share = (earned / max_total) if max_total else None

        score = final_score(tests_share, lessons_share, assignments_share)
        rows.append(
            {
                "user": user,
                "enrolled_at": started.get(uid),
                "lessons_done": lessons_done,
                "lessons_total": len(lesson_ids),
                "tests_taken": len(tests),
                "tests_total": len(test_ids),
                "tests_pct": round(tests_share * 100) if tests_share is not None else None,
                "assignments_done": sum(1 for aid in assignments if subs.get(aid, 0) > 0),
                "assignments_total": len(assignments),
                "pending": pending.get(uid, 0),
                "score": score,
                "grade": grade_5(score),
                "verdict": pass_fail(score),
            }
        )

    rows.sort(key=lambda r: r["user"].username)
    return rows


def gradebook_summary(rows):
    """Итоги внизу ведомости: распределение отметок и средний балл."""
    graded = [r for r in rows if r["score"] is not None]

    def with_mark(mark):
        return sum(1 for r in graded if r["grade"]["mark"] == mark)

    return {
        "total": len(rows),
        "excellent": with_mark(5),
        "good": with_mark(4),
        "satisfactory": with_mark(3),
        "unsatisfactory": with_mark(2),
        "passed": sum(1 for r in graded if r["verdict"]["passed"]),
        "avg_score": round(sum(r["score"] for r in graded) / len(graded)) if graded else None,
        "pending": sum(r["pending"] for r in rows),
        "period_from": min((r["enrolled_at"] for r in rows if r["enrolled_at"]), default=None),
    }


def manual_queue(teacher):
    """Работы, ожидающие ручной проверки: DDL и файловые задания."""
    course_ids = list(visible_courses(teacher).values_list("id", flat=True))
    manual_ids = [
        a.id
        for a in Assignment.objects.filter(course_id__in=course_ids)
        if not a.is_autocheckable
    ]
    return list(
        Submission.objects.filter(assignment_id__in=manual_ids)
        .exclude(status="graded")
        .select_related("user", "assignment")
        .order_by("submitted_at")
    )
