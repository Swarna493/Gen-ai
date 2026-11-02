
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!resume || !jobDescription.trim()) {
      setError("Please upload your resume and enter job description.");
      return;
    }

    setLoading(true);
    setError("");
    setAnalysis("");

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDescription);

    try {
      const apiUrl =
        import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

      const response = await fetch(`${apiUrl}/api/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Analysis failed");
      }

      setAnalysis(data.analysis);
    } catch (err) {
      setError(err.message || "Backend connection failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <header className="header">
        <h1>AI Resume Analyzer</h1>
        <p>Analyze your resume with Generative AI</p>
      </header>

      <form className="analyzer-card" onSubmit={handleSubmit}>
        <label>Upload Resume (PDF)</label>

        <input
          type="file"
          accept=".pdf,application/pdf"
          onChange={(e) => setResume(e.target.files[0] || null)}
        />

        {resume && (
          <p className="file-name">Selected: {resume.name}</p>
        )}

        <label>Job Description</label>

        <textarea
          rows="8"
          placeholder="Paste job description here..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>

        {error && <p className="error">{error}</p>}
      </form>

      {analysis && (
        <section className="result-card">
          <h2>Analysis Results</h2>

          <ReactMarkdown>
            {analysis.replace(/\\([#*])/g, "$1")}
          </ReactMarkdown>
        </section>
      )}

      <footer>
        Powered by React, Flask and Google Gemini
      </footer>
    </main>
  );
}

export default App;
