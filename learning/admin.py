from django import forms
from django.contrib import admin

from accounts.models import User
from core.admin_utils import OwnedAdmin

from .models import StudyGroup


class StudyGroupForm(forms.ModelForm):
    """Понятная ошибка на повторное название группы.

    Название уникально в пределах преподавателя, но поля «преподаватель» в форме у него
    нет — оно ставится автоматически. Django в таком случае не проверяет ограничение,
    и повтор доходил бы до базы, превращаясь в ошибку сервера.
    """

    # Подставляет `StudyGroupAdmin.get_form`: у формы нет доступа к запросу.
    owner = None

    def clean(self):
        cleaned = super().clean()
        if "teacher" in cleaned:
            teacher = cleaned["teacher"]
        else:
            teacher = self.instance.teacher if self.instance.teacher_id else self.owner

        name = cleaned.get("name")
        clash = StudyGroup.objects.filter(teacher=teacher, name=name).exclude(pk=self.instance.pk)
        if teacher is not None and name and clash.exists():
            self.add_error("name", "Группа с таким названием у этого преподавателя уже есть.")
        return cleaned


@admin.register(StudyGroup)
class StudyGroupAdmin(OwnedAdmin):
    """Состав учебных групп. Преподаватель видит и правит только свои (§17.9)."""

    form = StudyGroupForm
    owner_path = "teacher"
    list_display = ("name", "teacher", "students_count", "note")
    search_fields = ("name",)
    filter_horizontal = ("students",)

    def get_form(self, request, obj=None, **kwargs):
        # Django собирает класс формы заново на каждый запрос, поэтому атрибут не
        # протечёт к другому пользователю.
        form = super().get_form(request, obj, **kwargs)
        form.owner = request.user
        return form

    @admin.display(description="студентов")
    def students_count(self, obj):
        return obj.students.count()

    def get_exclude(self, request, obj=None):
        # преподавателю поле «преподаватель» не показываем — ставится автоматически
        if not request.user.is_superuser:
            return ("teacher",)
        return super().get_exclude(request, obj) or ()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # В группу набираются студенты; преподавателей и админов в списке быть не должно.
        if db_field.name == "students":
            kwargs["queryset"] = User.objects.filter(role__code="student").order_by("username")
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.teacher_id:
            obj.teacher = request.user
        super().save_model(request, obj, form, change)
