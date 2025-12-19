from django import forms
from .models import Task, TaskAssignment


class DateInput(forms.DateInput):
    input_type = "date"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "task_title",
            "task_description",
            "task_priority",
            "start_date",
            "end_date",
            "task_type",
        ]
        widgets = {
            "task_title": forms.TextInput(attrs={"class": "form-control"}),
            "task_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "task_priority": forms.Select(attrs={"class": "form-select"}),
            "start_date": DateInput(attrs={"class": "form-control"}),
            "end_date": DateInput(attrs={"class": "form-control"}),
            "task_type": forms.Select(attrs={"class": "form-select"}),
        }


class TaskAssignmentForm(forms.ModelForm):
    class Meta:
        model = TaskAssignment
        exclude = ["task", "assigned_date", "completed_at"]
        widgets = {
            "employee_name": forms.TextInput(attrs={"class": "form-control"}),
            "assigned_by": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
