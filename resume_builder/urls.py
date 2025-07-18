from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_resume, name='generate_resume'),
    # path('download/', views.download_resume_pdf, name='download_resume'),

]
