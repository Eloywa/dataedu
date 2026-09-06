"""Сборка объектов для тестов.

Фабрики, а не фикстуры в JSON: фикстура фиксирует данные целиком, и через полгода
никто не помнит, что в ней важно, а что попало случайно. Здесь тест просит ровно
то, что проверяет, а всё остальное заполняется разумными значениями по умолчанию.

Живёт в `core`, потому что это единственное приложение, которому по правилам
направления зависимостей (см. ARCHITECTURE.md §3.2) позволено знать обо всех.
"""

import itertools

from django.utils import timezone

from accounts.models import Role, User
from assessments.models import (
    AnswerOption,
    AnswerSubmission,
    Assignment,
    Question,
    Submission,
    Test,
    TestAttempt,
)
from courses.models import Course, CourseRating, Lesson, Module, Topic
from gamification.models import Achievement, UserAchievement
from learning.models import Activity, Enrollment, LessonProgress, Reflection, StudyGroup
from messaging.models import Message

PASSWORD = "test-pass-9271"

_counter = itertools.count(1)


def _n():
    return next(_counter)


def role(code, name=None):
    obj, _ = Role.objects.get_or_create(code=code, defaults={"name": name or code})
    return obj


def student(username=None, **extra):
    return User.objects.create_user(
        username=username or f"stud{_n()}",
        password=PASSWORD,
        role=role("student", "Студент"),
        **extra,
    )


def teacher(username=None, **extra):
    return User.objects.create_user(
        username=username or f"teach{_n()}",
        password=PASSWORD,
        role=role("teacher", "Преподаватель"),
        is_staff=True,
        **extra,
    )


def admin(username=None, **extra):
    return User.objects.create_superuser(
        username=username or f"admin{_n()}",
        password=PASSWORD,
        role=role("admin", "Администратор"),
        **extra,
    )


def topic(code=None, name=None):
    i = _n()
    return Topic.objects.create(code=code or f"topic{i}", name=name or f"Тема {i}")


def course(author=None, title=None, slug=None, published=True, level="basic", **extra):
    i = _n()
    return Course.objects.create(
        title=title or f"Курс {i}",
        slug=slug or f"course-{i}",
        level=level,
        is_published=published,
        author=author,
        **extra,
    )


def module(course_obj, order_index=0, week_number=None, title=None):
    return Module.objects.create(
        course=course_obj,
        title=title or f"Модуль {order_index + 1}",
        order_index=order_index,
        week_number=week_number if week_number is not None else order_index + 1,
    )


def lesson(module_obj, order_index=0, title=None, xp_reward=10, theory="Теория."):
    return Lesson.objects.create(
        module=module_obj,
        title=title or f"Урок {_n()}",
        order_index=order_index,
        xp_reward=xp_reward,
        theory_content=theory,
        est_minutes=20,
    )


def course_with_lessons(author=None, lessons=2, modules=1, **extra):
    """Курс с готовой структурой. Возвращает `(курс, [уроки в порядке прохождения])`."""
    obj = course(author=author, **extra)
    all_lessons = []
    for m in range(modules):
        mod = module(obj, order_index=m, week_number=m + 1)
        for i in range(lessons):
            all_lessons.append(lesson(mod, order_index=i))
    return obj, all_lessons


def test_for(lesson_obj, pass_score=60, title=None):
    return Test.objects.create(
        lesson=lesson_obj, title=title or f"Тест {_n()}", pass_score=pass_score
    )


def question(test_obj, points=1, order_index=0, correct="Верно", wrong="Неверно", topic_obj=None):
    """Вопрос с двумя вариантами. Возвращает `(вопрос, верный, неверный)`."""
    q = Question.objects.create(
        test=test_obj,
        text=f"Вопрос {_n()}?",
        type="single",
        points=points,
        order_index=order_index,
        topic=topic_obj,
    )
    right = AnswerOption.objects.create(question=q, text=correct, is_correct=True, order_index=0)
    left = AnswerOption.objects.create(question=q, text=wrong, is_correct=False, order_index=1)
    return q, right, left


def attempt(user, test_obj, score=100, passed=True, finished=True):
    now = timezone.now()
    return TestAttempt.objects.create(
        user=user,
        test=test_obj,
        score=score,
        is_passed=passed,
        started_at=now,
        finished_at=now if finished else None,
    )


def answer(attempt_obj, question_obj, option=None, is_correct=True):
    return AnswerSubmission.objects.create(
        attempt=attempt_obj, question=question_obj, answer_option=option, is_correct=is_correct
    )


def assignment(course_obj, lesson_obj=None, auto=True, max_score=100, is_final=False, **extra):
    """Задание. `auto=True` — с посчитанным эталоном, значит автопроверяемое."""
    expected = {"columns": ["n"], "rows": [[1]]} if auto else None
    return Assignment.objects.create(
        course=course_obj,
        lesson=lesson_obj,
        title=extra.pop("title", f"Задание {_n()}"),
        level="basic",
        type="sql" if auto else "ddl",
        expected_sql="SELECT 1 AS n;",
        setup_sql="",
        expected_result=expected,
        max_score=max_score,
        is_final=is_final,
        **extra,
    )


def submission(assignment_obj, user, status="submitted", score=None, **extra):
    return Submission.objects.create(
        assignment=assignment_obj,
        user=user,
        status=status,
        score=score,
        submitted_at=timezone.now(),
        **extra,
    )


def enroll(user, course_obj, status="active"):
    return Enrollment.objects.create(user=user, course=course_obj, status=status)


def complete(user, lesson_obj, status="completed"):
    return LessonProgress.objects.create(
        user=user,
        lesson=lesson_obj,
        status=status,
        completed_at=timezone.now() if status == "completed" else None,
    )


def complete_course(user, lessons):
    for lesson_obj in lessons:
        complete(user, lesson_obj)


def reflection(user, lesson_obj, clarity=4, difficulty=3, comment=None, anonymous=False):
    return Reflection.objects.create(
        user=user,
        lesson=lesson_obj,
        clarity_rating=clarity,
        difficulty_rating=difficulty,
        comment=comment,
        comment_is_anonymous=anonymous,
    )


def activity(user, type_="login", when=None, entity_type=None, entity_id=None):
    return Activity.objects.create(
        user=user,
        type=type_,
        entity_type=entity_type,
        entity_id=entity_id,
        created_at=when or timezone.now(),
    )


def achievement(code, title=None, xp_reward=25):
    obj, _ = Achievement.objects.get_or_create(
        code=code, defaults={"title": title or code, "xp_reward": xp_reward}
    )
    return obj


def award(user, code):
    return UserAchievement.objects.create(user=user, achievement=achievement(code))


def group(teacher_obj, name=None, students=()):
    obj = StudyGroup.objects.create(teacher=teacher_obj, name=name or f"ГР-{_n()}")
    if students:
        obj.students.set(students)
    return obj


def rate(user, course_obj, rating=5, comment=None):
    return CourseRating.objects.create(user=user, course=course_obj, rating=rating, comment=comment)


def message(sender, recipient, course_obj, body="Вопрос", read=False, when=None):
    return Message.objects.create(
        sender=sender,
        recipient=recipient,
        course=course_obj,
        body=body,
        created_at=when or timezone.now(),
        read_at=timezone.now() if read else None,
    )
