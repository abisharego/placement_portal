from django import forms
from .models import Job, Student
from django.db import models
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

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
