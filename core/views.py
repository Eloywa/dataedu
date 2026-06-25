from django.shortcuts import render


def home(request):
    """Главная страница (пока заглушка для проверки каркаса и дизайна)."""
    return render(request, "core/home.html")
