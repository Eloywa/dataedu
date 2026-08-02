"""Набор учебной группы из уже записанных на курс.

Руками это делается в админке, но на апробации логины выдаются пачкой
(`create_pilot_accounts`), и отмечать три десятка галочек — работа ради работы.
Команда идемпотентна: повторный запуск состав не дублирует, а `--replace` заменяет
его целиком.
"""

from django.core.management.base import BaseCommand, CommandError

from accounts.models import User
from courses.models import Course
from learning.models import Enrollment, StudyGroup


class Command(BaseCommand):
    help = "Создать учебную группу и набрать в неё студентов, записанных на курс"

    def add_arguments(self, parser):
        parser.add_argument("name", help="название группы, например «ИСТ-21»")
        parser.add_argument("--teacher", help="логин преподавателя-владельца группы")
        parser.add_argument("--course", help="slug курса: взять всех записанных на него")
        parser.add_argument("--logins", help="логины через запятую (вместо --course или вдобавок)")
        parser.add_argument(
            "--replace",
            action="store_true",
            help="заменить состав группы целиком, а не дополнить его",
        )

    def handle(self, *args, **options):
        name = options["name"].strip()
        if not (options["course"] or options["logins"]):
            raise CommandError("укажите --course и/или --logins — иначе набирать некого")

        teacher = None
        if options["teacher"]:
            teacher = User.objects.filter(username=options["teacher"]).first()
            if teacher is None:
                raise CommandError(f"не найден пользователь {options['teacher']}")
            if not teacher.is_teacher:
                raise CommandError(f"{teacher.username} не преподаватель")

        students = []
        if options["course"]:
            course = Course.objects.filter(slug=options["course"]).first()
            if course is None:
                raise CommandError(f"не найден курс {options['course']}")
            if teacher is None:
                teacher = course.author
            students += [
                e.user
                for e in Enrollment.objects.filter(course=course).select_related("user")
                if not e.user.is_teacher
            ]

        if options["logins"]:
            wanted = [x.strip() for x in options["logins"].split(",") if x.strip()]
            found = {u.username: u for u in User.objects.filter(username__in=wanted)}
            missing = [x for x in wanted if x not in found]
            if missing:
                raise CommandError(f"не найдены логины: {', '.join(missing)}")
            students += list(found.values())

        group, created = StudyGroup.objects.get_or_create(name=name, teacher=teacher)
        before = group.students.count()
        if options["replace"]:
            group.students.set(students)
        else:
            group.students.add(*students)
        after = group.students.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"{'Создана' if created else 'Обновлена'} группа «{group.name}»"
                f" (преподаватель: {group.teacher.username if group.teacher else '—'})"
            )
        )
        self.stdout.write(f"  состав: было {before}, стало {after}")
