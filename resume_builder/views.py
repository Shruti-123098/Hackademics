from django.shortcuts import render, redirect
from users.models import UserProfile
from django.contrib.auth.decorators import login_required
from .utils import enhance_with_ollama

@login_required
def generate_resume(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('edit_profile')

    template_choice = profile.resume_template_choice or 1
    template_name = f'resume_templates/template{template_choice}.html'

    # Enhance summary (optional)
    enhanced_projects = enhance_with_ollama(
        f"{profile.projects}"
    )
    enhanced_achievements = enhance_with_ollama(
        f"Rewrite the following achievements in a concise and impactful way:\n{profile.achievements}"
    )

    context = {
        'full_name': profile.full_name,
        'phone_number': profile.phone_number,
        'email': request.user.email,
        'location': profile.location,
        'skills': profile.skills,
        'education': profile.education,
        'experience': profile.experience,
        'projects': enhanced_projects,
        'achievements': enhanced_achievements or profile.achievements,
    }

    return render(request, template_name, context)

from django.http import HttpResponse
from django.template.loader import get_template
# from weasyprint import HTML

# @login_required
# def download_resume_pdf(request):
#     try:
#         profile = request.user.userprofile
#     except UserProfile.DoesNotExist:
#         return redirect('edit_profile')

#     template_choice = profile.resume_template_choice or 1
#     template_path = f'resume_templates/template{template_choice}.html'

#     enhanced_projects = enhance_with_ollama(
#         f"{profile.projects}"
#     )
#     enhanced_achievements = enhance_with_ollama(
#         f"{profile.achievements}"
#     )

#     context = {
#         'full_name': profile.full_name,
#         'phone_number': profile.phone_number,
#         'email': request.user.email,
#         'location': profile.location,
#         'skills': profile.skills,
#         'education': profile.education,
#         'experience': profile.experience,
#         'projects': enhanced_projects or profile.projects,
#         'achievements': enhanced_achievements or profile.achievements,
#     }

#     html_template = get_template(template_path)
#     html_content = html_template.render(context)
#     pdf_file = HTML(string=html_content).write_pdf()

#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
#     return response

