from django.contrib import admin
from .models import Attendance, AttendanceLog, LeaveRequest, Overtime

admin.site.register(Attendance)
admin.site.register(AttendanceLog)
admin.site.register(LeaveRequest)
admin.site.register(Overtime)

