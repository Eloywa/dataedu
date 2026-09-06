import re
import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


# Допустимый вид логина — **единственный** источник правды: на него ссылается и
# валидатор модели, и проверка в форме регистрации. Разъезжались они не гипотетически:
# в форме стояла проверка `ch.isalnum()`, а она в Python истинна и для кириллицы, и
# логин «иванов» проходил мимо валидатора, хотя поле объявлено латинским. Логин служит
# ключом сопоставления при выгрузке в Moodle, и кириллица в нём ломает импорт.
USERNAME_PATTERN = r"^[a-zA-Z0-9._-]+$"
USERNAME_HELP = "Логин может содержать только латиницу, цифры, точку, дефис и подчёркивание."


def is_valid_username(value):
    return bool(re.match(USERNAME_PATTERN, value or ""))


class Role(models.Model):
    """Роль пользователя: admin / teacher / student."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(unique=True, max_length=30)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, email=None, **extra):
        if not username:
            raise ValueError("Логин обязателен")
        # Email необязателен: платформа рассчитана на обезличенные учётные записи,
        # поэтому пустое значение хранится как NULL (уникальность его не задевает).
        user = self.model(
            username=username.strip(),
            email=self.normalize_email(email) if email else None,
            **extra,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, email=None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(username, password, email, **extra)

    def create_superuser(self, username, password=None, email=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        if extra.get("is_staff") is not True or extra.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=is_superuser=True")
        return self._create_user(username, password, email, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь платформы.

    Вход по **логину-псевдониму**, а не по email. Это осознанное решение в пользу
    минимизации данных: платформе для работы не нужно знать, кто именно за учётной
    записью, — ей достаточно устойчивого идентификатора. Обезличенные данные не
    относятся к персональным (ст. 3 п. 9 152-ФЗ), поэтому при выдаче логинов пачкой
    и хранении соответствия «код ↔ студент» вне системы платформа не становится
    оператором персональных данных.

    Поэтому: `email` необязателен, а `display_name` — это отображаемое имя, которое
    может быть псевдонимом; настоящее ФИО платформа не запрашивает.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        "логин",
        max_length=150,
        unique=True,
        validators=[RegexValidator(USERNAME_PATTERN, USERNAME_HELP)],
        help_text="Латиница, цифры, точка, дефис, подчёркивание.",
    )
    email = models.EmailField(
        "email",
        unique=True,
        blank=True,
        null=True,
        help_text="Необязательно. Платформа не рассылает писем; поле нужно только "
        "для восстановления доступа, если пользователь сам этого захочет.",
    )
    display_name = models.CharField(
        "отображаемое имя",
        max_length=200,
        blank=True,
        help_text="Как обращаться к пользователю в интерфейсе. Может быть псевдонимом; "
        "настоящее ФИО указывать не требуется. Если пусто — показывается логин.",
    )
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users", blank=True, null=True)
    avatar_url = models.TextField(blank=True, null=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_seen_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.display_name or self.username

    @property
    def label(self):
        """Как показывать пользователя в интерфейсе."""
        return self.display_name or self.username

    @property
    def is_teacher(self):
        return self.role is not None and self.role.code in ("teacher", "admin")

    @property
    def is_admin(self):
        return self.role is not None and self.role.code == "admin"


class Consent(models.Model):
    """Факт согласия пользователя с правовым документом.

    Согласие должно быть доказуемым (ст. 9 152-ФЗ): недостаточно чекбокса в форме,
    нужна запись о том, **с какой версией** документа человек согласился и когда.
    Документы версионируются датой (см. `accounts/legal.py`); при изменении текста
    поднимается версия, и прежние согласия остаются привязанными к прежней редакции.

    IP-адрес сознательно НЕ сохраняется: он сам является персональными данными, и
    хранить его ради подтверждения согласия на обработку данных — значит увеличивать
    объём обрабатываемого, а не уменьшать.
    """

    DOC_CHOICES = [
        ("privacy", "Политика обработки персональных данных"),
        ("terms", "Пользовательское соглашение"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="consents"
    )
    document = models.CharField("документ", max_length=30, choices=DOC_CHOICES)
    version = models.CharField("версия документа", max_length=20)
    granted_at = models.DateTimeField("дано", default=timezone.now)

    class Meta:
        db_table = "consents"
        verbose_name = "согласие"
        verbose_name_plural = "согласия"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "document", "version"],
                name="uniq_consent_per_user_doc_version",
            )
        ]

    def __str__(self):
        return f"{self.user} · {self.get_document_display()} v{self.version}"
