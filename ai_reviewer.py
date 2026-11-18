
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3.8-flash"


def review_code_with_ai(source_code):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "ERROR: Gemini API key not found. Check your .env file."

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an expert Python code reviewer.

Review the following Python code.

Provide these sections:

1. CODE SUMMARY
2. BUGS AND LOGICAL ERRORS
3. CODE QUALITY
4. SECURITY ANALYSIS
5. IMPROVEMENT SUGGESTIONS
6. IMPROVED PYTHON CODE

Explain issues in simple language.
Give practical suggestions.
Do not execute the submitted code.
Do not claim that code is completely secure.

Submitted code:

{source_code}
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response.text:
            return response.text

        return "ERROR: Gemini returned an empty response."

    except Exception as error:
        return f"ERROR: Gemini API failed: {str(error)}"
