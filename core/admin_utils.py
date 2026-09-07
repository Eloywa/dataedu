"""Изоляция авторства в админке.

`OwnedAdmin` показывает не-суперпользователю только «свои» объекты и запрещает
открывать чужие. Суперпользователь видит всё.

«Своё» бывает двух видов, и они не сводятся друг к другу:

* **через курс** — модуль, урок, тест, вопрос, задание. Владеет тот, кто автор
  курса **или его соавтор**. Такие классы объявляют `course_path` — путь от
  объекта до курса (`""` у самого курса, `"module__course"` у урока).
* **напрямую** — учебная группа принадлежит преподавателю, а не курсу. Такие
  объявляют `owner_path`.

Раньше вид был один: путь заканчивался на `author`, и владелец сравнивался
с пользователем через `==`. С появлением соавторов это перестало работать —
владельцев у курса стало несколько, и проверку пришлось перенести в
`Course.is_authored_by`, чтобы правило доступа существовало в одном месте.
"""

from django.contrib import admin
from django.db.models import Q


class OwnedAdmin(admin.ModelAdmin):
    # Путь от объекта до курса: "" (сам курс), "course", "module__course", …
    # Пустая строка — осмысленное значение, поэтому проверяется `is not None`.
    course_path = None

    # Путь от объекта до пользователя-владельца напрямую, напр. "teacher".
    owner_path = None

    # --- через курс ---------------------------------------------------------

    def _prefix(self):
        return f"{self.course_path}__" if self.course_path else ""

    def _course_filter(self, user):
        prefix = self._prefix()
        return Q(**{f"{prefix}author": user}) | Q(**{f"{prefix}coauthors": user})

    def _course_of(self, obj):
        value = obj
        for part in filter(None, self.course_path.split("__")):
            value = getattr(value, part, None)
            if value is None:
                return None
        return value

    # --- напрямую -----------------------------------------------------------

    def _owner_of(self, obj):
        value = obj
        for part in self.owner_path.split("__"):
            value = getattr(value, part, None)
            if value is None:
                return None
        return value

    # --- общее --------------------------------------------------------------

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if self.course_path is not None:
            # `distinct` обязателен: соединение с таблицей соавторов задваивает
            # строку курса, у которого соавторов несколько.
            return qs.filter(self._course_filter(request.user)).distinct()
        if self.owner_path:
            return qs.filter(**{self.owner_path: request.user})
        return qs

    def _owns(self, request, obj):
        if obj is None or request.user.is_superuser:
            return True
        if self.course_path is not None:
            course = self._course_of(obj)
            return course is not None and course.is_authored_by(request.user)
        if self.owner_path:
            return self._owner_of(obj) == request.user
        return True

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj) and self._owns(request, obj)

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and self._owns(request, obj)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and self._owns(request, obj)
