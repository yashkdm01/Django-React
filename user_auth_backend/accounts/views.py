from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
import random

from .forms import (
    LoginForm,
    PasswordResetRequestForm,
    OTPVerificationForm,
    PasswordResetForm,
)
from .models import PasswordResetOTP

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

def logout_view(request):
    logout(request)
    return redirect("login")

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user:
                messages.error(request, "No user found with that username/email.")
            else:
                code = f"{random.randint(0, 999999):06d}"
                otp_obj = PasswordResetOTP.objects.create(user=user, code=code)

                print("PASSWORD RESET OTP:", code)

                reset_url = reverse("password_reset_otp", args=[otp_obj.token])
                request.session["reset_token"] = str(otp_obj.token)

                messages.success(
                    request,
                    "An OTP has been generated and sent to your registered email."
                )
                return redirect("password_reset_otp", token=otp_obj.token)
    else:
        form = PasswordResetRequestForm()
    return render(request, "accounts/password_reset_request.html", {"form": form})

def password_reset_otp(request, token):
    otp_obj = get_object_or_404(PasswordResetOTP, token=token, is_used=False)
    if otp_obj.is_expired():
        messages.error(request, "OTP has expired. Please request a new one.")
        return redirect("password_reset_request")

    if request.method == "POST":
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["otp"] == otp_obj.code:
                otp_obj.is_used = True
                otp_obj.save()
                request.session["reset_user_id"] = otp_obj.user.id
                return redirect("password_reset_new")
            else:
                messages.error(request, "Invalid OTP.")
    else:
        form = OTPVerificationForm()
    return render(request, "accounts/password_reset_otp.html", {"form": form})

def password_reset_new(request):
    user_id = request.session.get("reset_user_id")
    if not user_id:
        return redirect("password_reset_request")

    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = PasswordResetForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password has been reset. Please login.")
            request.session.pop("reset_user_id", None)
            return redirect("login")
    else:
        form = PasswordResetForm(user)
    return render(request, "accounts/password_reset_new.html", {"form": form})
