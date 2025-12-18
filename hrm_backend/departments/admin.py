from django.contrib import admin
from .models import Department
# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id', 'dept_name', 'status', 'created_at', 'updated_at')
    list_filter = ['status']
    search_fields = ['dept_name']