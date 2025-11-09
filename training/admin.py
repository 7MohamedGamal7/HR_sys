from django.contrib import admin
from .models import (
    TrainingProgram, TrainingEnrollment, TrainingCertificate,
    SkillCategory, Skill, EmployeeSkill
)

admin.site.register(TrainingProgram)
admin.site.register(TrainingEnrollment)
admin.site.register(TrainingCertificate)
admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(EmployeeSkill)

