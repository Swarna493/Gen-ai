from ai_service import analyze_resume

resume = """
Python developer with skills in Python, Flask, SQL and React.
"""

job_description = """
Looking for a Python developer with Python, Flask, SQL,
React and Machine Learning skills.
"""

result = analyze_resume(resume, job_description)

print(result)