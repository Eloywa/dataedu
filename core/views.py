from django.shortcuts import render

from courses.models import Lesson
from learning.models import Enrollment, LessonProgress


def home(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, "core/home.html")

    if user.is_teacher:
        return render(request, "core/home_teacher.html")

    # Студент: найти курс «в процессе» и следующий незавершённый урок
    enrollments = Enrollment.objects.filter(user=user).select_related("course").order_by("-enrolled_at")
    current = None
    for e in enrollments:
        course = e.course
        lessons = list(
            Lesson.objects.filter(module__course=course).order_by("module__order_index", "order_index")
        )
        if not lessons:
            continue
        completed = set(
            LessonProgress.objects.filter(
                user=user, lesson__module__course=course, status="completed"
            ).values_list("lesson_id", flat=True)
        )
        nxt = next((l for l in lessons if l.id not in completed), None)
        if nxt is not None:
            done, total = len(completed), len(lessons)
            current = {
                "course": course,
                "next_lesson": nxt,
                "done": done,
                "total": total,
                "pct": round(done * 100 / total),
            }
            break

    return render(
        request,
        "core/home_student.html",
        {"current": current, "enroll_count": enrollments.count()},
    )
