from django.urls import path

from . import views

app_name = "assessments"

urlpatterns = [
    path("lessons/<uuid:lesson_id>/test/", views.lesson_test, name="lesson_test"),
]
