# recommendations/views.py
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from recommendations.ollama_utils import extract_skills_from_profile,match_live_jobs
from users.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
import requests
from resume_builder.models import resume
from .utils import generate_learning_roadmap , extract_skills_from_profile,fetch_jobs



@login_required
def extract_skills_view(request):
    try:
        user_profile = request.user.userprofile  # Or UserProfile.objects.get(user=request.user)
        
        if request.method == "POST":
            profile_data = f"""
Name: {request.user.get_full_name()}
Education: {user_profile.education}
Experience: {user_profile.experience}
Skills: {user_profile.skills}
Projects: {user_profile.projects}
Achievements: {user_profile.achievements}
"""
            skills = extract_skills_from_profile(profile_data)
            user_profile.extracted_skills = skills
            user_profile.save()
            
            return render(request, "recommendations/extracted_skills.html", {
                "skills": skills
            })

        return render(request, "recommendations/extract_skills.html", {
            "profile": user_profile
        })

    except ObjectDoesNotExist:
        # Redirect to profile creation or show error
        return render(request, "base.html"
        , status=404)
        
        
@login_required
def live_job_match_view(request):
    profile = UserProfile.objects.get(user=request.user)
    skills = profile.extracted_skills or []

    if not skills:
        return render(request, "recommendations/job_match.html", {
            "error": "Please extract your skills first."
        })

    # Use top skills as query (or a fixed job title from user input)
    query = "+".join(skills[:3])  # limit query length
    api_url = f"https://remotive.io/api/remote-jobs?search={query}"

    try:
        res = requests.get(api_url)
        data = res.json()
        jobs = data.get("jobs", [])[:10]  # limit to 10 for now
    except:
        jobs = []

    job_data = [{"title": j["title"], "description": j["description"]} for j in jobs]
    matches = match_live_jobs(skills, job_data)

    matched_jobs = []
    for match in matches:
        index = match.get("index", 0) - 1
        if 0 <= index < len(job_data):
            job = jobs[index]
            matched_jobs.append({
                "title": job["title"],
                "description": job["description"],
                "url": job["url"],
                "reason": match.get("reason")
            })

    return render(request, "recommendations/job-match.html", {
        "matched_jobs": matched_jobs
    })
    
import json
import google.generativeai as genai
def parse_roadmap_with_gemini(roadmap_text: str):
    """
    Uses Gemini to parse a freeform roadmap into structured JSON steps with a 'completed' field.
    
    Parameters:
    - roadmap_text (str): The input roadmap content (plain text or markdown)

    Returns:
    - list[dict]: Parsed steps, e.g., [{ "step": "Learn HTML", "completed": false }]
    """

    # ✅ Gemini API key configuration (same as other function)
    genai.configure(api_key="AIzaSyA-5bYusWS0-K9hDU5bxk7NDX1AX2gAuOI")

    model = genai.GenerativeModel("gemini-2.5-flash")

    # Prompt to extract checklist-style JSON from the roadmap
    prompt = f"""
You are a helpful assistant.

Take the following roadmap text and convert it into structured JSON. Each step should be a short sentence or phrase with a `step` and a `completed` flag (default to false).

Roadmap:
\"\"\"
{roadmap_text}
\"\"\"

Output format:
[
  {{
    "step": "First task",
    "completed": false
  }},
  {{
    "step": "Second task",
    "completed": false
  }}
]

Only return valid JSON. No commentary. No markdown or code fences. Just the JSON array.
"""

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Try to parse as JSON
        steps = json.loads(raw_text)
        return steps

    except Exception as e:
        # Fallback with error handling
        return [{"step": f"Error parsing roadmap: {str(e)}", "completed": False}]
    
@login_required
def create_roadmap(request,pk):
    latest_resume = resume.objects.filter(user=request.user).order_by('-created_at').first()
    
    skills = latest_resume.skills
    projects = latest_resume.projects
    experience = latest_resume.experience
    
    response = generate_learning_roadmap(skills , projects, experience, pk)
    steps = parse_roadmap_with_gemini(response)
    
    
    
    context = {
        'steps' : steps,
        'response':response
    }
    
    return render(request, 'recommendations/roadmap.html', context)


@login_required
def target_job_view(request):
    
    return render(request, 'recommendations/targetjob.html')
    
import json

import http.client
import json

    
@login_required
def job_recommendation_view(request):
    myprofile = UserProfile.objects.get(user=request.user)
    skills = myprofile.skills
    experience = myprofile.experience
    projects = myprofile.projects
    location = myprofile.location
    
    keywords = extract_skills_from_profile(location , skills , experience, projects)
    
    jobs = fetch_jobs(keywords, location)
    
    return render(request, 'recommendations/topjobs.html', {'jobs': jobs})
    




    
    
    