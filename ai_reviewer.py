
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL_NAME = "openai/gpt-oss-20b"


def review_code_with_ai(source_code):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "ERROR: Groq API key not found. Check your .env file."

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
You are an experienced Python code reviewer.

Analyze the following Python code and provide a concise,
useful code review.

Cover these sections:

Provide these sections:

1. CODE SUMMARY
2. BUGS AND LOGICAL ERRORS
3. CODE QUALITY AND BEST PRACTICES
4. SECURITY ANALYSIS
5. PERFORMANCE IMPROVEMENTS
6. IMPROVEMENT SUGGESTIONS
7. COMPLETE CORRECTED CODE

For every issue:
- Explain the problem.
- Mention the line number if possible.
- Provide a suggested correction.

If no issues are found, clearly mention that.

Keep the review simple and easy to understand.
When suggesting improved code:
- Preserve the original code structure whenever possible.
- Prefer simple solutions over unnecessary additional functions.
- Use if conditions for straightforward validation when appropriate.
- Do not introduce extra functions unless they provide a clear benefit.
- Explain why the suggested correction is better.
- Always provide the complete corrected version of the submitted code.
- Do not provide only example usage or isolated code snippets.
- Ensure the improved code addresses the identified issue.
- Preserve the original function names and structure unless a change is necessary.
CODE TO REVIEW:

{source_code}
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=1200
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"ERROR: Groq API failed: {str(e)}"
