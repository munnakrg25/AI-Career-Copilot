SKILL_ALIASES = {
    "react.js": "react",
    "drf": "django rest framework",
    "sqlite3": "sqlite",
    "rest api": "rest api",
    "jwt authentication": "jwt"
}


def normalize_skills(skills):
    normalized = set()

    for skill in skills:
        skill = skill.lower().strip()

        skill = SKILL_ALIASES.get(
            skill,
            skill
        )

        normalized.add(skill)

    return sorted(normalized)
