from django.db import models


class TblEmployees(models.Model):
    emp_id = models.AutoField(db_column='Emp_ID', primary_key=True)
    emp_code = models.CharField(db_column='Emp_Code', unique=True, max_length=20, blank=True, null=True)
    emp_fullname = models.CharField(db_column='Emp_FullName', max_length=200)
    national_id = models.CharField(db_column='National_ID', max_length=14, blank=True, null=True)
    job_title = models.CharField(db_column='Job_Title', max_length=100, blank=True, null=True)
    department = models.CharField(db_column='Department', max_length=100, blank=True, null=True)
    hire_date = models.DateField(db_column='Hire_Date', blank=True, null=True)
    salary_basic = models.DecimalField(db_column='Salary_Basic', max_digits=18, decimal_places=2, blank=True, null=True)
    salary_housing = models.DecimalField(db_column='Salary_Housing', max_digits=18, decimal_places=2, blank=True, null=True)
    salary_transport = models.DecimalField(db_column='Salary_Transport', max_digits=18, decimal_places=2, blank=True, null=True)
    salary_other = models.DecimalField(db_column='Salary_Other', max_digits=18, decimal_places=2, blank=True, null=True)
    salary_total = models.DecimalField(db_column='Salary_Total', max_digits=21, decimal_places=2, blank=True, null=True, editable=False)
    allowed_annual_leaves = models.IntegerField(db_column='Allowed_Annual_Leaves', blank=True, null=True)
    allowed_sick_leaves = models.IntegerField(db_column='Allowed_Sick_Leaves', blank=True, null=True)
    allowed_casual_leaves = models.IntegerField(db_column='Allowed_Casual_Leaves', blank=True, null=True)
    work_start = models.TimeField(db_column='Work_Start', blank=True, null=True)
    work_end = models.TimeField(db_column='Work_End', blank=True, null=True)
    telegram_userid = models.CharField(db_column='Telegram_UserID', max_length=50, blank=True, null=True)
    is_active = models.BooleanField(db_column='Is_Active')

    class Meta:
        managed = False
        db_table = 'Tbl_Employees'

    def save(self, *args, **kwargs):
        # Calculate salary_total before saving
        if self.salary_basic is not None or self.salary_housing is not None or self.salary_transport is not None or self.salary_other is not None:
            basic = self.salary_basic or 0
            housing = self.salary_housing or 0
            transport = self.salary_transport or 0
            other = self.salary_other or 0
            self.salary_total = basic + housing + transport + other
        super().save(*args, **kwargs)

    def __str__(self):
        return self.emp_fullname


class TblAttendance(models.Model):
    attendance_id = models.AutoField(db_column='Attendance_ID', primary_key=True)
    emp = models.ForeignKey('TblEmployees', on_delete=models.CASCADE, db_column='Emp_ID', blank=True, null=True)
    attendance_date = models.DateField(db_column='Attendance_Date')
    checkin_time = models.DateTimeField(db_column='CheckIn_Time', blank=True, null=True)
    checkout_time = models.DateTimeField(db_column='CheckOut_Time', blank=True, null=True)
    work_hours = models.DecimalField(db_column='Work_Hours', max_digits=5, decimal_places=2, blank=True, null=True)
    late_minutes = models.IntegerField(db_column='Late_Minutes', blank=True, null=True)
    overtime_hours = models.DecimalField(db_column='Overtime_Hours', max_digits=5, decimal_places=2, blank=True, null=True)
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tbl_Attendance'

    def __str__(self):
        return f"{self.emp.emp_fullname if self.emp else 'N/A'} - {self.attendance_date}"


class TblLates(models.Model):
    late_id = models.AutoField(db_column='Late_ID', primary_key=True)
    emp = models.ForeignKey('TblEmployees', on_delete=models.CASCADE, db_column='Emp_ID', blank=True, null=True)
    late_date = models.DateField(db_column='Late_Date')
    late_minutes = models.IntegerField(db_column='Late_Minutes')
    reason = models.CharField(db_column='Reason', max_length=200, blank=True, null=True)
    deduction_amount = models.DecimalField(db_column='Deduction_Amount', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tbl_Lates'


class TblLeaves(models.Model):
    leave_id = models.AutoField(db_column='Leave_ID', primary_key=True)
    emp = models.ForeignKey('TblEmployees', on_delete=models.CASCADE, db_column='Emp_ID', blank=True, null=True)
    start_date = models.DateField(db_column='Start_Date', blank=True, null=True)
    end_date = models.DateField(db_column='End_Date', blank=True, null=True)
    leave_type = models.CharField(db_column='Leave_Type', max_length=50, blank=True, null=True)
    leave_days = models.IntegerField(db_column='Leave_Days', blank=True, null=True)
    approved_by = models.CharField(db_column='Approved_By', max_length=100, blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tbl_Leaves'


class TblLoans(models.Model):
    loan_id = models.AutoField(db_column='Loan_ID', primary_key=True)
    emp = models.ForeignKey('TblEmployees', on_delete=models.CASCADE, db_column='Emp_ID', blank=True, null=True)
    loan_date = models.DateField(db_column='Loan_Date')
    loan_amount = models.DecimalField(db_column='Loan_Amount', max_digits=10, decimal_places=2)
    repayment_per_month = models.DecimalField(db_column='Repayment_Per_Month', max_digits=10, decimal_places=2, blank=True, null=True)
    remaining_amount = models.DecimalField(db_column='Remaining_Amount', max_digits=22, decimal_places=2, blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tbl_Loans'


class TblLogs(models.Model):
    log_id = models.AutoField(db_column='Log_ID', primary_key=True)
    emp_id = models.IntegerField(db_column='Emp_ID', blank=True, null=True)
    action = models.CharField(db_column='Action', max_length=100, blank=True, null=True)
    action_details = models.TextField(db_column='Action_Details', blank=True, null=True)
    performed_by = models.CharField(db_column='Performed_By', max_length=100, blank=True, null=True)
    performed_at = models.DateTimeField(db_column='Performed_At', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tbl_Logs'


class TblOvertime(models.Model):
    ot_id = models.AutoField(db_column='OT_ID', primary_key=True)
    emp = models.ForeignKey('TblEmployees', on_delete=models.CASCADE, db_column='Emp_ID', blank=True, null=True)
    ot_date = models.DateField(db_column='OT_Date')
    ot_hours = models.DecimalField(db_column='OT_Hours', max_digits=5, decimal_places=2, blank=True, null=True)
    ot_type = models.CharField(db_column='OT_Type', max_length=20, blank=True, null=True)
    ot_amount = models.DecimalField(db_column='OT_Amount', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tbl_Overtime'


class TblPayslips(models.Model):
    payslip_id = models.AutoField(db_column='Payslip_ID', primary_key=True)
    emp = models.ForeignKey('TblEmployees', on_delete=models.CASCADE, db_column='Emp_ID', blank=True, null=True)
    period_start = models.DateField(db_column='Period_Start', blank=True, null=True)
    period_end = models.DateField(db_column='Period_End', blank=True, null=True)
    gross_pay = models.DecimalField(db_column='Gross_Pay', max_digits=10, decimal_places=2, blank=True, null=True)
    total_deductions = models.DecimalField(db_column='Total_Deductions', max_digits=10, decimal_places=2, blank=True, null=True)
    net_pay = models.DecimalField(db_column='Net_Pay', max_digits=11, decimal_places=2, blank=True, null=True)
    generated_at = models.DateTimeField(db_column='Generated_At', blank=True, null=True)
    payslip_file = models.CharField(db_column='Payslip_File', max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tbl_Payslips'


class TblSettings(models.Model):
    setting_id = models.AutoField(db_column='Setting_ID', primary_key=True)
    company_name = models.CharField(db_column='Company_Name', max_length=200, blank=True, null=True)
    workday_start = models.TimeField(db_column='Workday_Start')
    workday_end = models.TimeField(db_column='Workday_End')
    lunch_break_minutes = models.IntegerField(db_column='Lunch_Break_Minutes')
    late_threshold_min = models.IntegerField(db_column='Late_Threshold_Min')
    overtime_rate = models.FloatField(db_column='Overtime_Rate')
    monthly_working_hours = models.FloatField(db_column='Monthly_Working_Hours')
    salary_currency = models.CharField(db_column='Salary_Currency', max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tbl_Settings'

    def __str__(self):
        return self.company_name or "Settings"


class TblStagingAttendance(models.Model):
    staging_id = models.AutoField(db_column='Staging_ID', primary_key=True)
    raw_userid = models.CharField(db_column='Raw_UserID', max_length=100, blank=True, null=True)
    raw_name = models.CharField(db_column='Raw_Name', max_length=200, blank=True, null=True)
    raw_datetime = models.CharField(db_column='Raw_DateTime', max_length=100, blank=True, null=True)
    raw_state = models.CharField(db_column='Raw_State', max_length=50, blank=True, null=True)
    parsed_date = models.DateField(db_column='Parsed_Date', blank=True, null=True)
    parsed_checktime = models.DateTimeField(db_column='Parsed_CheckTime', blank=True, null=True)
    parsed_state = models.CharField(db_column='Parsed_State', max_length=50, blank=True, null=True)
    parsed_emp_id = models.IntegerField(db_column='Parsed_Emp_ID', blank=True, null=True)
    processed = models.BooleanField(db_column='Processed', blank=True, null=True)
    processed_at = models.DateTimeField(db_column='Processed_At', blank=True, null=True)
    errormsg = models.CharField(db_column='ErrorMsg', max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tbl_Staging_Attendance'


class TblStagingAttendanceLog(models.Model):
    logid = models.AutoField(db_column='LogID', primary_key=True)
    logtime = models.DateTimeField(db_column='LogTime')
    filename = models.CharField(db_column='FileName', max_length=255, blank=True, null=True)
    errormessage = models.TextField(db_column='ErrorMessage', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tbl_Staging_Attendance_Log'


class TblStagingAttendanceTemp(models.Model):
    raw_userid = models.CharField(db_column='Raw_UserID', max_length=50, blank=True, null=True)
    raw_name = models.CharField(db_column='Raw_Name', max_length=100, blank=True, null=True)
    raw_datetime = models.CharField(db_column='Raw_DateTime', max_length=50, blank=True, null=True)
    raw_state = models.CharField(db_column='Raw_State', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tbl_Staging_Attendance_Temp'
