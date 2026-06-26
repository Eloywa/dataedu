from functools import wraps

from django.shortcuts import redirect


def teacher_required(view):
    """Доступ только преподавателю/админу. Гостя — на вход, студента — на главную."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")
        if not request.user.is_teacher:
            return redirect("core:home")
        return view(request, *args, **kwargs)

    return wrapper
