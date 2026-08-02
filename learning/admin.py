from django.contrib import admin

from accounts.models import User
from core.admin_utils import OwnedAdmin

from .models import StudyGroup


@admin.register(StudyGroup)
class StudyGroupAdmin(OwnedAdmin):
    """Состав учебных групп. Преподаватель видит и правит только свои (§17.9)."""

    owner_path = "teacher"
    list_display = ("name", "teacher", "students_count", "note")
    search_fields = ("name",)
    filter_horizontal = ("students",)

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
