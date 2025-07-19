import ollama
from google import genai
client = genai.Client(api_key="AIzaSyA-5bYusWS0-K9hDU5bxk7NDX1AX2gAuOI")


import google.generativeai as genai

def generate_questions_for_job(job_title, num_questions=6):
    genai.configure(api_key="AIzaSyA-5bYusWS0-K9hDU5bxk7NDX1AX2gAuOI")

    prompt = f"""
You are an expert technical interviewer. Generate {num_questions} subjective competency questions for the job role: '{job_title}'.
Each question should test relevant skills. Provide only the questions without any additional text.

Format:
1. Question Text 
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text.strip()

import re
from .models import Question

def save_generated_questions(raw_response, job_role):
    question_lines = raw_response.strip().split('\n')
    for line in question_lines:
        match = re.match(r'^\d+\.\s+(.*?)\s*-\s*(easy|medium|hard)', line.strip(), re.IGNORECASE)
        if match:
            text = match.group(1).strip()
            difficulty = match.group(2).lower()
            Question.objects.create(job_role=job_role, text=text, difficulty=difficulty)

def evaluate_answer(question_text, user_answer):
    genai.configure(api_key="AIzaSyA-5bYusWS0-K9hDU5bxk7NDX1AX2gAuOI")

    prompt = f"""
You're an expert answers evaluator. The following question was asked:

Q: {question_text}

User's Answer: {user_answer}

On a scale of 0 to 1, how correct is the user's answer? 
Respond ONLY with a decimal score (e.g., 0.0, 0.5, 1.0)
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    try:
        score = float(response.text.strip())
        return max(0.0, min(1.0, score))
    except:
        return 0.0