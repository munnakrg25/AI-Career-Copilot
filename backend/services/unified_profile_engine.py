from services.career_engine import recommend_careers
from services.skill_gap_engine import analyze_skill_gap
from services.roadmap_engine import generate_roadmap
from services.job_readiness_engine import calculate_job_readiness
from services.ai_career_advisor import generate_career_advice
from services.skill_normalizer import normalize_skills


async def generate_unified_profile(
    parsed_data,
    target_role,
    github_data=None
):
    skills = normalize_skills(
        parsed_data.get("skills", [])
    )

    career_recommendations = recommend_careers(skills)

    skill_gap = analyze_skill_gap(
        skills,
        target_role
    )

    roadmap = generate_roadmap(
        skills,
        target_role
    )

    job_readiness = calculate_job_readiness(
        parsed_data,
        target_role
    )

    ai_career_advice = generate_career_advice(
        parsed_data,
        github_data,
        target_role
    )

    profile = {
        "target_role": target_role,

        "candidate": {
            "name": parsed_data.get("name"),
            "email": parsed_data.get("email"),
            "phone": parsed_data.get("phone")
        },

        "resume": {
            "name": parsed_data.get("name"),
            "email": parsed_data.get("email"),
            "phone": parsed_data.get("phone"),
            "skills": skills,
            "education": parsed_data.get("education", []),
            "experience": parsed_data.get("experience", []),
            "projects": parsed_data.get("projects", []),
            "certifications": parsed_data.get("certifications", [])
        },

        "career_recommendations": career_recommendations,

        "target_role_analysis": {
            "target_role": target_role,
            "skill_gap": skill_gap,
            "roadmap": roadmap
        },

        "job_readiness": job_readiness,

        "ai_career_advice": ai_career_advice
    }

    if github_data:
        profile["github"] = github_data

    return profile
