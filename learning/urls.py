from django.urls import path

from . import views

app_name = "teaching"

urlpatterns = [
    path("teacher/", views.dashboard, name="dashboard"),
    path("teacher/analytics/", views.analytics, name="analytics"),
    path("teacher/export/students.csv", views.export_students, name="export_students"),
    path("teacher/export/difficulty.csv", views.export_difficulty, name="export_difficulty"),
]
