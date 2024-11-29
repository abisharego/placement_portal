from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Student, Recruiter, Job, Application
from django.core.mail import send_mail
import pandas as pd # type: ignore
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        if 'university_number' in request.POST:
            university_number = request.POST['university_number']
            password = request.POST['password']
            user = authenticate(request, username=university_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')
        else:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('recruiter_dashboard')
    return render(request, 'login.html')



def post_job(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        recruiter = request.user
        job = Job.objects.create(title=title, description=description, recruiter=recruiter)
        
        # Send email notification to admin
        send_mail(
            'New Job Posted',
            f'A new job has been posted: {title}',
            'from@example.com',
            ['abisharego18@gmail.com'],
            fail_silently=False,
        )
        return redirect('recruiter_dashboard')
    


def admin_dashboard(request):
    students = Student.objects.all()
    jobs = Job.objects.all()
    applications = Application.objects.all()
    return render(request, 'admin_dashboard.html', {'students': students, 'jobs': jobs, 'applications': applications})

def export_applications_to_excel(request, job_id):
    applications = Application.objects.filter(job_id=job_id)
    data = {
        'Student Name': [app.student.name for app in applications],
        'University Number': [app.student.university_number for app in applications],
        'Applied Date': [app.applied_date for app in applications],
    }
    df = pd.DataFrame(data)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="applications.xlsx"'
    
    df.to_excel(response, index=False)
    return response



def post_job_view(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        recruiter = request.user
        Job.objects.create(title=title, description=description, recruiter=recruiter)
        # Notify admin via email (as shown previously)
        return redirect('recruiter_dashboard')
    return render(request, 'post_job.html')



@login_required
def student_dashboard(request):
    # Assuming the user is a Student
    student = Student.objects.get(university_number=request.user.username)
    jobs = Job.objects.all()  # Fetch all jobs posted by recruiters
    applications = Application.objects.filter(student=student)  # Fetch applications made by the student
    return render(request, 'student_dashboard.html', {'student': student, 'jobs': jobs, 'applications': applications})

def apply_for_job(request, job_id):
    if request.method == "POST":
        student = Student.objects.get(university_number=request.user.username)
        job = Job.objects.get(id=job_id)
        Application.objects.create(student=student, job=job)
        return redirect('student_dashboard')
    


@login_required
def recruiter_dashboard(request):
    recruiter = request.user
    jobs = Job.objects.filter(recruiter=recruiter)  # Fetch jobs posted by the recruiter
    return render(request, 'recruiter_dashboard.html', {'jobs': jobs})