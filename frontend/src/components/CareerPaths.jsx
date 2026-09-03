import { useState } from "react";
import api from "../api/api";
import { getCareerRecommendations } from "../utils/dataUtils";

function CareerPaths({ analysis, setActivePage }) {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Use pre-existing analysis data if available
  const cachedResults = getCareerRecommendations(analysis || {});
  const hasCache = cachedResults.length > 0;

  // displayed results: fresh fetch takes priority, otherwise use cached
  const displayResults = results.length > 0 ? results : cachedResults;

  const analyzeCareers = async () => {
    if (!file) {
      setError("Please upload your resume first.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post(
        "/career-recommendation",
        formData
      );

      setResults(response.data.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to generate career recommendations."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">

      <div className="page-intro">
        <span className="section-badge">CAREER AI</span>
        <h2>Career Paths</h2>
        <p>
          Discover which career roles match your current skills.
        </p>
      </div>

      {hasCache ? (
        <section className="tool-card">
          <div className="info-notice">
            ✓ Showing results from your last resume analysis.
            To re-analyze with a different resume, upload below.
          </div>

          <div className="tool-input-row">

            <label className="mini-file-input">
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files[0])}
              />
              📄{" "}
              {file ? file.name : "Upload different resume"}
            </label>

            <button
              className="primary-btn"
              onClick={analyzeCareers}
              disabled={loading || !file}
            >
              {loading ? "Analyzing..." : "Re-analyze →"}
            </button>

          </div>

          {error && (
            <div className="error-box">⚠ {error}</div>
          )}
        </section>
      ) : (
        <section className="tool-card">

          <div className="tool-input-row">

            <label className="mini-file-input">
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files[0])}
              />
              📄{" "}
              {file ? file.name : "Choose Resume"}
            </label>

            <button
              className="primary-btn"
              onClick={analyzeCareers}
              disabled={loading}
            >
              {loading ? "Analyzing..." : "Find Career Matches"}
            </button>

          </div>

          {error && (
            <div className="error-box">⚠ {error}</div>
          )}

          {!hasCache && !loading && (
            <div className="empty-state">
              <span>📄</span>
              <p>
                No resume analyzed yet.{" "}
                <button
                  className="text-btn"
                  onClick={() => setActivePage("resume")}
                >
                  Analyze your resume first →
                </button>
              </p>
            </div>
          )}

        </section>
      )}

      {displayResults.length > 0 && (
        <div className="career-results">

          {displayResults.map((career, index) => (
            <div
              className={`career-result-card ${
                index === 0 ? "top-match" : ""
              }`}
              key={career.role || index}
            >

              <div className="career-rank">
                #{index + 1}
              </div>

              <div className="career-content">

                <div className="career-result-header">
                  <div>
                    <h3>{career.role}</h3>
                    <p>
                      {career.matched_skills?.length || 0} matching skills
                    </p>
                  </div>

                  <div className="match-score">
                    {career.score}%
                    <span>Match</span>
                  </div>
                </div>

                <div className="progress-bar">
                  <div
                    style={{ width: `${career.score}%` }}
                  ></div>
                </div>

                <div className="career-skill-groups">

                  <div>
                    <span>Matched Skills</span>
                    <div className="skill-list">
                      {(career.matched_skills || []).map(
                        (skill, i) => (
                          <span
                            className="skill-tag success"
                            key={i}
                          >
                            ✓ {skill}
                          </span>
                        )
                      )}
                    </div>
                  </div>

                  <div>
                    <span>Skills to Develop</span>
                    <div className="skill-list">
                      {(career.missing_skills || []).slice(0, 6).map(
                        (skill, i) => (
                          <span
                            className="skill-tag missing"
                            key={i}
                          >
                            + {skill}
                          </span>
                        )
                      )}
                    </div>
                  </div>

                </div>

              </div>

            </div>
          ))}

        </div>
      )}

    </div>
  );
}

export default CareerPaths;
