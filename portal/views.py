from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Student, Recruiter
from .models import Student, Job, Application
from .forms import JobSearchForm, ResumeForm
from django.core.mail import send_mail
import pandas as pd # type: ignore
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

def login_view(request):
    if request.method == "POST":
        user_type = request.POST.get('user_type')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user_type == 'Student':
            try:
                student = Student.objects.get(university_number=email)
                user = authenticate(request, username=student.university_number, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('student_dashboard')
                else:
                    # Handle invalid login for student
                    return render(request, 'login.html', {'error': 'Invalid login credentials'})
            except Student.DoesNotExist:
                return render(request, 'login.html', {'error': 'Student not found'})

        elif user_type == 'recruiter':
            try:
                recruiter = Recruiter.objects.get(email=email)
                user = authenticate(request, username=recruiter.email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('recruiter_dashboard')
                else:
                    # Handle invalid login for recruiter
                    return render(request, 'login.html', {'error': 'Invalid login credentials'})
            except Recruiter.DoesNotExist:
                return render(request, 'login.html', {'error': 'Recruiter not found'})
        else:
            return render(request, 'login.html', {'error': 'Invalid user type'})

    return render(request, 'login.html')




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_recruiter(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the user is a recruiter (you can use a user group or a custom field)
            if user.is_staff:  # Assuming recruiters are staff users
                login(request, user)
                return redirect('recruiter_dashboard')  # Redirect to a recruiter dashboard
            else:
                messages.error(request, "You do not have permission to access this page.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login_recruiter.html')

def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the user is an admin
            if user.is_superuser:  # Assuming admins are superusers
                login(request, user)
                return redirect('admin_dashboard')  # Redirect to an admin dashboard
            else:
                messages.error(request, "You do not have permission to access this page.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login_admin.html')

def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the user is a student (you can use a user group or a custom field)
            if not user.is_staff and not user.is_superuser:  # Assuming students are neither staff nor superusers
                login(request, user)
                return redirect('student_dashboard')  # Redirect to a student dashboard
            else:
                messages.error(request, "You do not have permission to access this page.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login_student.html')





def register_view(request):
    if request.method == "POST":
        username = request.POST("username")
        password = request.POST("password")
        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)  # Log in the user after registration
            return redirect('dashboard')  # Redirect to a success page
        except Exception as e:
            return render(request, 'register.html', {'error': str(e)})
    return render(request, 'register.html')

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
            ['admin@example.com'],
            fail_silently=False,
        )
        return redirect('recruiter_dashboard.html')
    


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Student

def register_student(request):
    if request.method == "POST":
        university_number = request.POST['university_number']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        
        # Create a User object (Django's built-in User model)
        user = User.objects.create_user(username=university_number, password=password)
        
        # Create a Student object and associate it with the User
        student = Student.objects.create(
            university_number=university_number,
            name=name,
            email=email,
            password=password
        )
        
        # Optionally log the student in automatically after registration
        login(request, user)
        
        return redirect('student_dashboard')
    
    return render(request, 'register_student.html')

@login_required
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


def job_search(request):
    form = JobSearchForm(request.GET or None)
    jobs = Job.objects.all()

    if form.is_valid():
        if form.cleaned_data['query']:
            jobs = jobs.filter(Q(title__icontains=form.cleaned_data['query']) | Q(recruiter__company_name__icontains=form.cleaned_data['query']))
        if form.cleaned_data['job_type']:
            jobs = jobs.filter(job_type=form.cleaned_data['job_type'])
        if form.cleaned_data['location']:
            jobs = jobs.filter(location__icontains=form.cleaned_data['location'])
        if form.cleaned_data['min_salary']:
            jobs = jobs.filter(salary__gte=form.cleaned_data['min_salary'])
        if form.cleaned_data['max_salary']:
            jobs = jobs.filter(salary__lte=form.cleaned_data['max_salary'])

    return render(request, 'job_search.html', {'form': form, 'jobs': jobs})


@login_required
@permission_required('portal.can_view_student_dashboard')
def student_dashboard(request):
    student = Student.objects.get(university_number=request.user.username)
    jobs = Job.objects.all()  # Fetch all jobs posted by recruiters
    applications = Application.objects.filter(student=student)  # Fetch applications made by the student
    return render(request, 'student_dashboard.html', {'student': student, 'jobs': jobs, 'applications': applications})

def apply_for_job(request, job_id):
    if request.method == "POST":
        student = Student.objects.get(university_number=request.user.username)
        job = Job.objects.get(id=job_id)
        Application.objects.create(student=student, job=job)
        return redirect('student_dashboard.html')
    
@login_required
def recruiter_dashboard(request):
    try:
        recruiter = Recruiter.objects.get(user=request.user)  # Get the recruiter profile
    except Recruiter.DoesNotExist:
        return redirect('recruiter_error')
    jobs = Job.objects.filter(recruiter=recruiter)  # Fetch jobs posted by the recruiter
    return render(request, 'recruiter_dashboard.html', {'jobs': jobs})

def recruiter_error(request):
    return render(request, 'recruiter_error.html')

def edit_student_profile(request):
    student = request.user.student  # Assuming a OneToOne relationship
    if request.method == "POST":
        student.name = request.POST['name']
        student.university_number = request.POST['university_number']
        student.save()
        return redirect('student_dashboard')
    
    return render(request, 'edit_student_profile.html', {'student': student})


def job_search(request):
    query = request.GET.get('q')
    jobs = Job.objects.filter(Q(title__icontains=query) | Q(recruiter__company_name__icontains=query)) if query else Job.objects.all()
    return render(request, 'job_search.html', {'jobs': jobs})


def update_application_status(request, application_id):
    application = Application.objects.get(id=application_id)
    if request.method == "POST":
        application.status = request.POST['status']
        application.save()
        return redirect('admin_dashboard')  # Redirect to admin dashboard or wherever appropriate
    return render(request, 'update_application_status.html', {'application': application})

def application_history(request):
    applications = Application.objects.filter(student=request.user.student)
    return render(request, 'application_history.html', {'applications': applications})

@login_required
def upload_resume(request):
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.student = request.user.student
            resume.save()
            return redirect('student_dashboard')
    else:
        form = ResumeForm()
    return render(request, 'upload_resume.html', {'form': form})

@receiver(post_save, sender=Job)
def notify_students(sender, instance, created, **kwargs):
    if created:
        students = Student.objects.all()
        for student in students:
            send_mail(
                'New Job Posted',
                f'A new job titled "{instance.title}" has been posted. Check it out!',
                'from@example.com',  # Replace with your email
                [student.user.email],
                fail_silently=False,
            )



def job_list(request):
    job_list = Job.objects.all()
    paginator = Paginator(job_list, 10)  # Show 10 jobs per page
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)
    return render(request, 'job_list.html', {'jobs': jobs})

def job_list(request):
    jobs = Job.objects.select_related('recruiter').all()
    return render(request, 'job_list.html', {'jobs': jobs})


@cache_page(60 * 15)  # Cache for 15 minutes
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})


from rest_framework import viewsets
from .models import Job
from .serializers import JobSerializer
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

from django.utils.translation import gettext as _
from django.utils import translation
def my_view(request):
    user_language = 'en'  # Or use request.LANGUAGE_CODE
    translation.activate(user_language)
    message = _("Welcome to the Job Portal")
    return render(request, 'my_template.html', {'message': message})

import logging

logger = logging.getLogger(__name__)

def my_view(request):
    try:
        # Log when the view is accessed
        logger.info("My view was accessed")

        # Example of business logic: retrieving data from a model
        jobs = Job.objects.all()  # Fetching all jobs (adjust this query as needed)
        logger.debug(f"Retrieved {jobs.count()} jobs")

        # Example of a warning log
        if jobs.count() == 0:
            logger.warning("No jobs found in the database")

        # Pass data to the template
        return render(request, 'my_template.html', {'jobs': jobs})

    except Exception as e:
        # Log the error with traceback if an exception occurs
        logger.error(f"Error occurred: {e}", exc_info=True)
        # Return a generic error response (you can customize this)
        return render(request, 'error_template.html', {'error': 'Something went wrong!'})


from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True  # Redirect if already logged in
    next_page = 'home'  # Or use a URL pattern name
