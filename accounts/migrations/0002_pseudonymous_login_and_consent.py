"""Этап 9.6: переход на вход по логину-псевдониму и фиксация согласий.

Порядок шагов важен, потому что в базе уже есть пользователи:

1. `full_name` → `display_name` (переименование, данные сохраняются);
2. `username` добавляется допускающим NULL — иначе existing rows не пройдут;
3. данные переливаются: логин берётся из локальной части email;
4. только теперь `username` становится обязательным и уникальным;
5. `email` перестаёт быть обязательным.
"""

import uuid

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


def fill_usernames(apps, schema_editor):
    """Логин = локальная часть email, с разрешением коллизий.

    `anna@stud.ru` → `anna`. Если такой логин уже занят (например, `olga@a.ru` и
    `olga@b.ru`), добавляется числовой суффикс.
    """
    User = apps.get_model("accounts", "User")
    taken = set()
    for user in User.objects.order_by("created_at"):
        base = (user.email or "").split("@")[0].strip().lower()
        base = "".join(ch for ch in base if ch.isalnum() or ch in "._-") or "user"
        candidate, n = base, 1
        while candidate in taken:
            n += 1
            candidate = f"{base}{n}"
        taken.add(candidate)
        user.username = candidate
        user.save(update_fields=["username"])


def clear_usernames(apps, schema_editor):
    """Обратный шаг: логины просто обнуляются, email остаётся идентификатором."""
    User = apps.get_model("accounts", "User")
    User.objects.update(username=None)


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="full_name",
            new_name="display_name",
        ),
        migrations.AlterField(
            model_name="user",
            name="display_name",
            field=models.CharField(
                blank=True,
                help_text="Как обращаться к пользователю в интерфейсе. Может быть "
                "псевдонимом; настоящее ФИО указывать не требуется. Если пусто — "
                "показывается логин.",
                max_length=200,
                verbose_name="отображаемое имя",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=150,
                null=True,
                verbose_name="логин",
            ),
        ),
        migrations.RunPython(fill_usernames, clear_usernames),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                help_text="Латиница, цифры, точка, дефис, подчёркивание.",
                max_length=150,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-zA-Z0-9._-]+$",
                        "Логин может содержать только латиницу, цифры, точку, дефис "
                        "и подчёркивание.",
                    )
                ],
                verbose_name="логин",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True,
                null=True,
                help_text="Необязательно. Платформа не рассылает писем; поле нужно "
                "только для восстановления доступа, если пользователь сам этого захочет.",
                max_length=254,
                unique=True,
                verbose_name="email",
            ),
        ),
        migrations.CreateModel(
            name="Consent",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "document",
                    models.CharField(
                        choices=[
                            ("privacy", "Политика обработки персональных данных"),
                            ("terms", "Пользовательское соглашение"),
                        ],
                        max_length=30,
                        verbose_name="документ",
                    ),
                ),
                ("version", models.CharField(max_length=20, verbose_name="версия документа")),
                (
                    "granted_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="дано"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="consents",
                        to="accounts.user",
                    ),
                ),
            ],
            options={
                "verbose_name": "согласие",
                "verbose_name_plural": "согласия",
                "db_table": "consents",
            },
        ),
        migrations.AddConstraint(
            model_name="consent",
            constraint=models.UniqueConstraint(
                fields=("user", "document", "version"),
                name="uniq_consent_per_user_doc_version",
            ),
        ),
    ]
