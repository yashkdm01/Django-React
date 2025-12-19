from django.contrib import admin
from .models import Employee, Leave, LeaveQuota

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ("leave_id", "employee", "leave_type", "start_date", "end_date", "status")
    list_filter = ("leave_type", "status")
    search_fields = ("employee__user__username", "employee__user__first_name")

@admin.register(LeaveQuota)
class LeaveQuotaAdmin(admin.ModelAdmin):
    list_display = ("quota_id", "employee", "leave_type", "total_quota", "used_quota", "remaining_quota")
    list_filter = ("leave_type",)
