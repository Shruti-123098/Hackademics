from django.db import models
from users.models import User

class JobRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    url = models.URLField()
    match_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class LearningPath(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_job = models.CharField(max_length=100)
    recommended_courses = models.TextField()
    estimated_duration_weeks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
