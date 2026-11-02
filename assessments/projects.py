"""Билеты итогового проекта: кто и когда может тянуть и как выбирается тема."""

import secrets
from collections import Counter

from django.db import IntegrityError, transaction

from gamification import services

from .models import ProjectDraw, ProjectTopic, Submission


def _waits_for(user, assignment):
    """Блок, который студенту ещё надо пройти, или None, если билет уже можно тянуть.

    Блок без уроков пройти нельзя, и он не должен запирать билет навсегда.
    """
    module = assignment.opens_after
    if module is None:
        return None
    gate = services.course_gating(user, assignment.course, user.is_teacher).get(module.id)
    if gate is None or gate["is_complete"] or gate["total"] == 0:
        return None
    return module


def ticket_state(user, assignment):
    """Что показать про билет на странице итогового задания.

    None означает, что билетов здесь нет: задание не итоговое или темы не заведены, и
    тогда итоговое работает как обычная ручная работа. Студент, сдавший работу до появления
    билетов, тянуть не должен: его работа уже у преподавателя.
    """
    if not assignment.is_final:
        return None
    course = assignment.course
    pool = ProjectTopic.objects.filter(course=course, is_active=True).count()
    draw, has_work = None, False
    if user.is_authenticated:
        draw = ProjectDraw.objects.filter(user=user, course=course).select_related("topic").first()
        has_work = Submission.objects.filter(user=user, assignment=assignment).exists()
    if not pool and draw is None:
        return None

    is_student = services.may_track_progress(user, course) and not user.is_teacher
    waits_for = _waits_for(user, assignment) if is_student and draw is None else None
    return {
        "draw": draw,
        "pool": pool,
        "has_work": has_work,
        "waits_for": waits_for,
        "can_draw": is_student and draw is None and not has_work and waits_for is None,
        # Сдать работу без темы нельзя: преподавателю будет не с чем её сравнить.
        "needs_draw": draw is None and not has_work,
    }


def pick_topic(course, user, rng=None):
    """Случайная тема среди тех, что в группе студента выпадали реже всего.

    Обычный случайный выбор на небольшом наборе даёт перекосы: у половины группы могла бы
    оказаться одна и та же тема. Здесь повтор появляется, только когда остальные темы уже
    разобраны. Группа пересекается с курсом через студентов, своего поля курса у неё нет;
    студент вне групп равняется на всех записавшихся на курс.
    """
    topics = list(ProjectTopic.objects.filter(course=course, is_active=True))
    if not topics:
        return None
    draws = ProjectDraw.objects.filter(course=course)
    groups = user.study_groups.all()
    if groups.exists():
        draws = draws.filter(user__study_groups__in=groups)
    # `distinct` по паре с ключом билета: соединение с группами удваивает строку студента из
    # двух групп, но одинаковые темы разных студентов схлопываться не должны.
    rows = draws.values_list("pk", "topic_id").distinct()
    taken = Counter(topic_id for _pk, topic_id in rows)
    rarest = min(taken[topic.id] for topic in topics)
    return (rng or secrets.SystemRandom()).choice(
        [topic for topic in topics if taken[topic.id] == rarest]
    )


def draw_ticket(user, assignment, rng=None):
    """Вытянуть билет. Повторный вызов вернёт уже вытянутый, а не новый."""
    course = assignment.course
    existing = ProjectDraw.objects.filter(user=user, course=course).first()
    if existing:
        return existing
    topic = pick_topic(course, user, rng=rng)
    if topic is None:
        return None
    try:
        with transaction.atomic():
            return ProjectDraw.objects.create(user=user, course=course, topic=topic)
    except IntegrityError:
        # Вторая вкладка успела раньше: её билет и есть билет студента.
        return ProjectDraw.objects.get(user=user, course=course)
