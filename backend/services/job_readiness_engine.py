from services.career_engine import CAREER_ROLES
from services.skill_normalizer import normalize_skills


def calculate_job_readiness(
    parsed_data,
    target_role,
    github_data=None
):
    if target_role not in CAREER_ROLES:
        raise ValueError("Invalid career role")

    skills = normalize_skills(
        parsed_data.get("skills", [])
    )

    skills = set(skills)

    projects = parsed_data.get(
        "projects",
        []
    )

    experience = parsed_data.get(
        "experience",
        []
    )

    education = parsed_data.get(
        "education",
        []
    )

    certifications = parsed_data.get(
        "certifications",
        []
    )

    role_skills = set(
        CAREER_ROLES[target_role]["skills"].keys()
    )

    # 1. Technical Skills - 25
    technical_skill_score = min(
        round((len(skills) / 15) * 25, 2),
        25
    )

    # 2. Projects - 20
    project_count = len(projects)

    if project_count >= 3:
        project_score = 20
    elif project_count == 2:
        project_score = 17
    elif project_count == 1:
        project_score = 10
    else:
        project_score = 0

    # 3. Experience - 15
    if len(experience) >= 4:
        experience_score = 15
    elif len(experience) >= 2:
        experience_score = 12
    elif len(experience) == 1:
        experience_score = 8
    else:
        experience_score = 0

    # 4. DSA - 10
    dsa_skills = {
        "dsa",
        "data structures",
        "algorithms"
    }

    has_dsa = bool(
        skills.intersection(dsa_skills)
    )

    dsa_score = 10 if has_dsa else 0

    # 5. Education - 10
    education_score = 10 if education else 0

    # 6. Certifications - 5
    certification_score = min(
        len(certifications) * 2.5,
        5
    )

    # 7. GitHub - 5
    github_score = 0

    if github_data:
        github_profile_score = github_data.get(
            "profile_score",
            0
        )

        github_score = round(
            (github_profile_score / 100) * 5,
            2
        )

    # 8. Role-specific Skills - 10
    matched_role_skills = skills.intersection(
        role_skills
    )

    if role_skills:
        role_skill_score = round(
            (
                len(matched_role_skills)
                / len(role_skills)
            ) * 10,
            2
        )
    else:
        role_skill_score = 0

    total_score = round(
        technical_skill_score
        + project_score
        + experience_score
        + dsa_score
        + education_score
        + certification_score
        + github_score
        + role_skill_score,
        2
    )

    total_score = min(
        total_score,
        100
    )

    strengths = []
    improvements = []

    # Technical skills
    if technical_skill_score >= 20:
        strengths.append(
            "Strong technical skill foundation"
        )
    else:
        improvements.append(
            "Improve technical skills relevant to the target role"
        )

    # Projects
    if project_score >= 17:
        strengths.append(
            "Good practical project experience"
        )
    else:
        improvements.append(
            "Build more real-world projects"
        )

    # Experience
    if experience_score >= 12:
        strengths.append(
            "Good practical experience"
        )
    else:
        improvements.append(
            "Gain more internship or industry experience"
        )

    # DSA
    if dsa_score == 10:
        strengths.append(
            "DSA knowledge detected"
        )
    else:
        improvements.append(
            "Improve Data Structures and Algorithms"
        )

    # Education
    if education_score > 0:
        strengths.append(
            "Educational background available"
        )
    else:
        improvements.append(
            "Add educational qualifications"
        )

    # Certifications
    if certification_score >= 2.5:
        strengths.append(
            "Relevant certifications available"
        )
    else:
        improvements.append(
            "Add relevant industry certifications"
        )

    # GitHub
    if github_score >= 3:
        strengths.append(
            "Good GitHub development activity"
        )
    else:
        improvements.append(
            "Improve GitHub project quality and documentation"
        )

    # Role-specific skills
    if role_skill_score >= 8:
        strengths.append(
            f"Strong skill match for {target_role}"
        )
    else:
        improvements.append(
            f"Develop more skills required for {target_role}"
        )

    return {
        "target_role": target_role,
        "overall_score": total_score,

        "readiness_level": (
            "Excellent"
            if total_score >= 85
            else "Good"
            if total_score >= 70
            else "Needs Improvement"
            if total_score >= 50
            else "Beginner"
        ),

        "breakdown": {
            "technical_skills": technical_skill_score,
            "projects": project_score,
            "experience": experience_score,
            "dsa": dsa_score,
            "education": education_score,
            "certifications": certification_score,
            "github": github_score,
            "role_specific_skills": role_skill_score
        },

        "role_skill_match": {
            "matched": sorted(
                matched_role_skills
            ),
            "total_required": len(
                role_skills
            ),
            "match_percentage": round(
                (
                    len(matched_role_skills)
                    / len(role_skills)
                ) * 100,
                2
            ) if role_skills else 0
        },

        "strengths": strengths,
        "improvements": improvements
    }
