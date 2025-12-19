from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("add/", views.add_review, name="add_review"),
    path("<int:pk>/edit/", views.edit_review, name="edit_review"),
    path("<int:pk>/delete/", views.delete_review, name="delete_review"),
    path("employee/<int:employee_id>/", views.employee_dashboard, name="employee_dashboard"),
]
