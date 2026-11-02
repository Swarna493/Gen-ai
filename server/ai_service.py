
import os
import time
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

PROMPT_TEMPLATE = """
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


def analyze_resume(resume_text, job_description):
    prompt = PROMPT_TEMPLATE.format(
        resume_text=resume_text,
        job_description=job_description
    )

    # Try Gemini first
    if gemini_client:
        try:
            print("Trying Gemini...")

            response = gemini_client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            if response.text:
                print("Gemini analysis successful!")
                return response.text

            raise ValueError("Gemini returned an empty response.")

        except Exception as e:
            print(f"Gemini failed: {e}")
            print("Trying Groq as backup...")

    # Use Groq if Gemini fails
    if groq_client:
        try:
            print("Trying Groq...")

            completion = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            result = completion.choices[0].message.content

            if result:
                print("Groq analysis successful!")
                return result

            raise ValueError("Groq returned an empty response.")

        except Exception as e:
            raise RuntimeError(f"Groq backup also failed: {e}")

    raise RuntimeError(
        "No AI provider is configured. Check GEMINI_API_KEY and GROQ_API_KEY."
    )
