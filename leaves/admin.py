from django.contrib import admin
from .models import LeavePolicy, LeaveBalance, LeaveApprovalWorkflow

admin.site.register(LeavePolicy)
admin.site.register(LeaveBalance)
admin.site.register(LeaveApprovalWorkflow)

