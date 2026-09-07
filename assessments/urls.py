from django.urls import path

from . import views

app_name = "assessments"

urlpatterns = [
    path("lessons/<uuid:lesson_id>/test/", views.lesson_test, name="lesson_test"),
    path("practice/", views.practice, name="practice"),
    path("practice/<uuid:assignment_id>/", views.assignment_detail, name="assignment_detail"),
    path("practice/<uuid:assignment_id>/check/", views.check_assignment, name="check"),
    path("practice/<uuid:assignment_id>/error/", views.report_error, name="report_error"),
]
