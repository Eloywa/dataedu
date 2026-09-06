"""Выдача обезличенных учётных записей для апробации.

Ключевой приём правового контура: участники исследования получают не аккаунты со
своими ФИО, а **коды участников** (`p-01`, `p-02`, …) со случайными паролями. Список
печатается один раз, преподаватель раздаёт строки участникам и хранит соответствие
«код ↔ студент» вне платформы (на бумаге). В базе остаются только обезличенные записи,
поэтому платформа не обрабатывает персональные данные (ст. 3 п. 9 152-ФЗ).

Пароли показываются **только в момент создания** — в базе лежат хеши, восстановить их
нельзя. Если строка потеряна, аккаунту назначается новый пароль (`--reset`).
"""

import secrets

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.legal import VERSIONS
from accounts.models import Consent, Role, User

# Алфавит без похожих друг на друга символов: пароль переносят с бумаги руками,
# и путаница 0/O или 1/l/I стоит дороже, чем два лишних бита энтропии.
ALPHABET = "abcdefghijkmnpqrstuvwxyzACDEFGHJKLMNPQRSTUVWXYZ23456789"


def make_password_str(length=10):
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


class Command(BaseCommand):
    help = "Создать обезличенные учётные записи участников апробации (p-01, p-02, …)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=25, help="сколько аккаунтов (по умолчанию 25)"
        )
        parser.add_argument("--prefix", default="p", help="префикс логина (по умолчанию p)")
        parser.add_argument("--start", type=int, default=1, help="с какого номера начинать")
        parser.add_argument(
            "--reset",
            action="store_true",
            help="если логин уже существует — назначить новый пароль вместо пропуска",
        )

    def handle(self, *args, **options):
        count = options["count"]
        prefix = options["prefix"].strip()
        start = options["start"]
        reset = options["reset"]

        if count < 1:
            raise CommandError("--count должен быть положительным")
        if not all(ch.isalnum() or ch in "._-" for ch in prefix):
            raise CommandError(
                "префикс может содержать только латиницу, цифры, точку, дефис, подчёркивание"
            )

        role = Role.objects.filter(code="student").first()
        if role is None:
            raise CommandError("не найдена роль student — сначала создайте роли")

        width = max(2, len(str(start + count - 1)))
        created, updated, skipped = [], [], []

        with transaction.atomic():
            for n in range(start, start + count):
                username = f"{prefix}-{str(n).zfill(width)}"
                password = make_password_str()
                existing = User.objects.filter(username=username).first()

                if existing is not None:
                    if not reset:
                        skipped.append(username)
                        continue
                    existing.set_password(password)
                    existing.save(update_fields=["password"])
                    updated.append((username, password))
                    continue

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=None,
                    display_name="",  # намеренно пусто: показывается логин
                    role=role,
                )
                # Согласие участника собирается организацией на бумаге; здесь
                # фиксируется, какая редакция документов действовала при выдаче.
                for document, version in VERSIONS.items():
                    Consent.objects.create(user=user, document=document, version=version)
                created.append((username, password))

        self._report(created, updated, skipped)

    def _report(self, created, updated, skipped):
        if created:
            self.stdout.write(self.style.SUCCESS(f"\nСоздано аккаунтов: {len(created)}"))
            self._table(created)
        if updated:
            self.stdout.write(self.style.WARNING(f"\nПароль сброшен у: {len(updated)}"))
            self._table(updated)
        if skipped:
            self.stdout.write(
                self.style.WARNING(
                    f"\nПропущено (логин уже занят, запустите с --reset): {', '.join(skipped)}"
                )
            )
        if created or updated:
            self.stdout.write(
                "\nПароли показаны единственный раз — в базе хранятся только хеши."
                "\nРаспечатайте список, раздайте строки участникам, а соответствие"
                "\n«код ↔ студент» держите вне платформы."
            )

    def _table(self, rows):
        self.stdout.write("")
        self.stdout.write(f"  {'логин':<12} пароль")
        self.stdout.write(f"  {'-' * 12} {'-' * 12}")
        for username, password in rows:
            self.stdout.write(f"  {username:<12} {password}")
