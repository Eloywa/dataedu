from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from accounts.avatars import AVATARS
from accounts.models import User

from .levels import LEVEL_THRESHOLDS, level_progress
from .services import (
    get_achievements_for_user,
    get_course_progress,
    get_profile_stats,
    get_recent_activity,
)

NAME_MAX_LENGTH = User._meta.get_field("display_name").max_length


def _profile_error(name, avatar):
    if len(name) > NAME_MAX_LENGTH:
        return f"Имя длиннее {NAME_MAX_LENGTH} символов."
    if avatar and avatar not in AVATARS:
        return "Такой аватарки нет в наборе."
    return None


@login_required
def profile(request):
    """Профиль: кто это, уровень и XP, курсы, достижения, лента активности."""
    user = request.user
    form_name, form_avatar = user.display_name, user.avatar
    error = None
    if request.method == "POST":
        form_name = request.POST.get("display_name", "").strip()
        form_avatar = request.POST.get("avatar", "")
        error = _profile_error(form_name, form_avatar)
        if error is None:
            user.display_name, user.avatar = form_name, form_avatar
            user.save(update_fields=["display_name", "avatar"])
            return redirect(f"{reverse('gamification:profile')}?saved=1")

    achievements = get_achievements_for_user(user)
    return render(
        request,
        "gamification/profile.html",
        {
            "progress": level_progress(user.xp or 0),
            "max_level": len(LEVEL_THRESHOLDS),
            "achievements": achievements,
            "earned_count": sum(1 for a in achievements if a["earned"]),
            "courses": get_course_progress(user),
            "activity": get_recent_activity(user),
            "stats": get_profile_stats(user),
            "avatars": [
                {"key": key, "label": label, "icon": mark_safe(icon)}
                for key, (label, icon) in AVATARS.items()
            ],
            "form_name": form_name,
            "form_avatar": form_avatar,
            "error": error,
            "saved": "saved" in request.GET,
        },
    )
