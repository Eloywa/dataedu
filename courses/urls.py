from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("catalog/", views.catalog, name="catalog"),
    path("catalog/<slug:slug>/", views.course_detail, name="course_detail"),
    path("catalog/<slug:slug>/enroll/", views.enroll, name="enroll"),
    path("catalog/<slug:slug>/review/", views.submit_review, name="review"),
    path("certificate/<slug:slug>/", views.certificate, name="certificate"),
    path("lessons/<uuid:lesson_id>/", views.lesson_detail, name="lesson_detail"),
    path("lessons/<uuid:lesson_id>/complete/", views.complete_lesson, name="complete_lesson"),
    path("lessons/<uuid:lesson_id>/reflection/", views.submit_reflection, name="submit_reflection"),
]
