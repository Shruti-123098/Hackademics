import requests



from google import genai
import ollama
import google.generativeai as genai

def enhance_with_ollama(prompt_text: str) -> str:
    """
    Enhances a given project description using Gemini (Google Generative AI).

    Parameters:
    - prompt_text (str): The raw input project description.

    Returns:
    - str: Enhanced project description.
    """

    genai.configure(api_key="AIzaSyA-5bYusWS0-K9hDU5bxk7NDX1AX2gAuOI")

    model = genai.GenerativeModel("gemini-1.5-flash")

    system_prompt = (
        "You are a professional technical writer. "
        "Enhance the following project description to make it clear, impressive, and resume-worthy. "
        "Focus on strong action verbs, real-world impact, technologies used, and clean formatting. "
        "Don't invent anything new, just polish what's already there. "
        "Return the enhanced description in bullet points. "
        "Limit to 3 bullet points."
    )

    full_prompt = f"{system_prompt}\n\nPROJECT:\n{prompt_text}"

    # Correct use of generate_content — single string or list of parts
    response = model.generate_content(full_prompt)

    return response.text


# def enhance_with_ollama(prompt_text: str) -> str:
#     """
#     Enhances a given project description using the Mistral model via Ollama.

#     Parameters:
#     - prompt_text (str): The raw input project description.

#     Returns:
#     - str: Enhanced project description.
#     """
#     system_prompt = (
#         "You are a professional technical writer. "
#         "Enhance the following project description to make it clear, impressive, and resume-worthy. "
#         "Focus on strong action verbs, real-world impact, technologies used, and clean formatting. "
#         "Don't invent anything new, just polish what's already there."
#         "return the enhanced description in bullet points"
#         "limit to 3 bullet points"
#     )

#     # response = ollama.chat(
#     #     model='mistral',
#     #     messages=[
#     #         {"role": "system", "content": system_prompt},
#     #         {"role": "user", "content": prompt_text}
#     #     ]
#     # )
#     messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": prompt_text}
#         ]
    
#     client = genai.Client(api_key="AIzaSyA7-76P9rL6EoNKG19dYsr4dw912PhuNEw")

#     response = client.models.generate_content(
#         model="gemini-2.5-flash", contents=messages
#     )
#     print(response.text)

#     return response['message']['content']