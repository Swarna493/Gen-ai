
import os
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

gemini_client = (
    genai.Client(
        api_key=GEMINI_API_KEY,
        http_options={"timeout": 10000}
    )
    if GEMINI_API_KEY else None
)

groq_client = (
    Groq(
        api_key=GROQ_API_KEY,
        timeout=20.0,
        max_retries=0
    )
    if GROQ_API_KEY else None
)

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

    # 1. Try Gemini first with a short timeout
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

            print("Gemini returned an empty response.")

        except Exception as e:
    import traceback
    print("GROQ ERROR TYPE:", type(e).__name__)
    print("GROQ ERROR DETAILS:", repr(e))
    traceback.print_exc()

    # 2. Try Groq immediately if Gemini fails
    if groq_client:
        try:
            print("Trying Groq backup...")

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
            print(f"Groq failed: {type(e).__name__}: {e}")
            raise RuntimeError(
                "Both Gemini and Groq failed. Please try again later."
            ) from e

    raise RuntimeError(
        "No AI provider configured. Check your environment variables."
    )
