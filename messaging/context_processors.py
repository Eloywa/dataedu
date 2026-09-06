"""Число непрочитанных сообщений для шапки.

Бейдж нужен на каждой странице, поэтому считается контекстным процессором, а не
повторяется в каждом представлении. Гостю запрос к базе не делается вовсе.
"""

from . import services


def unread(request):
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {"unread_messages": 0}
    return {"unread_messages": services.unread_count(user)}
