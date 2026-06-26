"""Задать демо-пароль всем пользователям (после переноса пароли «неустановлены»)
и поднять пользователя с ролью admin до суперпользователя для доступа в /admin.
"""

from django.core.management.base import BaseCommand

from accounts.models import User

DEMO_PASSWORD = "dataedu2026"


class Command(BaseCommand):
    help = "Установить демо-пароль всем пользователям и сделать админа суперпользователем."

    def handle(self, *args, **options):
        total = 0
        admins = 0
        for user in User.objects.select_related("role").all():
            user.set_password(DEMO_PASSWORD)
            if user.role and user.role.code == "admin":
                user.is_superuser = True
                user.is_staff = True
                admins += 1
            user.save(update_fields=["password", "is_superuser", "is_staff"])
            total += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Пароль '{DEMO_PASSWORD}' задан {total} пользователям; админов -> суперпользователь: {admins}."
            )
        )
