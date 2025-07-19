from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_resume, name='generate_resume'),
    # path('download/', views.download_resume_pdf, name='download_resume'),
    path('download/', views.download_resume_docx, name='download_resume'),
    path('view-resume/', views.view_resume, name='view'),
    path('resume-details/<int:pk>/', views.resume_details, name='view-resume'),
    path('delete-resume/<int:pk>/', views.delete_resume, name='delete_resume'),

]
