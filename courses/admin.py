from django.contrib import admin

from accounts.models import User
from assessments.admin import TestInline
from core.admin_utils import OwnedAdmin

from .models import Course, Lesson, Module, Topic


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    show_change_link = True


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    show_change_link = True


@admin.register(Course)
class CourseAdmin(OwnedAdmin):
    course_path = ""
    list_display = ("title", "level", "is_published", "author", "coauthor_names")
    filter_horizontal = ("coauthors",)
    list_filter = ("level", "is_published")
    search_fields = ("title", "slug")
    inlines = [ModuleInline]

    def get_exclude(self, request, obj=None):
        # преподавателю поле «автор» не показываем — ставится автоматически
        if not request.user.is_superuser:
            return ("author",)
        return super().get_exclude(request, obj) or ()

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        # Соавторы показываются в списке — без предзагрузки это запрос на строку.
        return super().get_queryset(request).prefetch_related("coauthors")

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """В соавторы можно звать только преподавателей.

        Иначе в список попадают все студенты платформы, и промах мышью выдаёт
        студенту доступ к аналитике по курсу — вместе с чужими баллами.
        """
        if db_field.name == "coauthors":
            kwargs["queryset"] = User.objects.filter(
                role__code__in=("teacher", "admin")
            ).order_by("username")
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    @admin.display(description="соавторы")
    def coauthor_names(self, obj):
        names = [u.display_name or u.username for u in obj.coauthors.all()]
        return ", ".join(names) if names else "—"


@admin.register(Module)
class ModuleAdmin(OwnedAdmin):
    course_path = "course"
    list_display = ("title", "course", "order_index", "week_number")
    inlines = [LessonInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "course":
            kwargs["queryset"] = Course.objects.authored_by(request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Lesson)
class LessonAdmin(OwnedAdmin):
    course_path = "module__course"
    list_display = ("title", "module", "order_index")
    inlines = [TestInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "module":
            kwargs["queryset"] = Module.objects.filter(
                course__in=Course.objects.authored_by(request.user)
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Темы каталога — общие, правит только суперпользователь."""

    list_display = ("name", "code")

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
