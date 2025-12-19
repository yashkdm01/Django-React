from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Task, TaskAssignment
from .forms import TaskForm, TaskAssignmentForm


def manager_dashboard(request):
    """Dashboard for Manager / TL to see all tasks."""
    # filters from query params
    employee = request.GET.get("employee")
    status = request.GET.get("status")
    date_from = request.GET.get("from")
    date_to = request.GET.get("to")

    assignments = TaskAssignment.objects.select_related("task").all()

    if employee:
        assignments = assignments.filter(employee_name__icontains=employee)

    if status:
        assignments = assignments.filter(status=status)

    if date_from:
        assignments = assignments.filter(task__start_date__gte=date_from)

    if date_to:
        assignments = assignments.filter(task__start_date__lte=date_to)

    # statistics
    stats = assignments.values("status").annotate(total=Count("id"))
    status_map = {"Pending": 0, "In Progress": 0, "Completed": 0}
    for row in stats:
        status_map[row["status"]] = row["total"]

    context = {
        "assignments": assignments.order_by("-assigned_date")[:20],
        "status_counts": status_map,
        "filters": {
            "employee": employee or "",
            "status": status or "",
            "from": date_from or "",
            "to": date_to or "",
        },
    }
    return render(request, "tasks/manager_dashboard.html", context)


def employee_dashboard(request, employee_name):
    """Dashboard for a single employee."""
    assignments = TaskAssignment.objects.select_related("task").filter(
        employee_name=employee_name
    )

    stats = assignments.values("status").annotate(total=Count("id"))
    status_map = {"Pending": 0, "In Progress": 0, "Completed": 0}
    for row in stats:
        status_map[row["status"]] = row["total"]

    context = {
        "employee_name": employee_name,
        "assignments": assignments.order_by("-assigned_date"),
        "status_counts": status_map,
    }
    return render(request, "tasks/employee_dashboard.html", context)


def task_create(request):
    if request.method == "POST":
        task_form = TaskForm(request.POST)
        assign_form = TaskAssignmentForm(request.POST)
        if task_form.is_valid() and assign_form.is_valid():
            task = task_form.save()
            assignment = assign_form.save(commit=False)
            assignment.task = task
            if assignment.status == "Completed":
                assignment.completed_at = timezone.now()
            assignment.save()
            return redirect("manager_dashboard")
    else:
        task_form = TaskForm()
        assign_form = TaskAssignmentForm()
    return render(
        request,
        "tasks/task_form.html",
        {"task_form": task_form, "assign_form": assign_form, "title": "Create Task"},
    )



def task_update(request, assignment_id):
    assignment = get_object_or_404(TaskAssignment, id=assignment_id)
    task = assignment.task

    if request.method == "POST":
        task_form = TaskForm(request.POST, instance=task)
        assign_form = TaskAssignmentForm(request.POST, instance=assignment)
        if task_form.is_valid() and assign_form.is_valid():
            task_form.save()
            assignment = assign_form.save(commit=False)
            if assignment.status == "Completed" and not assignment.completed_at:
                assignment.completed_at = timezone.now()
            assignment.save()
            return redirect("manager_dashboard")
    else:
        task_form = TaskForm(instance=task)
        assign_form = TaskAssignmentForm(instance=assignment)

    return render(
        request,
        "tasks/task_form.html",
        {"task_form": task_form, "assign_form": assign_form, "title": "Update Task"},
    )


def task_delete(request, assignment_id):
    assignment = get_object_or_404(TaskAssignment, id=assignment_id)

    if request.method == "POST":
        assignment.delete()
        return redirect("manager_dashboard")

    return render(request, "tasks/task_confirm_delete.html", {"assignment": assignment})


def mark_completed(request, assignment_id):
    assignment = get_object_or_404(TaskAssignment, id=assignment_id)
    assignment.status = "Completed"
    assignment.completed_at = timezone.now()
    assignment.save()
    return redirect("manager_dashboard")
