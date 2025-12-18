from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/otp/<uuid:token>/', views.password_reset_otp, name='password_reset_otp'),
    path('password-reset/new/', views.password_reset_new, name='password_reset_new'),
]
