import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from courses.models import Lesson
from gamification import services

from .grading import rows_equal
from .models import AnswerSubmission, Assignment, Submission, TestAttempt


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

        # Событие, XP за первое прохождение, «Знаток тестов», отметка урока.
        services.finish_test(request.user, attempt, lesson)

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


@login_required
def practice(request):
    assignments = list(
        Assignment.objects.filter(type="sql").select_related("course").order_by("course__title", "title")
    )
    solved = set(
        Submission.objects.filter(user=request.user, score__gte=1).values_list("assignment_id", flat=True)
    )
    for a in assignments:
        a.is_solved = a.id in solved
    return render(request, "assessments/practice_list.html", {"assignments": assignments})


@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment.objects.select_related("course"), id=assignment_id)
    solved = Submission.objects.filter(
        user=request.user, assignment=assignment, score__gte=1
    ).exists()
    return render(
        request,
        "assessments/assignment_detail.html",
        {"assignment": assignment, "solved": solved},
    )


@login_required
@require_POST
def check_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if not assignment.expected_result:
        return JsonResponse({"passed": False, "message": "Эталон для задания не настроен."}, status=400)

    try:
        payload = json.loads(request.body)
        sql = (payload.get("sql") or "").strip()
        columns = payload.get("columns") or []
        rows = payload.get("rows") or []
    except (ValueError, TypeError):
        return JsonResponse({"passed": False, "message": "Некорректные данные."}, status=400)

    expected = assignment.expected_result
    passed = rows_equal(columns, rows, expected.get("columns", []), expected.get("rows", []))

    # Сервер ставит итог независимо от браузера (целостность оценки).
    submission = Submission.objects.create(
        assignment=assignment,
        user=request.user,
        sql_query=sql,
        score=assignment.max_score if passed else 0,
        status="graded",
        feedback="Автопроверка: " + ("верно" if passed else "неверно"),
        submitted_at=timezone.now(),
        graded_at=timezone.now(),
    )
    services.record_submission(request.user, submission)

    message = "" if passed else (
        f"Ожидалось строк: {len(expected.get('rows', []))}, у вас: {len(rows)}."
    )
    return JsonResponse({"passed": passed, "message": message})
