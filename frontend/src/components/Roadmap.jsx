import { useState } from "react";
import api from "../api/api";
import { getSkills, getTargetRole } from "../utils/dataUtils";

function Roadmap({ analysis, setActivePage }) {
  const hasAnalysis = Object.keys(analysis || {}).length > 0;

  // Derive initial values from existing analysis
  const cachedRoadmap = analysis?.target_role_analysis?.roadmap || null;
  const initialRole = getTargetRole(analysis || {});

  const [targetRole, setTargetRole] = useState(initialRole);
  const [result, setResult] = useState(cachedRoadmap);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateRoadmap = async () => {
    if (!hasAnalysis) {
      setError("Please analyze your resume first.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      // Re-use skills already extracted from the resume — no file re-upload needed
      const skills = getSkills(analysis);

      const response = await api.get(
        "/roadmap-by-skills",
        {
          params: {
            target_role: targetRole,
            skills: skills.join(","),
          },
        }
      );

      setResult(response.data.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to generate roadmap."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleRoleChange = (e) => {
    setTargetRole(e.target.value);
    setResult(null);
  };

  return (
    <div className="page-container">

      <div className="page-intro">
        <span className="section-badge">PERSONALIZED PLAN</span>
        <h2>Learning Roadmap</h2>
        <p>
          Follow a structured path to become job-ready.
        </p>
      </div>

      <section className="tool-card">

        {hasAnalysis ? (
          <>
            <div className="info-notice">
              ✓ Using skills from your last resume analysis. Change the
              target role and click Generate to update.
            </div>

            <div className="tool-form-grid">
              <div>
                <label>Target Role</label>
                <select
                  value={targetRole}
                  onChange={handleRoleChange}
                >
                  <option>AI/ML Engineer</option>
                  <option>Backend Developer</option>
                  <option>Full Stack Developer</option>
                  <option>Frontend Developer</option>
                  <option>Data Scientist</option>
                  <option>Data Analyst</option>
                </select>
              </div>
            </div>

            <button
              className="primary-btn"
              onClick={generateRoadmap}
              disabled={loading}
            >
              {loading ? "Generating..." : "Generate Roadmap →"}
            </button>
          </>
        ) : (
          <>
            <div className="empty-state">
              <span>🗺</span>
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
          </>
        )}

        {error && (
          <div className="error-box">⚠ {error}</div>
        )}

      </section>

      {result && (
        <section className="roadmap-results">

          <div className="roadmap-heading">

            <div>
              <span className="section-badge">
                {result.target_role}
              </span>

              <h2>
                {result.roadmap_duration} Career Roadmap
              </h2>

              <p>
                Personalized learning recommendations based on your profile.
              </p>
            </div>

          </div>

          <div className="timeline">

            {(result.roadmap || []).map(
              (phase, index) => (
                <div className="timeline-item" key={index}>

                  <div className="timeline-marker">
                    {phase.month}
                  </div>

                  <div className="timeline-content">

                    <span className="month-label">
                      MONTH {phase.month}
                    </span>

                    <h3>{phase.focus}</h3>

                    <div className="topic-list">

                      {(phase.recommended_topics || phase.topics || []).map(
                        (topic, i) => (
                          <div
                            className="topic-item"
                            key={i}
                          >
                            <span>✓</span>
                            {topic}
                          </div>
                        )
                      )}

                    </div>

                  </div>

                </div>
              )
            )}

          </div>

        </section>
      )}

    </div>
  );
}

export default Roadmap;
