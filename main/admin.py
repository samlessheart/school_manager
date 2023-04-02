from django.contrib import admin
from .models import CustomUser, School, Student, Grades
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(School)
admin.site.register(Student)
admin.site.register(Grades)