from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LeaveForm
from .models import Leave, LeaveQuota, Employee


def is_manager(user):
    return user.is_staff or user.is_superuser


@login_required
def employee_dashboard(request):
    employee = get_object_or_404(Employee, user=request.user)

    quotas = LeaveQuota.objects.filter(employee=employee)
    leaves = Leave.objects.filter(employee=employee).order_by("-start_date")

    context = {
        "employee": employee,
        "quotas": quotas,
        "leaves": leaves,
    }
    return render(request, "leaves/employee_dashboard.html", context)


@login_required
def apply_leave(request):
    employee = get_object_or_404(Employee, user=request.user)

    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee
            days = (leave.end_date - leave.start_date).days + 1
            leave.total_days = max(days, 0)
            leave.status = "pending"
            leave.save()  # <-- always save now

            messages.success(request, "Leave applied successfully.")
            return redirect("leaves:employee_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LeaveForm()

    return render(request, "leaves/apply_leave.html", {"form": form})



@login_required
def update_leave(request, pk):
    employee = get_object_or_404(Employee, user=request.user)
    leave = get_object_or_404(Leave, pk=pk, employee=employee)

    if leave.status != "pending":
        messages.error(request, "You can edit only pending leaves.")
        return redirect("leaves:employee_dashboard")

    if request.method == "POST":
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            leave = form.save(commit=False)
            days = (leave.end_date - leave.start_date).days + 1
            leave.total_days = max(days, 0)
            leave.save()
            messages.success(request, "Leave updated successfully.")
            return redirect("leaves:employee_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LeaveForm(instance=leave)

    return render(request, "leaves/update_leave.html", {"form": form, "leave": leave})


@user_passes_test(is_manager)
def manager_dashboard(request):
    manager_emp = Employee.objects.filter(user=request.user).first()
    leaves = Leave.objects.all().order_by("-start_date")
    context = {
        "manager": manager_emp,
        "leaves": leaves,
    }
    return render(request, "leaves/manager_dashboard.html", context)


@user_passes_test(is_manager)
def approve_leave(request, pk):
    leave = get_object_or_404(Leave, pk=pk)

    if request.method == "POST":
        status = request.POST.get("status")
        if status not in ["approved", "rejected", "pending"]:
            messages.error(request, "Invalid status.")
            return redirect("leaves:manager_dashboard")

        previous_status = leave.status
        leave.status = status

        manager_emp = Employee.objects.filter(user=request.user).first()
        leave.approved_by = manager_emp
        leave.save()

        # Adjust quota only when transitioning to approved
        if previous_status != "approved" and status == "approved":
            try:
                quota = LeaveQuota.objects.get(employee=leave.employee, leave_type=leave.leave_type)
                quota.used_quota += leave.total_days
                quota.remaining_quota = quota.total_quota - quota.used_quota
                quota.save()
            except LeaveQuota.DoesNotExist:
                # If no quota row exists, just skip instead of erroring
                pass

        messages.success(request, "Leave updated.")
        return redirect("leaves:manager_dashboard")

    return render(request, "leaves/approve_leave.html", {"leave": leave})
