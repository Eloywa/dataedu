"""Админка переписки — только суперпользователю и только на чтение/удаление.

Личная переписка не должна быть открыта каждому сотруднику: показывать её всем,
у кого есть доступ в админку, значило бы расширить круг лиц, обрабатывающих
данные, без всякой на то нужды. Поэтому раздел виден только суперпользователю, а
править чужие сообщения нельзя вообще — задним числом переписку не переписывают.
Удаление оставлено: без него невозможно снять оскорбительное сообщение.
"""

from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "sender", "recipient", "course", "short_body", "read_at")
    list_filter = ("course",)
    search_fields = ("sender__username", "recipient__username")
    date_hierarchy = "created_at"

    @admin.display(description="текст")
    def short_body(self, obj):
        return obj.body[:60] + ("…" if len(obj.body) > 60 else "")

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
