from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # extra fields later if needed

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ("SL", "Sick Leave"),
        ("CL", "Casual Leave"),
        ("PL", "Privilege Leave"),
        ("LWP", "Leave Without Pay"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    leave_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leaves")
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    reason = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_leaves",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"


class LeaveQuota(models.Model):
    LEAVE_TYPE_CHOICES = [
        ("SL", "Sick Leave"),
        ("CL", "Casual Leave"),
        ("PL", "Privilege Leave"),
    ]

    quota_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="quotas")
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    total_quota = models.IntegerField()
    used_quota = models.IntegerField(default=0)
    remaining_quota = models.IntegerField()

    class Meta:
        unique_together = ("employee", "leave_type")

    def __str__(self):
        return f"{self.employee} - {self.leave_type}"
