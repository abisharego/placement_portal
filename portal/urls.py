from django.urls import path, include
from .views import admin_dashboard, export_applications_to_excel, student_dashboard, apply_for_job, recruiter_dashboard, login_view, post_job, register_view, recruiter_error, my_view, register_student, login_student, login_admin, login_recruiter
from rest_framework.routers import DefaultRouter
from .views import JobViewSet
from django.views.generic import RedirectView

router = DefaultRouter()
router.register(r'portal', JobViewSet)  # Register the JobViewSet

urlpatterns = [
    path('login/', login_student, name='login'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/export_applications/<int:job_id>/', export_applications_to_excel, name='export_applications'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('student/apply/<int:job_id>/', apply_for_job, name='apply_for_job'),
    path('recruiter/dashboard/', recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter/post_job/', post_job, name='post_job'),
    path('register/student/', register_student, name='register'),
    path('api/', include(router.urls)), 
    path('error/', recruiter_error, name='recruiter_error'),
    path('jobs/', my_view, name='my_view'),
    path('register/student/', register_student, name='register_student'),
    
    






    path('login/recruiter/', login_recruiter, name='login_recruiter'),
    path('login/admin/', login_admin, name='login_admin'),
    path('login/student/', login_student, name='login_student'),
]