from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(
        label="Username or Email Address",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def get_user(self):
        data = self.cleaned_data["email_or_username"]
        try:
            return User.objects.get(username=data)
        except User.DoesNotExist:
            try:
                return User.objects.get(email=data)
            except User.DoesNotExist:
                return None

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        label="One Time Password",
        max_length=6,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

class PasswordResetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "New Password"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm New Password"}
        )
