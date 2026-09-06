"""Админка учётных записей и согласий.

`User` наследует `AbstractBaseUser`, поэтому штатные `UserCreationForm` и
`UserChangeForm` не подходят: они привязаны к модели `auth.User`. Здесь описаны
минимальные собственные формы с правильной обработкой пароля — пароль никогда не
показывается и не редактируется как текст, только задаётся заново.
"""

from django import forms
from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm, ReadOnlyPasswordHashField
from django.utils.html import format_html

from .models import Consent, Role, User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Пароль ещё раз", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "display_name", "email", "role")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError({"password2": "Пароли не совпадают."})
        if len(cleaned.get("password1") or "") < 8:
            raise forms.ValidationError({"password1": "Пароль должен быть не короче 8 символов."})
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # Пустой email хранится как NULL: уникальность не должна ломаться на «».
        user.email = user.email or None
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Пароль",
        help_text="Пароли не хранятся в открытом виде, поэтому увидеть текущий нельзя.",
    )

    class Meta:
        model = User
        # Поля перечислены явно: с `__all__` любое новое поле модели автоматически
        # оказывалось бы в форме админки — включая служебные, которые править руками
        # не следует.
        fields = (
            "username",
            "email",
            "display_name",
            "role",
            "avatar_url",
            "xp",
            "level",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.email or None
        if commit:
            user.save()
            self.save_m2m()
        return user


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    change_password_form = AdminPasswordChangeForm

    list_display = ("username", "display_name", "role", "xp", "level", "is_active", "consent_state")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "display_name", "email")
    ordering = ("username",)
    readonly_fields = ("id", "created_at", "last_seen_at")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Профиль",
            {
                "fields": ("display_name", "email", "role"),
                "description": (
                    "Отображаемое имя может быть псевдонимом, email необязателен: "
                    "платформа сознательно не запрашивает настоящее ФИО."
                ),
            },
        ),
        ("Прогресс", {"fields": ("xp", "level")}),
        (
            "Доступ",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Служебное", {"fields": ("id", "created_at", "last_seen_at"), "classes": ("collapse",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": ("username", "display_name", "email", "role", "password1", "password2"),
                "description": (
                    "Для апробации удобнее выдавать аккаунты пачкой: "
                    "<code>manage.py create_pilot_accounts --count 25</code>."
                ),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs["form"] = self.add_form
            kwargs["fields"] = None
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        return self.add_fieldsets if obj is None else super().get_fieldsets(request, obj)

    @admin.display(description="согласия")
    def consent_state(self, obj):
        versions = sorted({c.version for c in obj.consents.all()})
        if not versions:
            return format_html('<span style="color:#b45309">нет записи</span>')
        return ", ".join(versions)


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    """Только чтение: согласие — юридический факт, его не редактируют вручную."""

    list_display = ("user", "document", "version", "granted_at")
    list_filter = ("document", "version")
    search_fields = ("user__username", "user__display_name")
    ordering = ("-granted_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    ordering = ("code",)
