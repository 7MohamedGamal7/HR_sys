"""
Automated Template Generator for HR Management System
مولد القوالب التلقائي لنظام إدارة الموارد البشرية

This script generates all remaining templates following Django best practices
"""
import os

# Define template patterns
def get_list_template(app_name, model_name, model_name_ar, fields):
    """Generate a list template"""
    return f"""{{%extends 'base.html' %}}

{{%block title %}}{model_name_ar}{{%endblock %}}

{{%block content %}}
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2><i class="fas fa-list ms-2"></i>{model_name_ar}</h2>
                <a href="{{{{url '{app_name}:{model_name}_create' }}}}" class="btn btn-primary">
                    <i class="fas fa-plus ms-2"></i>إضافة جديد
                </a>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    {' '.join([f'<th>{field}</th>' for field in fields])}
                                    <th>الإجراءات</th>
                                </tr>
                            </thead>
                            <tbody>
                                {{{{for item in page_obj %}}}}
                                    <tr>
                                        <!-- Add table cells here -->
                                        <td>
                                            <a href="{{{{url '{app_name}:{model_name}_detail' item.pk }}}}" class="btn btn-sm btn-info">
                                                <i class="fas fa-eye"></i>
                                            </a>
                                            <a href="{{{{url '{app_name}:{model_name}_update' item.pk }}}}" class="btn btn-sm btn-warning">
                                                <i class="fas fa-edit"></i>
                                            </a>
                                        </td>
                                    </tr>
                                {{{{empty %}}}}
                                    <tr><td colspan="{len(fields) + 1}" class="text-center">لا توجد بيانات</td></tr>
                                {{{{endfor %}}}}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{{%endblock %}}
"""


def get_form_template(app_name, model_name, model_name_ar):
    """Generate a form template"""
    return f"""{{%extends 'base.html' %}}
{{%load crispy_forms_tags %}}

{{%block title %}}{{{{if {model_name} %}}}}تعديل{{{{else %}}}}إضافة{{{{endif %}}}} {model_name_ar}{{%endblock %}}

{{%block content %}}
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>{{{{if {model_name} %}}}}تعديل{{{{else %}}}}إضافة{{{{endif %}}}} {model_name_ar}</h2>
                <a href="{{{{url '{app_name}:{model_name}_list' }}}}" class="btn btn-secondary">
                    <i class="fas fa-arrow-right ms-2"></i>العودة
                </a>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-body">
                    <form method="post" enctype="multipart/form-data">
                        {{{{csrf_token %}}}}
                        {{{{form|crispy %}}}}
                        <div class="text-end">
                            <a href="{{{{url '{app_name}:{model_name}_list' }}}}" class="btn btn-secondary">
                                <i class="fas fa-times ms-2"></i>إلغاء
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save ms-2"></i>حفظ
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{{%endblock %}}
"""


# Template configurations for each app
TEMPLATES_TO_CREATE = {
    "attendance": [
        ("attendance_list.html", "list", "سجلات الحضور", ["التاريخ", "الموظف", "وقت الدخول", "وقت الخروج", "الحالة"]),
        ("attendance_form.html", "form", "سجل حضور", None),
        ("leave_request_list.html", "list", "طلبات الإجازات", ["الموظف", "نوع الإجازة", "من", "إلى", "الحالة"]),
        ("leave_request_form.html", "form", "طلب إجازة", None),
        ("overtime_list.html", "list", "سجلات الإضافي", ["الموظف", "التاريخ", "الساعات", "الحالة"]),
        ("overtime_form.html", "form", "سجل إضافي", None),
    ],
    "organization": [
        ("department_list.html", "list", "الأقسام", ["الاسم", "القسم الرئيسي", "المدير"]),
        ("department_form.html", "form", "قسم", None),
        ("position_list.html", "list", "المناصب", ["المسمى", "القسم", "المستوى"]),
        ("position_form.html", "form", "منصب", None),
        ("branch_list.html", "list", "الفروع", ["الاسم", "المدينة", "العنوان"]),
        ("branch_form.html", "form", "فرع", None),
        ("shift_list.html", "list", "الورديات", ["الاسم", "وقت البداية", "وقت النهاية"]),
        ("shift_form.html", "form", "وردية", None),
        ("holiday_list.html", "list", "العطلات", ["الاسم", "التاريخ", "النوع"]),
        ("holiday_form.html", "form", "عطلة", None),
    ],
    "payroll": [
        ("payroll_list.html", "list", "كشوف الرواتب", ["الشهر", "السنة", "الحالة"]),
        ("payroll_form.html", "form", "كشف رواتب", None),
        ("payslip_list.html", "list", "قسائم الرواتب", ["الموظف", "الشهر", "الراتب الصافي"]),
        ("payslip_detail.html", "detail", "قسيمة راتب", None),
        ("loan_list.html", "list", "القروض", ["الموظف", "المبلغ", "تاريخ البداية", "الحالة"]),
        ("loan_form.html", "form", "قرض", None),
        ("bonus_list.html", "list", "المكافآت", ["الموظف", "المبلغ", "التاريخ", "السبب"]),
        ("bonus_form.html", "form", "مكافأة", None),
    ],
    "performance": [
        ("review_list.html", "list", "تقييمات الأداء", ["الموظف", "المقيّم", "الفترة", "التقييم"]),
        ("review_form.html", "form", "تقييم أداء", None),
        ("kpi_list.html", "list", "مؤشرات الأداء", ["الاسم", "الوصف", "الوحدة"]),
        ("kpi_form.html", "form", "مؤشر أداء", None),
        ("goal_list.html", "list", "الأهداف", ["الموظف", "الهدف", "الموعد النهائي", "الحالة"]),
        ("goal_form.html", "form", "هدف", None),
    ],
    "recruitment": [
        ("job_list.html", "list", "الوظائف المعلنة", ["المسمى", "القسم", "تاريخ النشر", "الحالة"]),
        ("job_form.html", "form", "وظيفة", None),
        ("application_list.html", "list", "طلبات التوظيف", ["المتقدم", "الوظيفة", "التاريخ", "الحالة"]),
        ("application_form.html", "form", "طلب توظيف", None),
        ("interview_list.html", "list", "المقابلات", ["المتقدم", "التاريخ", "المقابل", "الحالة"]),
        ("interview_form.html", "form", "مقابلة", None),
        ("offer_list.html", "list", "عروض العمل", ["المتقدم", "المنصب", "الراتب", "الحالة"]),
        ("offer_form.html", "form", "عرض عمل", None),
    ],
    "training": [
        ("program_list.html", "list", "البرامج التدريبية", ["الاسم", "الفئة", "المدة"]),
        ("program_form.html", "form", "برنامج تدريبي", None),
        ("session_list.html", "list", "الجلسات التدريبية", ["البرنامج", "المدرب", "التاريخ", "الحالة"]),
        ("session_form.html", "form", "جلسة تدريبية", None),
        ("enrollment_list.html", "list", "التسجيلات التدريبية", ["الموظف", "الجلسة", "تاريخ التسجيل"]),
        ("enrollment_form.html", "form", "تسجيل تدريبي", None),
    ],
    "leaves": [
        ("leave_policy_list.html", "list", "سياسات الإجازات", ["الاسم", "الأيام السنوية", "قابل للترحيل"]),
        ("leave_policy_form.html", "form", "سياسة إجازة", None),
        ("leave_balance_list.html", "list", "أرصدة الإجازات", ["الموظف", "السياسة", "الرصيد المتاح"]),
        ("leave_balance_form.html", "form", "رصيد إجازة", None),
    ],
    "reports": [
        ("reports_dashboard.html", "dashboard", "لوحة التقارير", None),
        ("employee_summary_report.html", "report", "تقرير ملخص الموظفين", None),
        ("attendance_summary_report.html", "report", "تقرير ملخص الحضور", None),
        ("leave_summary_report.html", "report", "تقرير ملخص الإجازات", None),
        ("payroll_summary_report.html", "report", "تقرير ملخص الرواتب", None),
    ],
}


def create_template_file(app_name, filename, template_type, title_ar, fields=None):
    """Create a template file"""
    template_dir = os.path.join("templates", app_name)
    os.makedirs(template_dir, exist_ok=True)
    
    filepath = os.path.join(template_dir, filename)
    
    # Skip if already exists
    if os.path.exists(filepath):
        print(f"⏭️  Skipped (exists): {filepath}")
        return
    
    # Generate content based on type
    if template_type == "list":
        model_name = filename.replace("_list.html", "")
        content = get_list_template(app_name, model_name, title_ar, fields or [])
    elif template_type == "form":
        model_name = filename.replace("_form.html", "")
        content = get_form_template(app_name, model_name, title_ar)
    else:
        # For detail, dashboard, report templates - create basic structure
        content = f"""{{%extends 'base.html' %}}

{{%block title %}}{title_ar}{{%endblock %}}

{{%block content %}}
<div class="container-fluid">
    <h2>{title_ar}</h2>
    <!-- Add content here -->
</div>
{{%endblock %}}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {filepath}")


def main():
    """Main function"""
    print("🚀 Starting automated template generation...")
    print("=" * 70)
    
    total_created = 0
    
    for app_name, templates in TEMPLATES_TO_CREATE.items():
        print(f"\n📁 Creating templates for {app_name}...")
        for template_config in templates:
            filename, template_type, title_ar = template_config[:3]
            fields = template_config[3] if len(template_config) > 3 else None
            create_template_file(app_name, filename, template_type, title_ar, fields)
            total_created += 1
    
    print("\n" + "=" * 70)
    print(f"✅ Template generation completed! Created {total_created} templates.")
    print("\n📝 Note: Some templates may need manual customization for specific features.")


if __name__ == "__main__":
    main()

