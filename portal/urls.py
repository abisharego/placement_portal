from django.urls import path
from .views import admin_dashboard, export_applications_to_excel, student_dashboard, apply_for_job, recruiter_dashboard, login_view, post_job

urlpatterns = [
    path('login/', login_view, name='login'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/export_applications/<int:job_id>/', export_applications_to_excel, name='export_applications'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('student/apply/<int:job_id>/', apply_for_job, name='apply_for_job'),
    path('recruiter/dashboard/', recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter/post_job/', post_job, name='post_job'),
]