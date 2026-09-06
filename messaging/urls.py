from django.urls import path

from . import views

app_name = "messaging"

urlpatterns = [
    path("messages/", views.inbox, name="inbox"),
    path("messages/send/", views.send, name="send"),
    path("messages/thread.json", views.thread_json, name="thread_json"),
    path("messages/unread.json", views.unread_json, name="unread_json"),
]
