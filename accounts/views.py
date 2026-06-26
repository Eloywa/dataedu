from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Role, User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    error = None
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get("next") or "core:home")
        error = "Неверный email или пароль."

    return render(request, "accounts/login.html", {"error": error})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("core:home")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    error = None
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm", "")

        if not full_name or not email or not password:
            error = "Заполните все поля."
        elif len(password) < 8:
            error = "Пароль должен быть не короче 8 символов."
        elif password != confirm:
            error = "Пароли не совпадают."
        elif User.objects.filter(email=email).exists():
            error = "Пользователь с таким email уже зарегистрирован."
        else:
            role = Role.objects.filter(code="student").first()
            user = User.objects.create_user(email=email, password=password, full_name=full_name, role=role)
            login(request, user)
            return redirect("core:home")

    return render(request, "accounts/register.html", {"error": error})


@login_required
def settings_view(request):
    error = None
    done = False
    if request.method == "POST":
        current = request.POST.get("current", "")
        new = request.POST.get("new", "")
        confirm = request.POST.get("confirm", "")

        if not request.user.check_password(current):
            error = "Текущий пароль неверный."
        elif len(new) < 8:
            error = "Новый пароль должен быть не короче 8 символов."
        elif new != confirm:
            error = "Пароли не совпадают."
        elif new == current:
            error = "Новый пароль совпадает с текущим."
        else:
            request.user.set_password(new)
            request.user.save(update_fields=["password"])
            update_session_auth_hash(request, request.user)  # не разлогинивать
            done = True

    return render(request, "accounts/settings.html", {"error": error, "done": done})
