"""Сервисы геймификации: XP/уровни, достижения, лента активности, gating-хелпер.
Порт логики из Next-версии (levels/achievements/activity/gating).
"""

from django.utils import timezone

from courses.models import Lesson
from learning.models import Activity, LessonProgress
from learning.sqlerrors import ERROR_CODES

from .gating import compute_gating
from .levels import level_for_xp
from .models import Achievement, UserAchievement

MEANINGFUL = [
    "lesson_complete",
    "test_finish",
    "sql_run",
    "submission",
    "achievement",
    "reflection",
]

# Начисление XP. Урок даёт свой lesson.xp_reward; тест и задание — фиксированную
# величину и только за первый успех (повторные попытки XP не приносят).
XP_TEST_PASS = 15
XP_ASSIGNMENT_SOLVED = 20
# Рефлексия даёт немного: она полезна исследованию, но не должна становиться
# способом набивать уровень в обход учебной работы. Начисляется один раз на урок —
# правка своей же оценки XP не приносит.
XP_REFLECTION = 5


def add_xp(user, amount):
    if not amount:
        return
    user.xp = (user.xp or 0) + amount
    user.level = level_for_xp(user.xp)
    user.save(update_fields=["xp", "level"])


def log_activity(user, type_, entity_type=None, entity_id=None, metadata=None):
    Activity.objects.create(
        user=user,
        type=type_,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata=metadata,
        created_at=timezone.now(),
    )


def award_achievement(user, code):
    """Идемпотентно выдать достижение: запись + XP + лог. Возвращает True, если выдано сейчас."""
    ach = Achievement.objects.filter(code=code).first()
    if ach is None:
        return False
    obj, created = UserAchievement.objects.get_or_create(
        user=user, achievement=ach, defaults={"awarded_at": timezone.now()}
    )
    if not created:
        return False
    add_xp(user, ach.xp_reward or 0)
    log_activity(user, "achievement", "achievement", ach.id)
    return True


def complete_lesson(user, lesson):
    """Отметить урок пройденным один раз: статус + XP урока + лог + first_lesson."""
    lp = LessonProgress.objects.filter(user=user, lesson=lesson).first()
    if lp and lp.status == "completed":
        return False
    if lp is None:
        lp = LessonProgress(user=user, lesson=lesson, time_spent_sec=0, visits=0)
    lp.status = "completed"
    lp.completed_at = timezone.now()
    lp.save()
    add_xp(user, lesson.xp_reward or 0)
    log_activity(user, "lesson_complete", "lesson", lesson.id)
    award_achievement(user, "first_lesson")
    return True


def finish_test(user, attempt, lesson):
    """События и награды за только что записанную попытку теста.

    XP за тест начисляется один раз — при первом успешном прохождении; при
    успехе урок отмечается пройденным (со своим XP и логом).
    """
    from assessments.models import TestAttempt

    test = attempt.test
    log_activity(user, "test_finish", "test", test.id)

    if attempt.is_passed:
        passed_before = (
            TestAttempt.objects.filter(user=user, test=test, is_passed=True)
            .exclude(pk=attempt.pk)
            .exists()
        )
        if not passed_before:
            add_xp(user, XP_TEST_PASS)
        complete_lesson(user, lesson)

    if attempt.score >= 80:
        award_achievement(user, "test_master")


def record_submission(user, submission):
    """Событие и XP за только что записанную сдачу (XP — за первое верное решение)."""
    from assessments.models import Submission

    assignment = submission.assignment
    log_activity(user, "submission", "assignment", assignment.id)

    if submission.score >= 1:
        solved_before = (
            Submission.objects.filter(user=user, assignment=assignment, score__gte=1)
            .exclude(pk=submission.pk)
            .exists()
        )
        if not solved_before:
            add_xp(user, XP_ASSIGNMENT_SOLVED)


def record_reflection(user, lesson, is_new):
    """Событие и XP за рефлексию. XP — только за первую по этому уроку.

    `is_new` приходит от вызывающей стороны (результат `update_or_create`), потому
    что к моменту вызова запись уже сохранена и «первая ли она» по базе уже не видно.
    """
    log_activity(user, "reflection", "lesson", lesson.id)
    if is_new:
        add_xp(user, XP_REFLECTION)


def record_sql_run(user):
    """Запуск запроса в тренажёре: событие для аналитики + «Первый запрос».

    Возвращает название достижения, если оно выдано именно сейчас, иначе None.
    """
    log_activity(user, "sql_run")
    if award_achievement(user, "first_query"):
        ach = Achievement.objects.filter(code="first_query").first()
        return ach.title if ach else None
    return None


def record_sql_error(user, code, assignment_id=None):
    """Ошибка в SQL: запоминается класс ошибки, но не сам запрос и не текст ошибки.

    Смысл записи — в отчёте «на чём спотыкаются»: он показывает не «урок трудный»,
    а что именно не выходит — группировка, соединение, типы. Это третий
    объективный признак трудности рядом с баллами и числом попыток, и в отличие
    от них он говорит о причине, а не о следствии.

    В запросе студента и в тексте ошибки PostgreSQL оказываются придуманные им
    данные, поэтому на сервер приходит только код класса.
    """
    if code not in ERROR_CODES:
        return
    log_activity(
        user,
        "sql_error",
        entity_type="assignment" if assignment_id else "trainer",
        entity_id=assignment_id,
        metadata={"code": code},
    )


def record_login(user):
    """Событие входа + проверка серии «Неделя без пропусков»."""
    log_activity(user, "login")
    check_login_streak(user)


def check_login_streak(user):
    """no_miss_week — 7 дней входов подряд (самая длинная серия по датам)."""
    dates = sorted({a.created_at.date() for a in Activity.objects.filter(user=user, type="login")})
    if not dates:
        return
    best = run = 1
    for i in range(1, len(dates)):
        delta = (dates[i] - dates[i - 1]).days
        if delta == 1:
            run += 1
            best = max(best, run)
        elif delta > 1:
            run = 1
    if best >= 7:
        award_achievement(user, "no_miss_week")


# Значки достижений в моно-стиле «Terminal» (в БД хранится только имя иконки).
ICON_GLYPHS = {"flag": "⚑", "code": "›_", "medal": "◉", "fire": "✦", "trophy": "★"}


def get_achievements_for_user(user):
    earned = {ua.achievement_id: ua.awarded_at for ua in UserAchievement.objects.filter(user=user)}
    items = []
    for a in Achievement.objects.order_by("xp_reward"):
        items.append(
            {
                "code": a.code,
                "title": a.title,
                "description": a.description,
                "icon": a.icon,
                "glyph": ICON_GLYPHS.get(a.icon or "", "◆"),
                "xp_reward": a.xp_reward,
                "earned": a.id in earned,
                "awarded_at": earned.get(a.id),
            }
        )
    return items


def _day_label(d):
    today = timezone.localdate()
    diff = (today - d).days
    if diff == 0:
        return "Сегодня"
    if diff == 1:
        return "Вчера"
    months = [
        "января",
        "февраля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        "ноября",
        "декабря",
    ]
    return f"{d.day} {months[d.month - 1]}"


def get_recent_activity(user, limit=20):
    acts = list(
        Activity.objects.filter(user=user, type__in=MEANINGFUL).order_by("-created_at")[:limit]
    )
    if not acts:
        return []

    def ids(entity):
        return [a.entity_id for a in acts if a.entity_type == entity and a.entity_id]

    lessons = {x.id: x.title for x in Lesson.objects.filter(id__in=ids("lesson"))}
    from assessments.models import Assignment, Test

    tests = {x.id: x.title for x in Test.objects.filter(id__in=ids("test"))}
    assignments = {x.id: x.title for x in Assignment.objects.filter(id__in=ids("assignment"))}

    def text_of(a):
        if a.type == "lesson_complete":
            n = lessons.get(a.entity_id)
            return ("lesson", f"Завершён урок «{n}»" if n else "Завершён урок")
        if a.type == "test_finish":
            n = tests.get(a.entity_id)
            return ("test", f"Пройден тест «{n}»" if n else "Пройден тест")
        if a.type == "sql_run":
            return ("sql", "Запрос в SQL-тренажёре")
        if a.type == "submission":
            n = assignments.get(a.entity_id)
            return ("submission", f"Сдано задание «{n}»" if n else "Сдано задание")
        if a.type == "achievement":
            return ("achievement", "Получено достижение")
        if a.type == "reflection":
            n = lessons.get(a.entity_id)
            return ("reflection", f"Рефлексия по уроку «{n}»" if n else "Рефлексия по уроку")
        return (None, None)

    groups = []
    current = None
    seen = set()
    for a in acts:
        kind, text = text_of(a)
        if not text or text in seen:
            continue
        seen.add(text)
        day = _day_label(a.created_at.astimezone().date())
        if current is None or current["day"] != day:
            current = {"day": day, "items": []}
            groups.append(current)
        current["items"].append({"kind": kind, "text": text})
    return groups


def get_profile_stats(user):
    """Сводка для страницы прогресса: уроки, тесты, задания, запросы."""
    from assessments.models import Submission, TestAttempt

    return {
        "lessons": LessonProgress.objects.filter(user=user, status="completed").count(),
        "tests": TestAttempt.objects.filter(user=user, is_passed=True)
        .values("test_id")
        .distinct()
        .count(),
        "assignments": Submission.objects.filter(user=user, score__gte=1)
        .values("assignment_id")
        .distinct()
        .count(),
        "queries": Activity.objects.filter(user=user, type="sql_run").count(),
    }


def course_gating(user, course, is_teacher):
    """Вернуть {module_id: {unlocked, is_complete, total, completed}} для курса."""
    modules = list(course.modules.all())
    completed_ids = set()
    if user.is_authenticated:
        completed_ids = set(
            LessonProgress.objects.filter(
                user=user, lesson__module__course=course, status="completed"
            ).values_list("lesson_id", flat=True)
        )
    counts = []
    for m in modules:
        lesson_ids = list(Lesson.objects.filter(module=m).values_list("id", flat=True))
        total = len(lesson_ids)
        completed = sum(1 for lid in lesson_ids if lid in completed_ids)
        counts.append((total, completed))
    flags = compute_gating(counts, bypass=is_teacher)
    return {
        m.id: {**flags[i], "total": counts[i][0], "completed": counts[i][1]}
        for i, m in enumerate(modules)
    }
