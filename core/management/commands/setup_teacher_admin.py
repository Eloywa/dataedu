"""Группа «Преподаватели» с правами на авторские модели и выдача её преподавателям.

Преподаватели становятся is_staff и получают права add/change/delete/view на курсы,
модули, уроки, тесты, вопросы, варианты ответов, задания и учебные группы. Видимость
своих объектов ограничивает уже сама админка (OwnedAdmin). Админ — суперпользователь,
видит всё.

Команду можно запускать повторно: при появлении новой модели в списке она довыдаст
права уже развёрнутой платформе, не трогая остальное.
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from accounts.models import User
from assessments.models import AnswerOption, Assignment, Question, Test
from courses.models import Course, Lesson, Module
from learning.models import StudyGroup

GROUP_NAME = "Преподаватели"
AUTHORING_MODELS = [Course, Module, Lesson, Test, Question, AnswerOption, Assignment, StudyGroup]


class Command(BaseCommand):
    help = "Создать группу «Преподаватели» с правами и выдать её преподавателям (is_staff)."

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name=GROUP_NAME)

        perms = []
        for model in AUTHORING_MODELS:
            ct = ContentType.objects.get_for_model(model)
            perms.extend(Permission.objects.filter(content_type=ct))
        group.permissions.set(perms)

        teachers = User.objects.filter(role__code="teacher")
        count = 0
        for user in teachers:
            if not user.is_staff:
                user.is_staff = True
                user.save(update_fields=["is_staff"])
            user.groups.add(group)
            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Группа '{GROUP_NAME}': {len(perms)} прав; преподавателей подключено: {count}."
            )
        )
