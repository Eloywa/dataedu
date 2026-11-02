"""Задания в структуре курса: состояние для студента и раскладка по блокам и урокам."""

from gamification import services

from . import projects
from .models import Assignment, Submission

STATE_META = {
    "solved": {"label": "решено", "tone": "success"},
    "graded": {"label": "оценено", "tone": "success"},
    "failed": {"label": "не решено", "tone": "neutral"},
    "submitted": {"label": "на проверке", "tone": "neutral"},
    "returned": {"label": "на доработке", "tone": "warning"},
}


def task_states(user, tasks):
    """Состояние заданий для студента: {id задания: подпись и тон метки}.

    Задание без сдач в словарь не попадает. Решённым считается то, где хоть раз получен
    балл: у автопроверки пробуют много раз, и последняя неудачная попытка не отменяет
    уже решённого.
    """
    if not user.is_authenticated:
        return {}
    by_id = {task.id: task for task in tasks}
    best, last = {}, {}
    rows = (
        Submission.objects.filter(user=user, assignment_id__in=by_id)
        .order_by("submitted_at")
        .values_list("assignment_id", "status", "score")
    )
    for task_id, status, score in rows:
        best[task_id] = max(best.get(task_id, 0), score or 0)
        last[task_id] = status

    states = {}
    for task_id, status in last.items():
        if best[task_id] >= 1:
            code = "solved" if by_id[task_id].is_autocheckable else "graded"
        elif status == "graded":
            code = "failed"
        else:
            code = status
        states[task_id] = STATE_META.get(code, STATE_META["submitted"])
    return states


def grouped_tasks(user):
    """Задания раскладкой курс → блок → урок для страницы «Задания».

    Задание закрытой недели видно, но не открывается: студент заранее знает, что его
    ждёт. Итоговый проект и задания без урока идут отдельно, неделям они не подчинены.
    """
    tasks = list(
        Assignment.objects.visible_to(user)
        .select_related("course", "lesson__module")
        .order_by("course__title", "title")
    )
    states = task_states(user, tasks)

    courses = {}
    for task in tasks:
        task.state = states.get(task.id)
        group = courses.setdefault(
            task.course_id, {"course": task.course, "finals": [], "blocks": {}, "loose": []}
        )
        if task.is_final:
            task.ticket = projects.ticket_state(user, task)
            group["finals"].append(task)
        elif task.lesson_id:
            module = task.lesson.module
            block = group["blocks"].setdefault(module.id, {"module": module, "lessons": {}})
            row = block["lessons"].setdefault(task.lesson_id, {"lesson": task.lesson, "tasks": []})
            row["tasks"].append(task)
        else:
            group["loose"].append(task)

    result = []
    for group in courses.values():
        gating = services.course_gating(user, group["course"], user.is_teacher)
        blocks = sorted(group["blocks"].values(), key=lambda b: b["module"].order_index)
        for block in blocks:
            gate = gating.get(block["module"].id, {"unlocked": True})
            block["unlocked"] = gate["unlocked"]
            block["lessons"] = sorted(
                block["lessons"].values(), key=lambda row: row["lesson"].order_index
            )
        group["blocks"] = blocks
        result.append(group)
    return result
