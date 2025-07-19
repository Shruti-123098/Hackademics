from django.db import models
from users.models import User
from django.utils import timezone

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
    goal_id = models.IntegerField()  # Using the pk parameter from your view
    content = models.TextField()
    steps = models.JSONField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'goal_id')  # One path per user per goal

    def __str__(self):
        return f"{self.user.username}'s Learning Path #{self.goal_id}"

class roadmap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
class Roadmap1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roadmaps')
    title = models.CharField(max_length=255, default='Untitled Roadmap')
    raw_response = models.TextField(help_text="Full Gemini-generated roadmap text")
    steps = models.JSONField(help_text="List of steps with completion status")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.title}"