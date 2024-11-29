from django.db import models

class Student(models.Model):
    university_number = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

class Recruiter(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)

class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name