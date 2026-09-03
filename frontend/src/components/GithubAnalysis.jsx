import { useState } from "react";
import api from "../api/api";

function GithubAnalysis() {
  const [username, setUsername] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyze = async () => {
    if (!username.trim()) {
      setError("Enter your GitHub username.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await api.post(
        `/github-analysis?username=${encodeURIComponent(username.trim())}`
      );

      setResult(response.data.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to analyze GitHub profile."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">

      <div className="page-intro">
        <span className="section-badge">DEVELOPER PROFILE</span>
        <h2>GitHub Analysis</h2>
        <p>
          Understand the quality and activity of your GitHub profile.
        </p>
      </div>

      <section className="tool-card github-search">

        <input
          type="text"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
          placeholder="Enter GitHub username"
        />

        <button
          className="primary-btn"
          onClick={analyze}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze GitHub →"}
        </button>

        {error && (
          <div className="error-box">
            ⚠ {error}
          </div>
        )}

      </section>

      {result && (
        <section className="github-results">

          <div className="github-profile-card">

            <div className="github-avatar">
              {result.username?.charAt(0)?.toUpperCase() || "G"}
            </div>

            <div>
              <h2>@{result.username || username}</h2>
              <p>GitHub Developer Profile</p>
            </div>

            <div className="github-score">
              <strong>{result.profile_score}</strong>
              <span>Profile Score</span>
            </div>

          </div>

          <div className="stats-grid github-stats">

            <Stat
              title="Repositories"
              value={result.total_repositories || 0}
              icon="📦"
            />

            <Stat
              title="Stars"
              value={result.total_stars || 0}
              icon="⭐"
            />

            <Stat
              title="Forks"
              value={result.total_forks || 0}
              icon="🍴"
            />

            <Stat
              title="Languages"
              value={
                Object.keys(result.languages || {}).length
              }
              icon="💻"
            />

          </div>

          <div className="analysis-grid">

            <div className="result-panel">

              <div className="panel-title">
                <h3>Programming Languages</h3>
              </div>

              <div className="language-list">

                {Object.entries(
                  result.languages || {}
                ).map(([language, count]) => (
                  <div
                    className="language-item"
                    key={language}
                  >
                    <span>{language}</span>
                    <strong>{count} repos</strong>
                  </div>
                ))}

              </div>

            </div>

            <div className="result-panel">

              <div className="panel-title">
                <h3>Profile Feedback</h3>
              </div>

              <div className="feedback-list">

                {(result.strengths || []).map(
                  (item, index) => (
                    <div className="feedback-item positive" key={index}>
                      ✓ {item}
                    </div>
                  )
                )}

                {(result.improvements || []).map(
                  (item, index) => (
                    <div className="feedback-item improvement" key={index}>
                      → {item}
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

function Stat({ title, value, icon }) {
  return (
    <div className="stat-card">
      <div className="stat-card-top">
        <div>
          <p className="stat-title">{title}</p>
          <h2>{value}</h2>
        </div>

        <div className="stat-icon">{icon}</div>
      </div>
    </div>
  );
}

export default GithubAnalysis;
