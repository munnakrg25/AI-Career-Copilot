import StatCard from "./StatCard";
import {
  getSkills,
  getProjects,
  getExperience,
  getJobReadiness,
  getTargetRole,
} from "../utils/dataUtils";

function Dashboard({ analysis, setActivePage }) {
  const skills = getSkills(analysis);
  const projects = getProjects(analysis);
  const experience = getExperience(analysis);
  const readiness = getJobReadiness(analysis);
  const targetRole = getTargetRole(analysis);

  const hasAnalysis = Object.keys(analysis || {}).length > 0;

  const skillCount = skills.length;
  const projectCount = projects.length;
  const experienceCount = experience.length;

  return (
    <div className="dashboard-page">

      <section className="hero-card">
        <div>
          <span className="hero-badge">AI CAREER MENTOR</span>

          <h2>
            Build your career with
            <span> AI-powered guidance.</span>
          </h2>

          <p>
            Upload your resume, analyze your skills, discover suitable
            career paths and prepare for interviews.
          </p>

          <button
            className="primary-btn"
            onClick={() => setActivePage("resume")}
          >
            Analyze My Resume →
          </button>
        </div>

        <div className="hero-visual">
          <div className="hero-circle">
            <span>AI</span>
          </div>
        </div>
      </section>

      <div className="stats-grid">

        <StatCard
          title="Job Readiness"
          value={`${readiness}%`}
          description={
            hasAnalysis
              ? "Based on your current profile"
              : "Upload resume to calculate"
          }
          icon="🎯"
        />

        <StatCard
          title="Skills Detected"
          value={skillCount || "—"}
          description={
            skillCount
              ? "Skills found in your resume"
              : "No analysis yet"
          }
          icon="⚡"
        />

        <StatCard
          title="Projects"
          value={projectCount || "—"}
          description="Practical projects detected"
          icon="💻"
        />

        <StatCard
          title="Experience"
          value={experienceCount || "—"}
          description="Experience entries detected"
          icon="💼"
        />

      </div>

      <div className="dashboard-grid">

        <section className="dashboard-card career-card">
          <div className="card-header">
            <div>
              <h3>Career Profile</h3>
              <p>Your selected career direction</p>
            </div>

            <span className="card-icon">🚀</span>
          </div>

          <div className="career-main">
            <div className="career-avatar">AI</div>

            <div>
              <h2>{targetRole}</h2>
              <p>
                Your profile is being evaluated for this role.
              </p>
            </div>
          </div>

          <button
            className="secondary-btn"
            onClick={() => setActivePage("career")}
          >
            Explore Career Paths
          </button>
        </section>

        <section className="dashboard-card">
          <div className="card-header">
            <div>
              <h3>Top Skills</h3>
              <p>Skills detected from your resume</p>
            </div>

            <span className="card-icon">⚡</span>
          </div>

          {skills.length > 0 ? (
            <div className="dashboard-skills">
              {skills.slice(0, 10).map((skill, index) => (
                <span key={index} className="skill-tag">
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <span>📄</span>
              <p>Analyze your resume to see your skills.</p>
            </div>
          )}
        </section>

      </div>

      <section className="dashboard-card roadmap-preview">

        <div className="card-header">
          <div>
            <h3>Career Roadmap</h3>
            <p>Your next steps toward your target role</p>
          </div>

          <button
            className="text-btn"
            onClick={() => setActivePage("roadmap")}
          >
            View Full Roadmap →
          </button>
        </div>

        <div className="roadmap-line">

          <div className="roadmap-step completed">
            <div className="step-number">1</div>
            <h4>Profile Analysis</h4>
            <p>Resume & skills</p>
          </div>

          <div className="roadmap-connector"></div>

          <div className="roadmap-step">
            <div className="step-number">2</div>
            <h4>Skill Development</h4>
            <p>Close skill gaps</p>
          </div>

          <div className="roadmap-connector"></div>

          <div className="roadmap-step">
            <div className="step-number">3</div>
            <h4>Projects</h4>
            <p>Build real projects</p>
          </div>

          <div className="roadmap-connector"></div>

          <div className="roadmap-step">
            <div className="step-number">4</div>
            <h4>Interview</h4>
            <p>Prepare & practice</p>
          </div>

        </div>
      </section>

    </div>
  );
}

export default Dashboard;
