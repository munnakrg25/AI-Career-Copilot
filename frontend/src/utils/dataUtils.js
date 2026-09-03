export function getNestedValue(object, paths, fallback = null) {
  for (const path of paths) {
    const parts = path.split(".");
    let value = object;

    for (const part of parts) {
      if (value === null || value === undefined) {
        value = undefined;
        break;
      }

      value = value[part];
    }

    if (value !== undefined && value !== null) {
      return value;
    }
  }

  return fallback;
}

export function getSkills(data) {
  const skills = getNestedValue(
    data,
    [
      "parsed_resume.skills",
      "parsed_data.skills",
      "resume.skills",
      "skills",
      "profile.skills",
    ],
    []
  );

  return Array.isArray(skills) ? skills : [];
}

export function getProjects(data) {
  const projects = getNestedValue(
    data,
    [
      "parsed_resume.projects",
      "parsed_data.projects",
      "resume.projects",
      "projects",
      "profile.projects",
    ],
    []
  );

  return Array.isArray(projects) ? projects : [];
}

export function getExperience(data) {
  const experience = getNestedValue(
    data,
    [
      "parsed_resume.experience",
      "parsed_data.experience",
      "resume.experience",
      "experience",
      "profile.experience",
    ],
    []
  );

  return Array.isArray(experience) ? experience : [];
}

export function getCertifications(data) {
  const certifications = getNestedValue(
    data,
    [
      "parsed_resume.certifications",
      "parsed_data.certifications",
      "resume.certifications",
      "certifications",
      "profile.certifications",
    ],
    []
  );

  return Array.isArray(certifications) ? certifications : [];
}

export function getJobReadiness(data) {
  return getNestedValue(
    data,
    [
      "job_readiness.overall_score",
      "job_readiness.score",
      "job_readiness.readiness_score",
      "overall_score",
      "readiness_score",
    ],
    0
  );
}

export function getCareerRecommendations(data) {
  const recommendations = getNestedValue(
    data,
    [
      "career_recommendations",
      "career_recommendation",
      "recommendations",
      "careers",
    ],
    []
  );

  return Array.isArray(recommendations) ? recommendations : [];
}

export function getGithub(data) {
  return getNestedValue(
    data,
    [
      "github",
      "github_data",
      "github_analysis",
    ],
    null
  );
}

export function getTargetRole(data) {
  return getNestedValue(
    data,
    [
      "target_role",
      "job_readiness.target_role",
      "skill_gap.target_role",
    ],
    "AI/ML Engineer"
  );
}
