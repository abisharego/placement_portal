from django.contrib import admin
from .models import Student, Job

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')  
    search_fields = ('name',)  

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'posted_date', 'salary')
    search_fields = ('title', 'company')
    list_filter = ('job_type',)
