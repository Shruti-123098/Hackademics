import requests




import ollama

def enhance_with_ollama(prompt_text: str) -> str:
    """
    Enhances a given project description using the Mistral model via Ollama.

    Parameters:
    - prompt_text (str): The raw input project description.

    Returns:
    - str: Enhanced project description.
    """
    system_prompt = (
        "You are a professional technical writer. "
        "Enhance the following project description to make it clear, impressive, and resume-worthy. "
        "Focus on strong action verbs, real-world impact, technologies used, and clean formatting. "
        "Don't invent anything new, just polish what's already there."
        "return the enhanced description in bullet points"
        "limit to 3 bullet points"
    )

    response = ollama.chat(
        model='mistral',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_text}
        ]
    )

    return response['message']['content']