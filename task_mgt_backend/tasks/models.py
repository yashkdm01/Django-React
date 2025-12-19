from django.db import models
from django.utils import timezone


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    TASK_TYPE_CHOICES = [
        ("Individual", "Individual"),
        ("Team", "Team"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    task_title = models.CharField(max_length=100)
    task_description = models.CharField(max_length=300)
    task_priority = models.CharField(max_length=200, choices=PRIORITY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_title


class TaskAssignment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]


    employee_name = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assignments")
    assigned_by = models.CharField(max_length=100)
    assigned_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="Pending")
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.task.task_title} → {self.employee_name}"
