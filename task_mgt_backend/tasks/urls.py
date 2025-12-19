from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path(
        "dashboard/employee/<str:employee_name>/",
        views.employee_dashboard,
        name="employee_dashboard",
    ),
    path("tasks/create/", views.task_create, name="task_create"),
    path("tasks/<int:assignment_id>/edit/", views.task_update, name="task_update"),
    path("tasks/<int:assignment_id>/delete/", views.task_delete, name="task_delete"),
    path(
        "tasks/<int:assignment_id>/complete/",
        views.mark_completed,
        name="task_mark_completed",
    ),
]
