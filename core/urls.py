from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("trainer/", views.trainer, name="trainer"),
    path("trainer/log/", views.trainer_log, name="trainer_log"),
]
