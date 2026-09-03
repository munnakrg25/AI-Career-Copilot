import { useEffect, useState } from "react";

import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";

import Dashboard from "./components/Dashboard";
import ResumeAnalysis from "./components/ResumeAnalysis";
import CareerPaths from "./components/CareerPaths";
import SkillGap from "./components/SkillGap";
import Roadmap from "./components/Roadmap";
import GithubAnalysis from "./components/GithubAnalysis";
import MockInterview from "./components/MockInterview";

import "./App.css";

function App() {
  const [activePage, setActivePage] =
    useState("dashboard");

  const [analysis, setAnalysis] = useState(() => {
    try {
      const saved =
        localStorage.getItem("career_analysis");

      return saved ? JSON.parse(saved) : {};
    } catch {
      return {};
    }
  });

  useEffect(() => {
    localStorage.setItem(
      "career_analysis",
      JSON.stringify(analysis)
    );
  }, [analysis]);

  const handleAnalysisComplete = (data) => {
    setAnalysis(data);
  };

  const renderPage = () => {
    switch (activePage) {
      case "resume":
        return (
          <ResumeAnalysis
            onAnalysisComplete={handleAnalysisComplete}
          />
        );

      case "career":
        return (
          <CareerPaths
            analysis={analysis}
            setActivePage={setActivePage}
          />
        );

      case "skill-gap":
        return (
          <SkillGap
            analysis={analysis}
            setActivePage={setActivePage}
          />
        );

      case "roadmap":
        return (
          <Roadmap
            analysis={analysis}
            setActivePage={setActivePage}
          />
        );

      case "github":
        return <GithubAnalysis />;

      case "interview":
        return <MockInterview />;

      case "dashboard":
      default:
        return (
          <Dashboard
            analysis={analysis}
            setActivePage={setActivePage}
          />
        );
    }
  };

  return (
    <div className="app">

      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <main className="main-content">

        <Topbar activePage={activePage} />

        <div className="content-area">
          {renderPage()}
        </div>

      </main>

    </div>
  );
}

export default App;
