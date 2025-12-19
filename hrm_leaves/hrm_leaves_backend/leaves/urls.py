from django.urls import path
from . import views

app_name = "leaves"

urlpatterns = [
    path("", views.employee_dashboard, name="employee_dashboard"),
    path("apply/", views.apply_leave, name="apply_leave"),
    path("leave/<int:pk>/update/", views.update_leave, name="update_leave"),
    path("manager/", views.manager_dashboard, name="manager_dashboard"),
    path("manager/leave/<int:pk>/", views.approve_leave, name="approve_leave"),
]
