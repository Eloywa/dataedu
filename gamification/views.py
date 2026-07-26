from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .levels import LEVEL_THRESHOLDS, level_progress
from .services import get_achievements_for_user, get_profile_stats, get_recent_activity


@login_required
def profile(request):
    """«Мой прогресс»: уровень и XP, достижения, лента активности."""
    user = request.user
    achievements = get_achievements_for_user(user)
    return render(
        request,
        "gamification/profile.html",
        {
            "progress": level_progress(user.xp or 0),
            "max_level": len(LEVEL_THRESHOLDS),
            "achievements": achievements,
            "earned_count": sum(1 for a in achievements if a["earned"]),
            "activity": get_recent_activity(user),
            "stats": get_profile_stats(user),
        },
    )
