from services.career_engine import CAREER_ROLES


def analyze_skill_gap(user_skills, target_role):

    user_skills = {
        skill.lower().strip()
        for skill in user_skills
    }

    role = CAREER_ROLES.get(target_role)

    if not role:
        raise ValueError("Invalid career role")

    required_skills = role["skills"]

    matched = []
    missing = []

    total_weight = sum(required_skills.values())
    matched_weight = 0

    for skill, weight in required_skills.items():

        if skill in user_skills:
            matched.append(skill)
            matched_weight += weight
        else:
            if weight >= 15:
                priority = "High"
            elif weight >= 10:
                priority = "Medium"
            else:
                priority = "Low"

            missing.append({
                "skill": skill,
                "weight": weight,
                "priority": priority
            })

    readiness_score = round(
        (matched_weight / total_weight) * 100,
        2
    )

    missing.sort(
        key=lambda x: x["weight"],
        reverse=True
    )

    return {
        "target_role": target_role,
        "readiness_score": readiness_score,
        "strong_skills": matched,
        "missing_skills": missing
    }
