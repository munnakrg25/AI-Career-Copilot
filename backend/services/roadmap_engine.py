from services.career_engine import CAREER_ROLES
from services.skill_normalizer import normalize_skills


ROADMAPS = {
    "AI/ML Engineer": [
        {
            "month": 1,
            "focus": "Advanced Machine Learning",
            "topics": [
                "Feature Engineering",
                "Model Selection",
                "Hyperparameter Tuning",
                "Ensemble Learning"
            ]
        },
        {
            "month": 2,
            "focus": "Advanced Deep Learning",
            "topics": [
                "Neural Networks",
                "CNN",
                "RNN",
                "Transformers"
            ]
        },
        {
            "month": 3,
            "focus": "NLP & Generative AI",
            "topics": [
                "Text Classification",
                "Embeddings",
                "LLM Fundamentals",
                "Prompt Engineering",
                "RAG"
            ]
        },
        {
            "month": 4,
            "focus": "MLOps & Deployment",
            "topics": [
                "FastAPI",
                "Docker",
                "Model Deployment",
                "API Integration",
                "Cloud Deployment"
            ]
        },
        {
            "month": 5,
            "focus": "End-to-End AI/ML Project",
            "topics": [
                "Real World Dataset",
                "Data Preprocessing",
                "Model Training",
                "Model Evaluation",
                "GitHub Documentation"
            ]
        },
        {
            "month": 6,
            "focus": "AI/ML Placement Preparation",
            "topics": [
                "ML Interview Questions",
                "Python",
                "SQL",
                "DSA",
                "ML System Design",
                "Mock Interviews"
            ]
        }
    ],

    "Backend Developer": [
        {
            "month": 1,
            "focus": "Backend Fundamentals",
            "topics": [
                "FastAPI",
                "Django",
                "REST APIs",
                "Authentication",
                "PostgreSQL"
            ]
        },
        {
            "month": 2,
            "focus": "Production Backend",
            "topics": [
                "JWT",
                "API Security",
                "Docker",
                "Testing",
                "Database Optimization"
            ]
        },
        {
            "month": 3,
            "focus": "Backend Project & Deployment",
            "topics": [
                "System Design",
                "Cloud Deployment",
                "CI/CD",
                "Monitoring",
                "Production Project"
            ]
        }
    ],

    "Full Stack Developer": [
        {
            "month": 1,
            "focus": "Frontend Development",
            "topics": [
                "React",
                "JavaScript",
                "HTML",
                "CSS",
                "Tailwind CSS"
            ]
        },
        {
            "month": 2,
            "focus": "Backend & Database",
            "topics": [
                "Django",
                "DRF",
                "REST APIs",
                "PostgreSQL",
                "JWT"
            ]
        },
        {
            "month": 3,
            "focus": "Full Stack Project & Deployment",
            "topics": [
                "Docker",
                "Cloud Deployment",
                "Testing",
                "GitHub",
                "Production Project"
            ]
        }
    ],

    "Frontend Developer": [
        {
            "month": 1,
            "focus": "HTML, CSS & JavaScript Fundamentals",
            "topics": [
                "HTML",
                "CSS",
                "JavaScript",
                "Responsive Design",
                "Flexbox"
            ]
        },
        {
            "month": 2,
            "focus": "React & Component Architecture",
            "topics": [
                "React",
                "useState",
                "useEffect",
                "Props",
                "React Router"
            ]
        },
        {
            "month": 3,
            "focus": "Styling & UI Libraries",
            "topics": [
                "Tailwind CSS",
                "Bootstrap",
                "CSS Animations",
                "Design Systems"
            ]
        },
        {
            "month": 4,
            "focus": "Frontend Project & Deployment",
            "topics": [
                "Git",
                "GitHub",
                "Vite",
                "Netlify Deployment",
                "Portfolio Project"
            ]
        }
    ],

    "Data Scientist": [
        {
            "month": 1,
            "focus": "Python & Data Manipulation",
            "topics": [
                "Python",
                "Pandas",
                "NumPy",
                "Data Cleaning",
                "Exploratory Data Analysis"
            ]
        },
        {
            "month": 2,
            "focus": "Machine Learning Fundamentals",
            "topics": [
                "Scikit-learn",
                "Supervised Learning",
                "Model Evaluation",
                "Cross-Validation",
                "Feature Engineering"
            ]
        },
        {
            "month": 3,
            "focus": "Advanced ML & Deep Learning",
            "topics": [
                "Deep Learning",
                "TensorFlow",
                "Neural Networks",
                "Ensemble Methods",
                "Hyperparameter Tuning"
            ]
        },
        {
            "month": 4,
            "focus": "Data Science Project & Deployment",
            "topics": [
                "SQL",
                "Data Visualisation",
                "Model Deployment",
                "GitHub Documentation",
                "End-to-End Project"
            ]
        }
    ],

    "Data Analyst": [
        {
            "month": 1,
            "focus": "SQL & Database Fundamentals",
            "topics": [
                "SQL",
                "Joins",
                "Aggregations",
                "Subqueries",
                "Database Design"
            ]
        },
        {
            "month": 2,
            "focus": "Python for Data Analysis",
            "topics": [
                "Python",
                "Pandas",
                "NumPy",
                "Data Cleaning",
                "Exploratory Analysis"
            ]
        },
        {
            "month": 3,
            "focus": "Data Visualisation & Reporting",
            "topics": [
                "Matplotlib",
                "Seaborn",
                "Power BI",
                "Excel",
                "Dashboard Design"
            ]
        },
        {
            "month": 4,
            "focus": "Analytics Project & Portfolio",
            "topics": [
                "End-to-End Analytics Project",
                "Storytelling with Data",
                "GitHub Documentation",
                "Business Insights"
            ]
        }
    ]
}


TOPIC_ALIASES = {
    "react": ["react", "react.js"],
    "django": ["django"],
    "django rest framework": ["django rest framework", "drf"],
    "postgresql": ["postgresql", "postgres"],
    "jwt": ["jwt", "jwt authentication"],
    "fastapi": ["fastapi"],
    "python": ["python"],
    "sql": ["sql", "mysql", "postgresql"],
    "machine learning": ["machine learning"],
    "deep learning": ["deep learning"],
    "tensorflow": ["tensorflow"],
    "scikit-learn": ["scikit-learn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "nlp": ["nlp"],
    "git": ["git"],
    "html": ["html"],
    "css": ["css"],
    "javascript": ["javascript"],
    "docker": ["docker"],
    "dsa": ["dsa", "data structures", "algorithms"]
}


def topic_already_known(topic, user_skills):
    topic_lower = topic.lower().strip()

    if topic_lower in user_skills:
        return True

    aliases = TOPIC_ALIASES.get(
        topic_lower,
        []
    )

    return any(
        alias in user_skills
        for alias in aliases
    )


def generate_roadmap(user_skills, target_role):

    if target_role not in CAREER_ROLES:
        raise ValueError("Invalid career role")

    roadmap = ROADMAPS.get(target_role)

    if not roadmap:
        return {
            "target_role": target_role,
            "roadmap_duration": "0 months",
            "roadmap": []
        }

    user_skills = normalize_skills(
        user_skills
    )

    user_skills = set(user_skills)

    personalized_roadmap = []

    for phase in roadmap:

        recommended_topics = []

        for topic in phase["topics"]:

            if not topic_already_known(
                topic,
                user_skills
            ):
                recommended_topics.append(topic)

        personalized_roadmap.append(
            {
                "month": phase["month"],
                "focus": phase["focus"],
                "topics": phase["topics"],
                "recommended_topics": recommended_topics
            }
        )

    return {
        "target_role": target_role,
        "roadmap_duration": f"{len(roadmap)} months",
        "personalized": True,
        "roadmap": personalized_roadmap
    }
