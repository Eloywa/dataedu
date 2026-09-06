from django.urls import path

from . import views

app_name = "teaching"

urlpatterns = [
    path("teacher/", views.dashboard, name="dashboard"),
    path("teacher/analytics/", views.analytics, name="analytics"),
    path("teacher/report/", views.report, name="report"),
    path("teacher/submissions/", views.submissions, name="submissions"),
    path("teacher/submissions/<uuid:submission_id>/grade/", views.grade, name="grade"),
    path("teacher/students/<uuid:user_id>/", views.student, name="student"),
    path("teacher/students/<uuid:user_id>/defend/", views.defend_project, name="defend_project"),
    path("teacher/export/students.csv", views.export_students, name="export_students"),
    path("teacher/export/difficulty.csv", views.export_difficulty, name="export_difficulty"),
    path("teacher/export/vedomost.csv", views.export_vedomost, name="export_vedomost"),
    path("teacher/export/moodle.csv", views.export_moodle, name="export_moodle"),
]
