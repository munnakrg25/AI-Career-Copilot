from services.skill_normalizer import normalize_skills


CAREER_ROLES = {
    "AI/ML Engineer": {
        "skills": {
            "python": 10,
            "machine learning": 20,
            "deep learning": 15,
            "tensorflow": 10,
            "scikit-learn": 10,
            "pandas": 5,
            "numpy": 5,
            "sql": 5,
            "nlp": 10,
            "git": 5
        }
    },

    "Backend Developer": {
        "skills": {
            "python": 15,
            "django": 15,
            "fastapi": 15,
            "sql": 10,
            "postgresql": 10,
            "rest apis": 15,
            "jwt": 5,
            "git": 5,
            "docker": 10
        }
    },

    "Full Stack Developer": {
        "skills": {
            "python": 10,
            "javascript": 10,
            "html": 5,
            "css": 5,
            "react": 15,
            "django": 10,
            "django rest framework": 10,
            "sql": 5,
            "postgresql": 5,
            "git": 5,
            "rest apis": 10,
            "jwt": 5
        }
    },

    "Frontend Developer": {
        "skills": {
            "html": 15,
            "css": 15,
            "javascript": 20,
            "react": 25,
            "git": 10,
            "bootstrap": 5,
            "tailwind css": 10
        }
    },

    "Data Scientist": {
        "skills": {
            "python": 15,
            "machine learning": 20,
            "pandas": 10,
            "numpy": 10,
            "scikit-learn": 15,
            "matplotlib": 5,
            "seaborn": 5,
            "sql": 10,
            "deep learning": 10
        }
    },

    "Data Analyst": {
        "skills": {
            "python": 15,
            "sql": 20,
            "pandas": 15,
            "numpy": 10,
            "matplotlib": 10,
            "seaborn": 10,
            "excel": 10,
            "power bi": 10
        }
    }
}


def recommend_careers(user_skills):

    user_skills = normalize_skills(user_skills)

    user_skills = set(user_skills)

    recommendations = []

    for role, data in CAREER_ROLES.items():

        required_skills = data["skills"]

        matched_skills = []
        missing_skills = []

        matched_weight = 0
        total_weight = sum(
            required_skills.values()
        )

        for skill, weight in required_skills.items():

            if skill in user_skills:

                matched_skills.append(skill)

                matched_weight += weight

            else:

                missing_skills.append(skill)

        score = round(
            (matched_weight / total_weight) * 100,
            2
        )

        recommendations.append({
            "role": role,
            "score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return recommendations
