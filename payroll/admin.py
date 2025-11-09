from django.contrib import admin
from .models import Payroll, Payslip, Loan, Bonus

admin.site.register(Payroll)
admin.site.register(Payslip)
admin.site.register(Loan)
admin.site.register(Bonus)

