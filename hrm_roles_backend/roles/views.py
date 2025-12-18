from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q

from .models import Role
from .forms import RoleForm


def role_list(request):
    query = request.GET.get("q", "").strip()

    roles = Role.objects.filter(status=True)
    if query:
        roles = roles.filter(Q(role_name__icontains=query) |
                             Q(description__icontains=query))

    context = {
        "roles": roles.order_by("id"),
        "query": query,
        "active_count": Role.objects.filter(status=True).count(),
        "inactive_count": Role.objects.filter(status=False).count(),
    }
    return render(request, "roles/role_list.html", context)


def role_create(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Role created successfully.")
            return redirect("role_list")
    else:
        form = RoleForm()

    return render(request, "roles/role_form.html", {"form": form, "title": "Create Role"})


def role_update(request, pk):
    role = get_object_or_404(Role, pk=pk)

    if request.method == "POST":
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, "Role updated successfully.")
            return redirect("role_list")  
    else:
        form = RoleForm(instance=role)

    return render(request, "roles/role_form.html", {"form": form, "title": "Update Role"})


def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)

    if request.method == "POST":
        role.status = False
        role.save()
        messages.warning(request, f"Role '{role.role_name}' has been marked as inactive.")
        return redirect("role_list")

    return render(request, "roles/role_confirm_delete.html", {"role": role})
