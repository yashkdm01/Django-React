from django import forms
from .models import Leave


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ["leave_type", "reason", "start_date", "end_date"]

        # Optional: add basic Bootstrap classes to widgets
        widgets = {
            "leave_type": forms.Select(attrs={"class": "form-select"}),
            "reason": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }
    