from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from courses.models import Lesson
from learning.models import LessonProgress

from .models import AnswerSubmission, TestAttempt


@login_required
def lesson_test(request, lesson_id):
    lesson = get_object_or_404(Lesson.objects.select_related("module__course"), id=lesson_id)
    test = lesson.tests.first()
    if test is None:
        return redirect("courses:lesson_detail", lesson_id=lesson_id)

    questions = list(test.questions.prefetch_related("options").all())

    if request.method == "POST":
        total_points = 0
        earned = 0
        results = []
        for q in questions:
            total_points += q.points
            options = list(q.options.all())
            option_ids = {str(o.id) for o in options}
            correct = next((o for o in options if o.is_correct), None)

            chosen_id = request.POST.get(f"q_{q.id}")
            if chosen_id not in option_ids:  # защита от подделки/пустого
                chosen_id = None
            is_correct = bool(correct and chosen_id and str(correct.id) == chosen_id)
            if is_correct:
                earned += q.points

            results.append(
                {
                    "question": q,
                    "options": options,
                    "chosen_id": chosen_id,
                    "correct_id": str(correct.id) if correct else None,
                    "is_correct": is_correct,
                }
            )

        score = round(earned * 100 / total_points) if total_points else 0
        is_passed = score >= test.pass_score

        attempt = TestAttempt.objects.create(
            user=request.user,
            test=test,
            score=score,
            is_passed=is_passed,
            started_at=timezone.now(),
            finished_at=timezone.now(),
        )
        AnswerSubmission.objects.bulk_create(
            [
                AnswerSubmission(
                    attempt=attempt,
                    question=r["question"],
                    answer_option_id=r["chosen_id"],
                    is_correct=r["is_correct"],
                )
                for r in results
            ]
        )

        if is_passed:
            LessonProgress.objects.update_or_create(
                user=request.user,
                lesson=lesson,
                defaults={"status": "completed", "completed_at": timezone.now()},
            )
        # TODO (этап 9): начисление XP и проверка достижений за прохождение теста.

        return render(
            request,
            "assessments/test_result.html",
            {"lesson": lesson, "test": test, "score": score, "is_passed": is_passed, "results": results},
        )

    return render(
        request,
        "assessments/test.html",
        {"lesson": lesson, "test": test, "questions": questions},
    )
