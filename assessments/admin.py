from django.contrib import admin

from core.admin_utils import OwnedAdmin

from .models import AnswerOption, Assignment, Question, Test


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 0


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    show_change_link = True


class TestInline(admin.TabularInline):
    model = Test
    extra = 0
    show_change_link = True


@admin.register(Test)
class TestAdmin(OwnedAdmin):
    owner_path = "lesson__module__course__author"
    list_display = ("title", "lesson", "pass_score")
    inlines = [QuestionInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "lesson":
            from courses.models import Lesson

            kwargs["queryset"] = Lesson.objects.filter(module__course__author=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Question)
class QuestionAdmin(OwnedAdmin):
    owner_path = "test__lesson__module__course__author"
    list_display = ("text", "test", "points")
    inlines = [AnswerOptionInline]


@admin.register(Assignment)
class AssignmentAdmin(OwnedAdmin):
    owner_path = "course__author"
    list_display = ("title", "course", "level", "is_final")
    list_filter = ("level", "is_final")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "course":
                from courses.models import Course

                kwargs["queryset"] = Course.objects.filter(author=request.user)
            elif db_field.name == "lesson":
                from courses.models import Lesson

                kwargs["queryset"] = Lesson.objects.filter(module__course__author=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
