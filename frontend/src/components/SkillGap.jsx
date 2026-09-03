import { useState } from "react";
import api from "../api/api";
import { getSkills, getTargetRole } from "../utils/dataUtils";

function SkillGap({ analysis, setActivePage }) {
  const hasAnalysis = Object.keys(analysis || {}).length > 0;

  // Derive initial values from existing analysis
  const cachedSkillGap = analysis?.target_role_analysis?.skill_gap || null;
  const initialRole = getTargetRole(analysis || {});

  const [targetRole, setTargetRole] = useState(initialRole);
  const [result, setResult] = useState(cachedSkillGap);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyze = async () => {
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
        "/skill-gap-by-skills",
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
        "Unable to analyze skill gap."
      );
    } finally {
      setLoading(false);
    }
  };

  // When the user changes the role, run analysis automatically
  const handleRoleChange = (e) => {
    setTargetRole(e.target.value);
    setResult(null);
  };

  return (
    <div className="page-container">

      <div className="page-intro">
        <span className="section-badge">SKILL GAP AI</span>
        <h2>Skill Gap Analysis</h2>
        <p>
          Identify the skills you already have and the skills you need.
        </p>
      </div>

      <section className="tool-card">

        {hasAnalysis ? (
          <>
            <div className="info-notice">
              ✓ Using skills from your last resume analysis. Change the
              target role and click Analyze to update.
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
              onClick={analyze}
              disabled={loading}
            >
              {loading ? "Analyzing..." : "Analyze Skill Gap →"}
            </button>
          </>
        ) : (
          <>
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
          </>
        )}

        {error && (
          <div className="error-box">⚠ {error}</div>
        )}

      </section>

      {result && (
        <section className="skill-gap-results">

          <div className="gap-summary">

            <div>
              <span className="section-badge">
                {result.target_role}
              </span>

              <h2>Skill Readiness</h2>

              <p>
                Your current skill match for the selected role.
              </p>
            </div>

            <div className="big-score">
              {result.readiness_score}%
              <span>Readiness</span>
            </div>

          </div>

          <div className="gap-columns">

            <div className="result-panel">

              <div className="panel-title">
                <h3>Strong Skills</h3>
                <span>
                  {result.strong_skills?.length || 0}
                </span>
              </div>

              <div className="skill-list">
                {(result.strong_skills || []).map(
                  (skill, index) => (
                    <span
                      className="skill-tag success"
                      key={index}
                    >
                      ✓ {skill}
                    </span>
                  )
                )}
              </div>

            </div>

            <div className="result-panel">

              <div className="panel-title">
                <h3>Missing Skills</h3>
                <span>
                  {result.missing_skills?.length || 0}
                </span>
              </div>

              <div className="missing-skill-list">

                {(result.missing_skills || []).map(
                  (item, index) => (
                    <div
                      className="missing-skill-item"
                      key={index}
                    >
                      <div>
                        <strong>{item.skill}</strong>
                        <span>
                          Priority: {item.priority}
                        </span>
                      </div>

                      <span className="weight">
                        {item.weight}
                      </span>
                    </div>
                  )
                )}

              </div>

            </div>

          </div>

        </section>
      )}

    </div>
  );
}

export default SkillGap;
