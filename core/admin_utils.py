"""Изоляция авторства в админке.

`OwnedAdmin` показывает не-суперпользователю только «свои» объекты (через путь к
автору курса) и запрещает открывать/править чужие. Суперпользователь видит всё.
"""

from django.contrib import admin


class OwnedAdmin(admin.ModelAdmin):
    # Путь от объекта к пользователю-автору, напр. "author" или "course__author".
    owner_path = None

    def _owner_of(self, obj):
        value = obj
        for part in self.owner_path.split("__"):
            value = getattr(value, part, None)
            if value is None:
                return None
        return value

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or not self.owner_path:
            return qs
        return qs.filter(**{self.owner_path: request.user})

    def _owns(self, request, obj):
        if obj is None or request.user.is_superuser or not self.owner_path:
            return True
        return self._owner_of(obj) == request.user

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj) and self._owns(request, obj)

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and self._owns(request, obj)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and self._owns(request, obj)
