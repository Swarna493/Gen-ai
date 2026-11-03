import requests

url = "http://127.0.0.1:5000/api/analyze"

job_description = """
We are looking for a Python Developer with skills in Python,
Machine Learning, Deep Learning, TensorFlow, SQL, JavaScript,
HTML, and data analysis. The candidate should have good
problem-solving and communication skills.
"""

with open("resume.pdf", "rb") as resume:
    files = {
        "resume": resume
    }

    data = {
        "job_description": job_description
    }

    response = requests.post(
        url,
        files=files,
        data=data
    )

print("Status Code:", response.status_code)
print(response.json())