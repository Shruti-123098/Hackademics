from django.urls import path
from .views import *
urlpatterns = [
     path('extract-skills/', extract_skills_view, name='extract_skills'),
     path('match-live-jobs/', live_job_match_view, name='match_live_jobs'),
     path('roadmap/<str:pk>/' ,create_roadmap, name='create_roadmap'),
     path('targetjob/', target_job_view, name='target_job'),
     path('job-recommendation/', job_recommendation_view, name='job_recommendation'),
]
