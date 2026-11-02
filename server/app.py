from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
from ai_service import analyze_resume
import tempfile
import os

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Resume and Job Description GenAI Backend is Running!"


def extract_resume_text(pdf_file):

    # First try normal PDF text extraction
    reader = PdfReader(pdf_file)
    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text + "\n"

    # If normal extraction works, return the text
    if resume_text.strip():
        return resume_text

    # OCR fallback for scanned/image PDFs
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        pdf_file.seek(0)
        temp.write(pdf_file.read())
        temp_path = temp.name

    try:
        pages = convert_from_path(temp_path)

        ocr_text = ""

        for page in pages:
            ocr_text += pytesseract.image_to_string(page) + "\n"

        return ocr_text

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route("/api/analyze", methods=["POST"])
def analyze():

    try:
        resume_file = request.files.get("resume")
        job_description = request.form.get("job_description")

        if not resume_file:
            return jsonify({
                "error": "Resume PDF is required"
            }), 400

        if not job_description:
            return jsonify({
                "error": "Job description is required"
            }), 400

        resume_text = extract_resume_text(resume_file)

        if not resume_text.strip():
            return jsonify({
                "error": "Could not extract text from resume PDF"
            }), 400

        result = analyze_resume(
            resume_text,
            job_description
        )

        return jsonify({
            "success": True,
            "analysis": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)