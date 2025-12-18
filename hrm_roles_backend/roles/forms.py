from django import forms
from .models import Role

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name', 'description', 'status']
        widgets = {
            'role_name': forms.TextInput(attrs= {'class': 'form-control'}),
            'description': forms.Textarea(attrs= {'class': 'form-control', 'rows': 3}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }