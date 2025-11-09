"""
Admin configuration for organization app
"""
from django.contrib import admin
from .models import (
    Department, Position, Branch, WorkShift, Holiday
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Department Admin"""
    list_display = ['dept_code', 'dept_name_ar', 'parent_department', 'manager', 'location']
    list_filter = ['parent_department']
    search_fields = ['dept_code', 'dept_name_ar', 'dept_name_en']
    ordering = ['dept_code']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Position Admin"""
    list_display = ['position_code', 'position_name_ar', 'department', 'level', 'min_salary', 'max_salary']
    list_filter = ['department', 'level']
    search_fields = ['position_code', 'position_name_ar', 'position_name_en']
    ordering = ['position_code']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """Branch Admin"""
    list_display = ['branch_code', 'branch_name_ar', 'city', 'manager', 'is_active']
    list_filter = ['is_active', 'city']
    search_fields = ['branch_code', 'branch_name_ar', 'branch_name_en', 'city']
    ordering = ['branch_code']


@admin.register(WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    """Work Shift Admin"""
    list_display = ['shift_name', 'start_time', 'end_time', 'is_active']
    list_filter = ['is_active']
    search_fields = ['shift_name', 'description']
    ordering = ['start_time']


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    """Holiday Admin"""
    list_display = ['name', 'date', 'holiday_type', 'is_recurring']
    list_filter = ['is_recurring', 'holiday_type', 'date']
    search_fields = ['name', 'description']
    ordering = ['-date']

