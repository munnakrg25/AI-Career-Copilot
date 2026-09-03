import re


SKILLS = [
    "python",
    "java",
    "c++",
    "c",
    "javascript",
    "typescript",
    "react",
    "react.js",
    "node.js",
    "django",
    "django rest framework",
    "drf",
    "fastapi",
    "flask",
    "spring boot",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "sqlite3",
    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "html",
    "css",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "rest api",
    "rest apis",
    "jwt",
    "jwt authentication",
    "bootstrap",
    "tailwind css",
    "data structures",
    "algorithms",
    "dsa",
    "oop",
    "dbms",
    "os",
    "computer networks",
    "excel",
    "power bi"
]


def clean_text(text: str):
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_email(text: str):
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group(0) if match else None


def extract_phone(text: str):
    match = re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    return match.group(0) if match else None


def extract_name(text: str):
    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    if not lines:
        return None

    return lines[0]


def extract_skills(text: str):

    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(skill)
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))


def get_section_lines(text: str, start_heading: str, end_headings: list):

    lines = text.split("\n")

    collecting = False
    section = []

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        if not collecting:

            if start_heading.lower() in lower_line:
                collecting = True

            continue

        if any(
            heading.lower() in lower_line
            for heading in end_headings
        ):
            break

        section.append(clean_line)

    return section


def extract_education(text: str):

    return get_section_lines(
        text,
        "Education",
        [
            "Technical Skills",
            "Projects",
            "Training & Internship",
            "Achievements & Coding",
            "Certifications"
        ]
    )


def extract_experience(text: str):

    return get_section_lines(
        text,
        "Training & Internship",
        [
            "Achievements & Coding",
            "Certifications"
        ]
    )


def extract_projects(text: str):

    lines = get_section_lines(
        text,
        "Projects",
        [
            "Training & Internship",
            "Achievements & Coding",
            "Certifications"
        ]
    )

    projects = []

    current_project = None

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        date_match = re.search(
            r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
            r"\s+\d{4}",
            clean_line,
            re.IGNORECASE
        )

        if date_match:

            if current_project:
                projects.append(current_project)

            project_name = clean_line[:date_match.start()].strip()

            date = date_match.group(0)

            current_project = {
                "name": project_name,
                "date": date,
                "technologies": [],
                "description": []
            }

            continue

        if current_project is None:
            continue

        if (
            clean_line.startswith("·")
            or clean_line.startswith("-")
            or clean_line.startswith("•")
        ):

            description = re.sub(
                r"^[·•-]\s*",
                "",
                clean_line
            )

            current_project["description"].append(
                description
            )

        elif not current_project["technologies"]:

            technologies = [
                tech.strip()
                for tech in clean_line.split(",")
                if tech.strip()
            ]

            current_project["technologies"] = technologies

    if current_project:
        projects.append(current_project)

    return projects

def extract_certifications(text: str):
    return get_section_lines(
        text,
        "Certifications",
        []
    )


def parse_resume(text: str):
    cleaned_text = clean_text(text)

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text),
        "certifications": extract_certifications(text)
    }
