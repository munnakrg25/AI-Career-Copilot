function Sidebar({ activePage, setActivePage }) {
  const mainItems = [
    { id: "dashboard", icon: "⌂", label: "Dashboard" },
    { id: "resume", icon: "▣", label: "Resume Analysis" },
    { id: "career", icon: "◆", label: "Career Paths" },
    { id: "skill-gap", icon: "◇", label: "Skill Gap" },
    { id: "roadmap", icon: "▥", label: "Roadmap" },
  ];

  const toolItems = [
    { id: "github", icon: "○", label: "GitHub Analysis" },
    { id: "interview", icon: "✦", label: "AI Mock Interview" },
  ];

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-logo">AI</div>

        <div>
          <h2>Career Copilot</h2>
          <p>AI Career Mentor</p>
        </div>
      </div>

      <div className="sidebar-section">
        <p className="sidebar-label">MAIN</p>

        {mainItems.map((item) => (
          <button
            key={item.id}
            className={`sidebar-item ${
              activePage === item.id ? "active" : ""
            }`}
            onClick={() => setActivePage(item.id)}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </div>

      <div className="sidebar-section tools-section">
        <p className="sidebar-label">TOOLS</p>

        {toolItems.map((item) => (
          <button
            key={item.id}
            className={`sidebar-item ${
              activePage === item.id ? "active" : ""
            }`}
            onClick={() => setActivePage(item.id)}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </div>

      <div className="sidebar-user">
        <div className="user-avatar">MK</div>

        <div>
          <strong>Munna Kumar</strong>
          <span>Candidate</span>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
