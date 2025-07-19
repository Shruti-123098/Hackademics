import google.generativeai as genai

def generate_learning_roadmap(skills, projects, experience, target_job):
    """
    Uses Gemini to identify lacking skills and generate a learning roadmap based on user's input.
    Give bullet points 
    
    Parameters:
    - skills (list[str]): List of current skills
    - projects (list[str] or str): Summary of projects done
    - experience (str): Work or internship experience
    - target_job (str): Target job role, e.g. "Machine Learning Engineer"

    Returns:
    - str: Gemini-generated roadmap and missing skills
    """

    # ✅ Hardcoded Gemini API Key
    genai.configure(api_key="AIzaSyA-5bYusWS0-K9hDU5bxk7NDX1AX2gAuOI")

    # Format the input into a clean prompt
    prompt = f"""
You are a career mentor. Based on the following user profile, identify the skills they are lacking to become a successful {target_job}.
Then, generate a detailed, step-by-step learning roadmap for the next 3–4 months.
Give the roadmap in bullet points without using asteriks or hashes.
you can underline the headings for better readability.
Also provide any sources like documentation, courses, or articles that can help the user learn these skills.

Current Skills:
{', '.join(skills)}

Projects:
{projects if isinstance(projects, str) else '.'.join(projects)}

Experience:
{experience}

Output Format:
1. Lacking Skills: (List format)
2. Roadmap: (Detailed weekly or monthly roadmap)

Be realistic, practical, and focused on relevant technologies and goals. Avoid suggesting skills the user already has.
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    return response.text


import google.generativeai as genai
import http.client
import json

GOOGLE_API_KEY = "AIzaSyA-5bYusWS0-K9hDU5bxk7NDX1AX2gAuOI"
genai.configure(api_key=GOOGLE_API_KEY)

def extract_skills_from_profile(location, skills, experience, projects):
    try:
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        Based on the user's professional information, extract a clean and concise list of technical and relevant soft skills only. Avoid repetitions.

        Location: {location}
        Skills mentioned: {skills}
        Experience: {experience}
        Projects: {projects}

        Respond with only a comma-separated list of skills.
        """

        response = model.generate_content(prompt)
        extracted_skills = response.text.strip()

        # Optional: Clean up whitespace and return as list
        return [skill.strip() for skill in extracted_skills.split(',') if skill.strip()]

    except Exception as e:
        return [f"Error: {str(e)}"]


def fetch_jobs(keywords, location):
    import http.client
    import json

    host = 'jooble.org'
    key = '1d0939bd-d781-471a-85c9-4a75cb8b1882'
    connection = http.client.HTTPSConnection(host)
    headers = {"Content-type": "application/json"}

    body = json.dumps({
        "keywords": ', '.join(keywords),  # Ensure string
        "location": 'India'
    })

    connection.request('POST', f'/api/{key}', body, headers)
    response = connection.getresponse()
    print("Status:", response.status, response.reason)

    data = response.read().decode()
    print("Raw Response:", data)  # For debugging

    if not data:
        print("Empty response from Jooble API.")
        return []

    try:
        parsed_data = json.loads(data)
        return parsed_data.get("jobs", [])
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return []
