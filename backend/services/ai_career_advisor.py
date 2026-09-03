from services.llm_service import generate_career_advice_llm


def _rule_based_advice(parsed_data, github_data, target_role):
    """
    Original rule-based career advice.
    Used as a fallback when Gemini is unavailable or returns an invalid response.
    """
    skills = parsed_data.get("skills", [])
    projects = parsed_data.get("projects", [])
    experience = parsed_data.get("experience", [])
    certifications = parsed_data.get("certifications", [])

    advice = []
    strengths = []
    improvements = []
    next_steps = []

    if len(skills) >= 10:
        strengths.append("You have a strong technical skill foundation.")
    elif len(skills) >= 5:
        strengths.append("You have a good technical foundation.")
    else:
        improvements.append("Develop more role-specific technical skills.")

    if len(projects) >= 2:
        strengths.append(
            "Your project portfolio demonstrates practical development experience."
        )
    elif len(projects) == 1:
        improvements.append(
            "Build more real-world projects to strengthen your portfolio."
        )
    else:
        improvements.append("Build practical projects related to your target role.")

    if experience:
        strengths.append(
            "Your profile includes practical training or internship experience."
        )
    else:
        improvements.append("Gain internship or practical industry experience.")

    if certifications:
        strengths.append("You have relevant certifications that support your profile.")
    else:
        improvements.append("Add relevant industry certifications.")

    if github_data:
        repositories = github_data.get("total_repositories", 0)
        github_score = github_data.get("profile_score", 0)

        if repositories >= 10:
            strengths.append(
                "Your GitHub contains a good number of public repositories."
            )
        else:
            improvements.append("Increase the number of quality public repositories.")

        if github_score >= 70:
            strengths.append("Your GitHub profile shows good development activity.")
        else:
            improvements.append(
                "Improve GitHub project quality, documentation and visibility."
            )

    advice.append(f"Your selected target role is {target_role}.")

    if strengths:
        advice.append("Your strongest areas are: " + ", ".join(strengths))

    if improvements:
        advice.append("The main areas to improve are: " + ", ".join(improvements))

    next_steps.extend([
        f"Build one production-level project focused on {target_role}.",
        "Improve GitHub README files and project documentation.",
        "Practice role-specific technical interview questions.",
        "Strengthen DSA, SQL and problem-solving skills.",
        "Prepare a strong ATS-friendly resume.",
        "Practice mock interviews regularly."
    ])

    return {
        "target_role": target_role,
        "career_summary": (
            f"You are building a profile for {target_role}. "
            "Your current profile has a useful technical foundation, "
            "but continuous project building and interview preparation "
            "will improve your job readiness."
        ),
        "advice": advice,
        "strengths": strengths,
        "improvements": improvements,
        "next_steps": next_steps
    }


def generate_career_advice(parsed_data, github_data, target_role):
    """
    Generate personalised AI career advice using Gemini.
    Falls back to rule-based advice if Gemini is unavailable or returns an error.
    """
    try:
        return generate_career_advice_llm(parsed_data, github_data, target_role)
    except Exception:
        # Gemini unavailable, key missing, quota exceeded, or bad JSON — use fallback
        return _rule_based_advice(parsed_data, github_data, target_role)
