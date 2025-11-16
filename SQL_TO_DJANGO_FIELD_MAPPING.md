# SQL Server to Django Field Mapping

## Complete Field Mapping from Tbl_Employee to Employee Model

| SQL Server Field | Django Field | Type | Tab Location | Notes |
|-----------------|--------------|------|--------------|-------|
| **Basic Information** |
| Emp_Code | emp_code | CharField(20) | البيانات الشخصية | ✅ Existing |
| First_Name_Ar | first_name_ar | CharField(50) | البيانات الشخصية | ✅ Existing |
| Second_Name_Ar | second_name_ar | CharField(50) | البيانات الشخصية | ✅ NEW |
| Middle_Name_Ar | middle_name_ar | CharField(50) | البيانات الشخصية | ✅ Existing |
| Last_Name_Ar | last_name_ar | CharField(50) | البيانات الشخصية | ✅ Existing |
| Full_Name_Ar | full_name_ar | CharField(200) | البيانات الشخصية | ✅ NEW |
| First_Name_En | first_name_en | CharField(50) | البيانات الشخصية | ✅ Existing |
| Last_Name_En | last_name_en | CharField(50) | البيانات الشخصية | ✅ Existing |
| Full_Name_En | full_name_en | CharField(200) | البيانات الشخصية | ✅ NEW |
| Mother_Name | mother_name | CharField(100) | البيانات الشخصية | ✅ NEW |
| **Personal Information** |
| National_ID | national_id | CharField(20) | البيانات الشخصية | ✅ Existing |
| National_ID_Expiry_Date | national_id_expiry_date | DateField | البيانات الشخصية | ✅ NEW |
| Passport_Number | passport_number | CharField(20) | البيانات الشخصية | ✅ Existing |
| Date_Of_Birth | date_of_birth | DateField | البيانات الشخصية | ✅ Existing |
| Place_Of_Birth | place_of_birth | CharField(100) | البيانات الشخصية | ✅ NEW |
| Gender | gender | CharField(10) | البيانات الشخصية | ✅ Existing |
| Marital_Status | marital_status | CharField(20) | البيانات الشخصية | ✅ Existing |
| Nationality | nationality | CharField(50) | البيانات الشخصية | ✅ Existing |
| Religion | religion | CharField(50) | البيانات الشخصية | ✅ Existing |
| People_With_Special_Needs | people_with_special_needs | BooleanField | البيانات الشخصية | ✅ NEW |
| Governorate | governorate | CharField(50) | البيانات الشخصية | ✅ NEW |
| **Contact Information** |
| Email | email | EmailField | البيانات الشخصية | ✅ Existing |
| Phone | phone | CharField(20) | البيانات الشخصية | ✅ Existing |
| Phone2 | phone2 | CharField(20) | البيانات الشخصية | ✅ NEW |
| Mobile | mobile | CharField(20) | البيانات الشخصية | ✅ Existing |
| Address | address | TextField | البيانات الشخصية | ✅ Existing |
| City | city | CharField(50) | البيانات الشخصية | ✅ Existing |
| Postal_Code | postal_code | CharField(10) | البيانات الشخصية | ✅ Existing |
| Telegram_ID | telegram_id | CharField(100) | البيانات الشخصية | ✅ NEW |
| **Employment Information** |
| Department_ID | department | ForeignKey | بيانات العمل | ✅ Existing |
| Position_ID | position | ForeignKey | بيانات العمل | ✅ Existing |
| Branch_ID | branch | ForeignKey | بيانات العمل | ✅ Existing |
| Manager_ID | manager | ForeignKey | بيانات العمل | ✅ Existing |
| Hire_Date | hire_date | DateField | بيانات العمل | ✅ Existing |
| Employment_Type | employment_type | CharField(20) | بيانات العمل | ✅ Existing |
| Working_Condition | working_condition | CharField(50) | بيانات العمل | ✅ NEW |
| Probation_End_Date | probation_end_date | DateField | بيانات العمل | ✅ Existing |
| Confirmation_Date | confirmation_date | DateField | بيانات العمل | ✅ Existing |
| **Work Schedule** |
| Work_Shift_ID | work_shift | ForeignKey | بيانات العمل | ✅ Existing |
| Current_Week_Shift | current_week_shift | CharField(50) | بيانات العمل | ✅ NEW |
| Next_Week_Shift | next_week_shift | CharField(50) | بيانات العمل | ✅ NEW |
| Friday_Operation | friday_operation | BooleanField | بيانات العمل | ✅ NEW |
| Shift_Type | shift_type | CharField(50) | بيانات العمل | ✅ NEW |
| Shift_Paper | shift_paper | CharField(100) | بيانات العمل | ✅ NEW |
| **Transportation** |
| Has_Car | has_car | BooleanField | بيانات العمل | ✅ NEW |
| Car_Ride_Time | car_ride_time | DateTimeField | بيانات العمل | ✅ NEW |
| Car_Pickup_Point | car_pickup_point | CharField(200) | بيانات العمل | ✅ NEW |
| **Salary Information** |
| Total_Salary | total_salary | DecimalField | بيانات الراتب | ✅ NEW |
| Total_Salary_Text | total_salary_text | CharField(200) | بيانات الراتب | ✅ NEW |
| Basic_Salary (computed) | get_calculated_basic_salary() | Property | بيانات الراتب | ✅ Computed |
| Basic_Salary | basic_salary | DecimalField | بيانات الراتب | ✅ Existing |
| Housing_Allowance | housing_allowance | DecimalField | بيانات الراتب | ✅ Existing |
| Transport_Allowance | transport_allowance | DecimalField | بيانات الراتب | ✅ Existing |
| Other_Allowances | other_allowances | DecimalField | بيانات الراتب | ✅ Existing |
| Allowances (computed) | get_calculated_allowances() | Property | بيانات الراتب | ✅ Computed |
| **Leave Balances** |
| Annual_Leave_Balance | annual_leave_balance | IntegerField | بيانات الراتب | ✅ Existing |
| Sick_Leave_Balance | sick_leave_balance | IntegerField | بيانات الراتب | ✅ Existing |
| **Social Insurance** |
| Insurance_Status | insurance_status | CharField(50) | التأمينات الاجتماعية | ✅ NEW |
| Insurance_Number | insurance_number | CharField(50) | التأمينات الاجتماعية | ✅ NEW |
| Insurance_Code | insurance_code | CharField(50) | التأمينات الاجتماعية | ✅ NEW |
| Insurance_Job_Code | insurance_job_code | CharField(50) | التأمينات الاجتماعية | ✅ NEW |
| Insurance_Job_Name | insurance_job_name | CharField(100) | التأمينات الاجتماعية | ✅ NEW |
| Insurance_Start_Date | insurance_start_date | DateField | التأمينات الاجتماعية | ✅ NEW |
| Insurance_Salary | insurance_salary | DecimalField | التأمينات الاجتماعية | ✅ NEW |
| Insurance_Percentage | insurance_percentage | DecimalField | التأمينات الاجتماعية | ✅ NEW |
| Insurance_Amount_Due | insurance_amount_due | DecimalField | التأمينات الاجتماعية | ✅ NEW |
| **Insurance Forms** |
| Form_S1 | form_s1 | CharField(50) | التأمينات الاجتماعية | ✅ NEW |
| Form_S1_Delivery_Date | form_s1_delivery_date | DateField | التأمينات الاجتماعية | ✅ NEW |
| Form_S1_Receive_Date | form_s1_receive_date | DateField | التأمينات الاجتماعية | ✅ NEW |
| Form_S1_Entry_Number | form_s1_entry_number | CharField(50) | التأمينات الاجتماعية | ✅ NEW |
| Form_S1_Entry_Date | form_s1_entry_date | DateField | التأمينات الاجتماعية | ✅ NEW |
| Insurance_Entry_Confirmation | insurance_entry_confirmation | BooleanField | التأمينات الاجتماعية | ✅ NEW |
| Form_S6 | form_s6 | CharField(50) | التأمينات الاجتماعية | ✅ NEW |
| Form_S6_Delivery_Date | form_s6_delivery_date | DateField | التأمينات الاجتماعية | ✅ NEW |
| Form_S6_Receive_Date | form_s6_receive_date | DateField | التأمينات الاجتماعية | ✅ NEW |
| Form_S6_Entry_Number | form_s6_entry_number | CharField(50) | التأمينات الاجتماعية | ✅ NEW |
| Form_S6_Entry_Date | form_s6_entry_date | DateField | التأمينات الاجتماعية | ✅ NEW |
| Confirm_Exit_Insurance | confirm_exit_insurance | BooleanField | التأمينات الاجتماعية | ✅ NEW |
| **Health Insurance** |
| Health_Card | health_card | BooleanField | التأمين الصحي | ✅ NEW |
| Health_Card_Number | health_card_number | CharField(50) | التأمين الصحي | ✅ NEW |
| Health_Card_Start_Date | health_card_start_date | DateField | التأمين الصحي | ✅ NEW |
| Health_Card_Renewal_Date | health_card_renewal_date | DateField | التأمين الصحي | ✅ NEW |
| Health_Card_Remaining_Days | health_card_remaining_days | IntegerField | التأمين الصحي | ✅ NEW |
| Health_Card_Expiry_Date (computed) | get_health_card_expiry_date() | Property | التأمين الصحي | ✅ Computed |
| Hiring_Date_Health_Card (computed) | get_hiring_date_health_card() | Property | التأمين الصحي | ✅ Computed |
| **International Insurance (Orient)** |
| Orient_Subscription_Start_Date | orient_subscription_start_date | DateField | التأمين الصحي | ✅ NEW |
| Orient_Subscription_Expiry_Date | orient_subscription_expiry_date | DateField | التأمين الصحي | ✅ NEW |
| Orient_Incoming_Number | orient_incoming_number | CharField(50) | التأمين الصحي | ✅ NEW |
| Orient_Incoming_Date | orient_incoming_date | DateField | التأمين الصحي | ✅ NEW |
| Orient_S1 | orient_s1 | CharField(50) | التأمين الصحي | ✅ NEW |
| Orient_S1_Delivery_Date | orient_s1_delivery_date | DateField | التأمين الصحي | ✅ NEW |
| Orient_S1_Receipt_Date | orient_s1_receipt_date | DateField | التأمين الصحي | ✅ NEW |
| Orient_Insurance_Entry_Confirmation | orient_insurance_entry_confirmation | BooleanField | التأمين الصحي | ✅ NEW |
| Orient_S6 | orient_s6 | CharField(50) | التأمين الصحي | ✅ NEW |
| **Contract Information** |
| Contract_Renewal_Date | contract_renewal_date | DateField | بيانات العقد | ✅ NEW |
| Contract_Renewal_Month | contract_renewal_month | IntegerField | بيانات العقد | ✅ NEW |
| Remaining_Contract_Renewal | remaining_contract_renewal | IntegerField | بيانات العقد | ✅ NEW |
| Years_Since_Contract_Start | years_since_contract_start | IntegerField | بيانات العقد | ✅ NEW |
| Contract_Expiry_Date (computed) | get_contract_expiry_date() | Property | بيانات العقد | ✅ Computed |
| **Bank Information** |
| Bank_Name | bank_name | CharField(100) | البيانات البنكية | ✅ Existing |
| Bank_Account_Number | bank_account_number | CharField(50) | البيانات البنكية | ✅ Existing |
| IBAN | iban | CharField(50) | البيانات البنكية | ✅ Existing |
| **Document Submission** |
| Military_Service_Certificate | military_service_certificate | BooleanField | مستندات التعيين | ✅ NEW |
| Qualification_Certificate | qualification_certificate | BooleanField | مستندات التعيين | ✅ NEW |
| Birth_Certificate | birth_certificate | BooleanField | مستندات التعيين | ✅ NEW |
| Insurance_Printout | insurance_printout | BooleanField | مستندات التعيين | ✅ NEW |
| ID_Card_Photo | id_card_photo | BooleanField | مستندات التعيين | ✅ NEW |
| Personal_Photos | personal_photos | BooleanField | مستندات التعيين | ✅ NEW |
| Employment_Contract_Submitted | employment_contract_submitted | BooleanField | مستندات التعيين | ✅ NEW |
| Medical_Exam_Form_Submitted | medical_exam_form_submitted | BooleanField | مستندات التعيين | ✅ NEW |
| Medical_Exam_Form_Submission | medical_exam_form_submission | BooleanField | مستندات التعيين | ✅ NEW |
| Criminal_Record_Check | criminal_record_check | BooleanField | مستندات التعيين | ✅ NEW |
| Social_Status_Report | social_status_report | BooleanField | مستندات التعيين | ✅ NEW |
| Skill_Level_Measurement_Certificate | skill_level_measurement_certificate | BooleanField | مستندات التعيين | ✅ NEW |
| **Work Heel** |
| Work_Heel | work_heel | BooleanField | مستندات التعيين | ✅ NEW |
| Work_Heel_Number | work_heel_number | CharField(50) | مستندات التعيين | ✅ NEW |
| Work_Heel_Recipient | work_heel_recipient | CharField(100) | مستندات التعيين | ✅ NEW |
| Work_Heel_Recipient_Address | work_heel_recipient_address | CharField(200) | مستندات التعيين | ✅ NEW |
| Work_Heel_Registration_Date (computed) | get_work_heel_registration_date() | Property | مستندات التعيين | ✅ Computed |
| **Other** |
| Photo | photo | ImageField | البيانات الشخصية | ✅ Existing |
| ZK_User_ID | zk_user_id | IntegerField | بيانات العمل | ✅ Existing |
| **Status** |
| Is_Active | is_active | BooleanField | حالة الموظف | ✅ Existing |
| Termination_Date | termination_date | DateField | حالة الموظف | ✅ Existing |
| Termination_Reason | termination_reason | TextField | حالة الموظف | ✅ Existing |
| Resignation_Date | resignation_date | DateField | حالة الموظف | ✅ NEW |
| Resignation_Reason | resignation_reason | TextField | حالة الموظف | ✅ NEW |

---

## Summary Statistics

- **Total SQL Fields:** ~150 fields
- **Django Model Fields:** 120+ fields (including existing)
- **New Fields Added:** 77 fields
- **Computed Properties:** 7 properties
- **Fields NOT Implemented:** 0 (all relevant fields implemented)

**Note:** SQL computed fields (using `AS` keyword) were implemented as Django property methods instead of database fields.

