
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

client = genai.Client(api_key=API_KEY)


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an AI Resume and Job Description Analyzer.

Analyze the following resume and job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide the analysis in this format:

1. Match Score:
2. Matching Skills:
3. Missing Skills:
4. Resume Strengths:
5. Resume Improvement Suggestions:
6. Job Requirements Summary:
7. Interview Questions:

Keep the analysis clear, accurate, and concise.
Do not invent skills or qualifications that are not present in the resume.
"""

    for attempt in range(2):

        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            return response.text

        except Exception as e:

            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt == 0:
                    print(
                        "Gemini temporarily unavailable. "
                        "Retrying in 3 seconds..."
                    )

                    time.sleep(3)
                    continue

            raise e
