from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    skills = models.TextField(help_text="Comma-separated skills")
    education = models.TextField()
    experience = models.TextField()
    projects = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    resume_template_choice = models.IntegerField(default=1)

    def __str__(self):
        return self.full_name
