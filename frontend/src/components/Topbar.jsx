const pageTitles = {
  dashboard: ["Dashboard", "Welcome back! Here's your career overview."],
  resume: ["Resume Analysis", "Analyze your resume with AI."],
  career: ["Career Paths", "Discover career opportunities based on your skills."],
  "skill-gap": ["Skill Gap", "Find the skills you need to improve."],
  roadmap: ["Learning Roadmap", "Your personalized career learning path."],
  github: ["GitHub Analysis", "Analyze your development profile."],
  interview: ["AI Mock Interview", "Practice technical interviews with AI."],
};

function Topbar({ activePage }) {
  const [title, subtitle] =
    pageTitles[activePage] || pageTitles.dashboard;

  return (
    <header className="topbar">
      <div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>

      <div className="topbar-actions">
        <button className="notification-btn">🔔</button>
        <button className="top-avatar">MK</button>
      </div>
    </header>
  );
}

export default Topbar;
