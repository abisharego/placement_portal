from django import forms
from .models import Job, Student
from django.db import models

class JobSearchForm(forms.Form):
    query = forms.CharField(required=False)
    job_type = forms.ChoiceField(choices=[('full-time', 'Full-Time'), ('part-time', 'Part-Time'), ('internship', 'Internship')], required=False)
    location = forms.CharField(required=False)
    min_salary = forms.DecimalField(required=False)
    max_salary = forms.DecimalField(required=False)

class ResumeForm(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
