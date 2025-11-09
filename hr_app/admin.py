# hr_app/admin.py
from django.contrib import admin
from .models import (
    TblAttendance,
    TblEmployees,
    TblLates,
    TblLeaves,
    TblLoans,
    TblLogs,
    TblOvertime,
    TblPayslips,
    TblSettings,
    TblStagingAttendance,
    TblStagingAttendanceLog,
    TblStagingAttendanceTemp,
)

# يمكنك تسجيلها كلها دفعة واحدة
admin.site.register(TblAttendance)
admin.site.register(TblEmployees)
admin.site.register(TblLates)
admin.site.register(TblLeaves)
admin.site.register(TblLoans)
admin.site.register(TblLogs)
admin.site.register(TblOvertime)
admin.site.register(TblPayslips)
admin.site.register(TblSettings)
admin.site.register(TblStagingAttendance)
admin.site.register(TblStagingAttendanceLog)
admin.site.register(TblStagingAttendanceTemp)