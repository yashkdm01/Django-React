from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'email', 'mobile',
            'role_id', 'dept_id', 'reporting_manager_id',
            'date_of_joining', 'username', 'password',
        ]
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }
