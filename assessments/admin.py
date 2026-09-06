import json

from django.contrib import admin, messages
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html, format_html_join
from django.views.decorators.http import require_POST

from core.admin_utils import OwnedAdmin

from .expected import ExpectedError, compute_and_save
from .models import AnswerOption, Assignment, Question, Test


def plural_ru(n, one, few, many):
    """Согласование существительного с числом: 1 строка, 2 строки, 5 строк.

    Штатный `pluralize` Django даёт две формы и для русского не годится.
    """
    n = abs(int(n))
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def rows_cols_summary(n_rows, n_cols):
    return (
        f"{n_rows} {plural_ru(n_rows, 'строка', 'строки', 'строк')}, "
        f"{n_cols} {plural_ru(n_cols, 'столбец', 'столбца', 'столбцов')}"
    )


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
    list_display = ("text", "test", "topic", "points")
    list_filter = ("topic",)
    list_editable = ("topic",)  # тему удобно проставлять пачкой прямо в списке
    inlines = [AnswerOptionInline]


@admin.register(Assignment)
class AssignmentAdmin(OwnedAdmin):
    """Конструктор SQL-заданий (этап 10.5).

    Преподаватель заполняет заготовку данных и эталонный запрос, а эталонный результат
    считает кнопка «Посчитать эталон» — в терминал за `manage.py compute_expected`
    ходить не нужно. Сам `expected_result` только для чтения: это производное значение,
    и правка его руками рассинхронизировала бы оценивание с эталонным запросом.

    Отдельная защита — от **устаревшего эталона**: при изменении `setup_sql` или
    `expected_sql` сохранённый результат обнуляется. Иначе решения студентов молча
    сверялись бы с эталоном от прежней редакции задания.
    """

    owner_path = "course__author"
    list_display = ("title", "course", "level", "type", "expected_state", "is_final")
    list_filter = ("level", "type", "is_final")
    search_fields = ("title", "description")
    readonly_fields = ("expected_preview",)
    actions = ("recompute_expected",)
    change_form_template = "admin/assessments/assignment/change_form.html"

    fieldsets = (
        (None, {"fields": ("course", "lesson", "title", "description")}),
        ("Параметры", {"fields": ("level", "type", "max_score", "is_final")}),
        (
            "Автопроверка (для type = sql)",
            {
                "fields": ("setup_sql", "expected_sql", "expected_preview"),
                "description": (
                    "<b>Заготовка данных</b> — DDL и INSERT, создающие условия задачи. "
                    "Она же выполняется в браузере студента, поэтому пишите только "
                    "переносимый SQL.<br>"
                    "<b>Эталонный запрос</b> — правильное решение; студенту он никогда "
                    "не отдаётся.<br>"
                    "После заполнения нажмите <b>«Посчитать эталон»</b> внизу страницы: "
                    "запрос выполнится в одноразовой схеме на сервере и откатится, а "
                    "результат сохранится для сравнения. Запрос студента сервер не "
                    "исполняет — он работает в браузере."
                ),
            },
        ),
    )

    @admin.display(description="эталон")
    def expected_state(self, obj):
        if obj.type != "sql":
            return "—"
        if not obj.expected_result:
            return format_html('<span style="color:#b45309">не посчитан</span>')
        rows = len(obj.expected_result.get("rows", []))
        cols = len(obj.expected_result.get("columns", []))
        return format_html('<span style="color:#3f7d14">{}</span>', rows_cols_summary(rows, cols))

    @admin.display(description="Посчитанный эталон")
    def expected_preview(self, obj):
        """Эталон таблицей, а не сырым JSON: преподаватель должен его глазами проверить."""
        if obj is None or not obj.expected_result:
            return "Ещё не посчитан — заполните поля выше и нажмите «Посчитать эталон»."
        cols = obj.expected_result.get("columns", [])
        rows = obj.expected_result.get("rows", [])
        head = format_html_join("", "<th style='padding:4px 10px'>{}</th>", ((c,) for c in cols))
        body = format_html_join(
            "",
            "<tr>{}</tr>",
            (
                (
                    format_html_join(
                        "",
                        "<td style='padding:4px 10px'>{}</td>",
                        (("NULL" if v is None else v,) for v in row),
                    ),
                )
                for row in rows[:20]
            ),
        )
        hidden = len(rows) - 20
        tail = (
            format_html(
                "<p>… и ещё {} {}</p>", hidden, plural_ru(hidden, "строка", "строки", "строк")
            )
            if hidden > 0
            else ""
        )
        return format_html(
            "<table style='border-collapse:collapse'>"
            "<thead><tr>{}</tr></thead><tbody>{}</tbody></table>"
            "<p style='margin-top:8px'><b>Всего: {}.</b></p>{}",
            head,
            body,
            rows_cols_summary(len(rows), len(cols)),
            tail,
        )

    def save_model(self, request, obj, form, change):
        """Сохранить и, если изменились исходники эталона, обнулить его."""
        stale = change and ("setup_sql" in form.changed_data or "expected_sql" in form.changed_data)
        if stale and obj.expected_result:
            obj.expected_result = None
            self.message_user(
                request,
                "Заготовка или эталонный запрос изменились — прежний эталон сброшен. "
                "Нажмите «Посчитать эталон», иначе автопроверка задания не работает.",
                messages.WARNING,
            )
        super().save_model(request, obj, form, change)

    # --- Пересчёт эталона: кнопка на странице объекта и действие в списке ---------

    def get_urls(self):
        return [
            path(
                "<uuid:object_id>/compute-expected/",
                self.admin_site.admin_view(self.compute_expected_view),
                name="assessments_assignment_compute_expected",
            ),
            path(
                "<uuid:object_id>/save-expected/",
                self.admin_site.admin_view(self.save_expected_view),
                name="assessments_assignment_save_expected",
            ),
            *super().get_urls(),
        ]

    @method_decorator(require_POST)
    def save_expected_view(self, request, object_id):
        """Принять эталон, посчитанный в браузере преподавателя (static/js/expected.js).

        Доверие здесь то же, что и у остальной админки: эталон задаёт преподаватель,
        и он же его считает. Проверяется только право менять именно это задание —
        `get_object` учитывает изоляцию авторства, поэтому чужому заданию эталон
        подставить нельзя.

        Форма результата проверяется явно: сюда приходит JSON, а не форма Django,
        и на кривой вход нужно ответить понятной ошибкой, а не пятисоткой.
        """
        obj = self.get_object(request, object_id)
        if obj is None or not self.has_change_permission(request, obj):
            raise Http404

        try:
            payload = json.loads(request.body)
            columns = payload["columns"]
            rows = payload["rows"]
        except (ValueError, TypeError, KeyError):
            return JsonResponse({"ok": False, "error": "Некорректные данные."}, status=400)

        if not isinstance(columns, list) or not isinstance(rows, list):
            return JsonResponse({"ok": False, "error": "Ожидались списки."}, status=400)
        if not columns:
            return JsonResponse(
                {"ok": False, "error": "Эталон без столбцов — нужен SELECT."}, status=400
            )
        if any(not isinstance(r, list) or len(r) != len(columns) for r in rows):
            return JsonResponse(
                {"ok": False, "error": "Строки не совпадают по числу столбцов."}, status=400
            )

        obj.expected_result = {"columns": columns, "rows": rows}
        obj.save(update_fields=["expected_result"])
        return JsonResponse({"ok": True, "summary": rows_cols_summary(len(rows), len(columns))})

    def compute_expected_view(self, request, object_id):
        obj = self.get_object(request, object_id)
        if obj is None or not self.has_change_permission(request, obj):
            raise Http404
        try:
            result = compute_and_save(obj)
            self.message_user(
                request,
                "Эталон посчитан: "
                + rows_cols_summary(len(result["rows"]), len(result["columns"]))
                + ".",
                messages.SUCCESS,
            )
        except ExpectedError as e:
            self.message_user(request, f"Не удалось посчитать эталон. {e}", messages.ERROR)
        return redirect(reverse("admin:assessments_assignment_change", args=[object_id]))

    @admin.action(description="Посчитать эталон для выбранных заданий")
    def recompute_expected(self, request, queryset):
        done, failed = 0, []
        for obj in queryset:
            try:
                compute_and_save(obj)
                done += 1
            except ExpectedError as e:
                failed.append(f"«{obj.title}»: {e}")
        if done:
            self.message_user(request, f"Эталон посчитан для {done} заданий.", messages.SUCCESS)
        for line in failed:
            self.message_user(request, f"Не удалось — {line}", messages.ERROR)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "course":
                from courses.models import Course

                kwargs["queryset"] = Course.objects.filter(author=request.user)
            elif db_field.name == "lesson":
                from courses.models import Lesson

                kwargs["queryset"] = Lesson.objects.filter(module__course__author=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
