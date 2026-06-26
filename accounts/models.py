import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


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

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("Email обязателен")
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        if extra.get("is_staff") is not True or extra.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=is_superuser=True")
        return self._create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь платформы. Вход по email (штатная аутентификация Django)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users", blank=True, null=True)
    avatar_url = models.TextField(blank=True, null=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_seen_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    @property
    def is_teacher(self):
        return self.role is not None and self.role.code in ("teacher", "admin")

    @property
    def is_admin(self):
        return self.role is not None and self.role.code == "admin"
