from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    university_number = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    class Meta:
        permissions = [
            ("can_view_student_dashboard", "Can view student dashboard"),
        ]

class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    class Meta:
        permissions = [
            ("can_view_recruiter_dashboard", "Can view recruiter dashboard"),
        ]

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=50, default='Full-time')
    recruiter_company_name = models.CharField(max_length=100, default='Unknown Company')

class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'posted_date', 'salary')
    search_fields = ('title', 'recruiter_company_name')
    list_filter = ('job_type',)


class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



admin.site.register(Application)

admin.site.register(Recruiter)
admin.site.register(Feedback)