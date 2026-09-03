import { useState } from "react";
import api from "../api/api";
import {
  getSkills,
  getProjects,
  getExperience,
  getCertifications,
  getJobReadiness,
  getTargetRole,
} from "../utils/dataUtils";

function ResumeAnalysis({ onAnalysisComplete }) {
  const [file, setFile] = useState(null);
  const [targetRole, setTargetRole] = useState("AI/ML Engineer");
  const [githubUsername, setGithubUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please select your resume PDF.");
      return;
    }

    if (file.type !== "application/pdf") {
      setError("Only PDF resumes are supported.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();

      formData.append("file", file);
      formData.append("target_role", targetRole);

      if (githubUsername.trim()) {
        formData.append(
          "github_username",
          githubUsername.trim()
        );
      }

      const response = await api.post(
        "/unified-profile",
        formData
      );

      const data = response.data.data;

      setResult(data);

      if (onAnalysisComplete) {
        onAnalysisComplete(data);
      }
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
        "Unable to analyze your resume. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const skills = result ? getSkills(result) : [];
  const projects = result ? getProjects(result) : [];
  const experience = result ? getExperience(result) : [];
  const certifications = result
    ? getCertifications(result)
    : [];

  const readiness = result
    ? getJobReadiness(result)
    : 0;

  const role = result
    ? getTargetRole(result)
    : targetRole;

  return (
    <div className="page-container">

      <div className="page-intro">
        <div>
          <span className="section-badge">AI ANALYSIS</span>
          <h2>Analyze Your Resume</h2>
          <p>
            Upload your resume and get a personalized career profile.
          </p>
        </div>
      </div>

      <div className="resume-layout">

        <section className="form-card">

          <div className="form-card-header">
            <div className="large-icon">📄</div>
            <div>
              <h3>Resume Details</h3>
              <p>Provide your resume and career preferences.</p>
            </div>
          </div>

          <div className="form-group">
            <label>Resume PDF</label>

            <label className="file-drop">
              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={(e) => {
                  setFile(e.target.files[0] || null);
                  setError("");
                }}
              />

              <span className="upload-icon">☁</span>

              <strong>
                {file
                  ? file.name
                  : "Choose your resume"}
              </strong>

              <small>
                PDF format • Maximum recommended size 5MB
              </small>
            </label>
          </div>

          <div className="form-group">
            <label>Target Role</label>

            <select
              value={targetRole}
              onChange={(e) =>
                setTargetRole(e.target.value)
              }
            >
              <option>AI/ML Engineer</option>
              <option>Backend Developer</option>
              <option>Full Stack Developer</option>
              <option>Frontend Developer</option>
              <option>Data Scientist</option>
              <option>Data Analyst</option>
            </select>
          </div>

          <div className="form-group">
            <label>GitHub Username</label>

            <input
              type="text"
              value={githubUsername}
              onChange={(e) =>
                setGithubUsername(e.target.value)
              }
              placeholder="e.g. munnakrg25"
            />

            <small className="input-help">
              Optional — helps improve your profile analysis.
            </small>
          </div>

          {error && (
            <div className="error-box">
              ⚠ {error}
            </div>
          )}

          <button
            className="primary-btn full-btn"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing Profile...
              </>
            ) : (
              "Analyze My Profile →"
            )}
          </button>

        </section>

        {!result && (
          <section className="info-card">

            <div className="info-icon">✨</div>

            <h3>What you'll get</h3>

            <div className="feature-list">

              <div>
                <span>🎯</span>
                <p>
                  <strong>Job Readiness</strong>
                  <small>Understand your placement readiness.</small>
                </p>
              </div>

              <div>
                <span>🧠</span>
                <p>
                  <strong>Skill Analysis</strong>
                  <small>Identify strengths and missing skills.</small>
                </p>
              </div>

              <div>
                <span>🚀</span>
                <p>
                  <strong>Career Direction</strong>
                  <small>Find suitable career opportunities.</small>
                </p>
              </div>

              <div>
                <span>🗺</span>
                <p>
                  <strong>Learning Roadmap</strong>
                  <small>Get personalized next steps.</small>
                </p>
              </div>

            </div>

          </section>
        )}

      </div>

      {result && (
        <section className="analysis-results">

          <div className="results-title">
            <div>
              <span className="section-badge">ANALYSIS COMPLETE</span>
              <h2>Your Career Profile</h2>
              <p>
                AI has analyzed your resume and career profile.
              </p>
            </div>

            <div className="readiness-circle">
              <strong>{readiness}%</strong>
              <span>Readiness</span>
            </div>
          </div>

          <div className="result-stats">

            <div className="result-stat">
              <span>🎯</span>
              <p>Job Readiness</p>
              <strong>{readiness}%</strong>
            </div>

            <div className="result-stat">
              <span>💼</span>
              <p>Target Role</p>
              <strong>{role}</strong>
            </div>

            <div className="result-stat">
              <span>⚡</span>
              <p>Skills Detected</p>
              <strong>{skills.length}</strong>
            </div>

            <div className="result-stat">
              <span>💻</span>
              <p>Projects</p>
              <strong>{projects.length}</strong>
            </div>

          </div>

          <div className="analysis-grid">

            <div className="result-panel">

              <div className="panel-title">
                <h3>Detected Skills</h3>
                <span>{skills.length}</span>
              </div>

              {skills.length > 0 ? (
                <div className="skill-list">
                  {skills.map((skill, index) => (
                    <span
                      className="skill-tag"
                      key={index}
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  No skills detected.
                </div>
              )}

            </div>

            <div className="result-panel">

              <div className="panel-title">
                <h3>Profile Summary</h3>
              </div>

              <div className="profile-details">

                <div>
                  <span>Name</span>
                  <strong>
                    {result.candidate?.name || "Not detected"}
                  </strong>
                </div>

                <div>
                  <span>Email</span>
                  <strong>
                    {result.candidate?.email || "Not detected"}
                  </strong>
                </div>

                <div>
                  <span>Experience</span>
                  <strong>{experience.length} entries</strong>
                </div>

                <div>
                  <span>Certifications</span>
                  <strong>{certifications.length}</strong>
                </div>

              </div>

            </div>

          </div>

        </section>
      )}

    </div>
  );
}

export default ResumeAnalysis;
