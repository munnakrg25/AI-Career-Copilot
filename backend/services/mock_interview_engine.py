import random

INTERVIEW_QUESTIONS = {
    "AI/ML Engineer": [
        {
            "question": "What is overfitting in Machine Learning?",
            "topic": "Machine Learning",
            "difficulty": "Easy",
            "keywords": ["training", "test", "generalization", "complexity"]
        },
        {
            "question": "What is the difference between supervised and unsupervised learning?",
            "topic": "Machine Learning",
            "difficulty": "Easy",
            "keywords": ["labeled", "unlabeled", "classification", "clustering"]
        },
        {
            "question": "What is the purpose of feature scaling?",
            "topic": "Machine Learning",
            "difficulty": "Medium",
            "keywords": ["scale", "normalization", "standardization", "features"]
        },
        {
            "question": "What is the difference between CNN and RNN?",
            "topic": "Deep Learning",
            "difficulty": "Medium",
            "keywords": ["cnn", "image", "rnn", "sequence"]
        },
        {
            "question": "What is an activation function?",
            "topic": "Deep Learning",
            "difficulty": "Easy",
            "keywords": ["neural", "nonlinear", "relu", "sigmoid"]
        },
        {
            "question": "What is the difference between precision and recall?",
            "topic": "Machine Learning",
            "difficulty": "Medium",
            "keywords": ["precision", "recall", "false positive", "false negative"]
        },
        {
            "question": "What is NLP?",
            "topic": "NLP",
            "difficulty": "Easy",
            "keywords": ["natural language", "text", "language", "processing"]
        },
        {
            "question": "What is the purpose of train-test split?",
            "topic": "Machine Learning",
            "difficulty": "Easy",
            "keywords": ["training", "testing", "evaluation", "data"]
        },
        {
            "question": "What is gradient descent?",
            "topic": "Machine Learning",
            "difficulty": "Medium",
            "keywords": ["loss", "gradient", "learning rate", "optimization"]
        },
        {
            "question": "What is the difference between TensorFlow and Scikit-learn?",
            "topic": "Tools",
            "difficulty": "Medium",
            "keywords": ["tensorflow", "scikit", "deep learning", "machine learning"]
        }
    ],

    "Backend Developer": [
        {
            "question": "What is a REST API?",
            "topic": "Backend",
            "difficulty": "Easy",
            "keywords": ["http", "api", "client", "server"]
        },
        {
            "question": "What is JWT authentication?",
            "topic": "Authentication",
            "difficulty": "Medium",
            "keywords": ["token", "authentication", "jwt", "authorization"]
        },
        {
            "question": "What is database indexing?",
            "topic": "Database",
            "difficulty": "Medium",
            "keywords": ["index", "query", "search", "performance"]
        },
        {
            "question": "What is the difference between SQL and NoSQL?",
            "topic": "Database",
            "difficulty": "Easy",
            "keywords": ["relational", "non relational", "schema", "document"]
        },
        {
            "question": "What is middleware in FastAPI or web applications?",
            "topic": "Backend",
            "difficulty": "Medium",
            "keywords": ["request", "response", "middleware"]
        }
    ],

    "Full Stack Developer": [
        {
            "question": "What is the difference between frontend and backend?",
            "topic": "Web Development",
            "difficulty": "Easy",
            "keywords": ["frontend", "backend", "client", "server"]
        },
        {
            "question": "What is React?",
            "topic": "React",
            "difficulty": "Easy",
            "keywords": ["javascript", "library", "component", "ui"]
        },
        {
            "question": "What is REST API?",
            "topic": "Backend",
            "difficulty": "Easy",
            "keywords": ["api", "http", "client", "server"]
        },
        {
            "question": "What is JWT?",
            "topic": "Authentication",
            "difficulty": "Medium",
            "keywords": ["token", "authentication", "authorization"]
        },
        {
            "question": "What is PostgreSQL?",
            "topic": "Database",
            "difficulty": "Easy",
            "keywords": ["database", "sql", "relational", "postgresql"]
        }
    ],

    "Frontend Developer": [
        {
            "question": "What is the difference between HTML, CSS, and JavaScript?",
            "topic": "Web Fundamentals",
            "difficulty": "Easy",
            "keywords": ["html", "structure", "css", "style", "javascript", "behaviour"]
        },
        {
            "question": "What is the Virtual DOM in React?",
            "topic": "React",
            "difficulty": "Medium",
            "keywords": ["virtual", "dom", "reconciliation", "rendering", "performance"]
        },
        {
            "question": "What is the difference between useState and useEffect in React?",
            "topic": "React",
            "difficulty": "Medium",
            "keywords": ["state", "effect", "hook", "render", "side effect"]
        },
        {
            "question": "What is CSS Flexbox?",
            "topic": "CSS",
            "difficulty": "Easy",
            "keywords": ["flex", "container", "align", "justify", "layout"]
        },
        {
            "question": "What is responsive web design?",
            "topic": "CSS",
            "difficulty": "Easy",
            "keywords": ["responsive", "media query", "mobile", "breakpoint", "viewport"]
        },
        {
            "question": "What is the difference between let, const, and var in JavaScript?",
            "topic": "JavaScript",
            "difficulty": "Easy",
            "keywords": ["let", "const", "var", "scope", "hoisting"]
        },
        {
            "question": "What is an event listener in JavaScript?",
            "topic": "JavaScript",
            "difficulty": "Easy",
            "keywords": ["event", "listener", "click", "callback", "dom"]
        },
        {
            "question": "What is prop drilling in React and how do you avoid it?",
            "topic": "React",
            "difficulty": "Medium",
            "keywords": ["props", "drilling", "context", "state management", "redux"]
        }
    ],

    "Data Scientist": [
        {
            "question": "What is the difference between supervised and unsupervised learning?",
            "topic": "Machine Learning",
            "difficulty": "Easy",
            "keywords": ["labeled", "unlabeled", "classification", "clustering"]
        },
        {
            "question": "What is cross-validation and why is it used?",
            "topic": "Machine Learning",
            "difficulty": "Medium",
            "keywords": ["cross validation", "overfitting", "generalisation", "fold", "evaluation"]
        },
        {
            "question": "What is the difference between correlation and causation?",
            "topic": "Statistics",
            "difficulty": "Easy",
            "keywords": ["correlation", "causation", "relationship", "variable"]
        },
        {
            "question": "What is a confusion matrix?",
            "topic": "Machine Learning",
            "difficulty": "Medium",
            "keywords": ["true positive", "false positive", "precision", "recall", "accuracy"]
        },
        {
            "question": "What is feature engineering?",
            "topic": "Data Science",
            "difficulty": "Medium",
            "keywords": ["feature", "transformation", "encoding", "selection", "model"]
        },
        {
            "question": "What is the purpose of Pandas in data science?",
            "topic": "Tools",
            "difficulty": "Easy",
            "keywords": ["pandas", "dataframe", "data manipulation", "cleaning", "analysis"]
        },
        {
            "question": "What is the difference between mean, median, and mode?",
            "topic": "Statistics",
            "difficulty": "Easy",
            "keywords": ["mean", "median", "mode", "average", "distribution"]
        },
        {
            "question": "What is regularisation in machine learning?",
            "topic": "Machine Learning",
            "difficulty": "Medium",
            "keywords": ["regularisation", "overfitting", "lasso", "ridge", "penalty"]
        }
    ],

    "Data Analyst": [
        {
            "question": "What is the difference between INNER JOIN and LEFT JOIN in SQL?",
            "topic": "SQL",
            "difficulty": "Medium",
            "keywords": ["inner join", "left join", "matching", "null", "rows"]
        },
        {
            "question": "What is a pivot table?",
            "topic": "Excel",
            "difficulty": "Easy",
            "keywords": ["pivot", "summarise", "aggregate", "rows", "columns"]
        },
        {
            "question": "What is data cleaning and why is it important?",
            "topic": "Data Analysis",
            "difficulty": "Easy",
            "keywords": ["missing", "duplicate", "outlier", "quality", "accuracy"]
        },
        {
            "question": "What is the difference between OLTP and OLAP?",
            "topic": "Database",
            "difficulty": "Medium",
            "keywords": ["oltp", "olap", "transactional", "analytical", "reporting"]
        },
        {
            "question": "What is a GROUP BY clause in SQL?",
            "topic": "SQL",
            "difficulty": "Easy",
            "keywords": ["group by", "aggregate", "sum", "count", "having"]
        },
        {
            "question": "What is the purpose of data visualisation?",
            "topic": "Data Analysis",
            "difficulty": "Easy",
            "keywords": ["visualisation", "chart", "trend", "insight", "decision"]
        },
        {
            "question": "What is an outlier and how do you handle it?",
            "topic": "Statistics",
            "difficulty": "Medium",
            "keywords": ["outlier", "detection", "remove", "transform", "iqr"]
        },
        {
            "question": "What is Power BI used for?",
            "topic": "Tools",
            "difficulty": "Easy",
            "keywords": ["power bi", "dashboard", "report", "visualisation", "microsoft"]
        }
    ]
}


def start_mock_interview(target_role, number_of_questions=5):
    if target_role not in INTERVIEW_QUESTIONS:
        raise ValueError("Invalid career role")

    questions = INTERVIEW_QUESTIONS[target_role]

    number_of_questions = min(
        number_of_questions,
        len(questions)
    )

    selected_questions = random.sample(
        questions,
        number_of_questions
    )

    return {
        "target_role": target_role,
        "total_questions": number_of_questions,
        "current_question": 1,
        "questions": [
            {
                "question_id": index + 1,
                "question": item["question"],
                "topic": item["topic"],
                "difficulty": item["difficulty"]
            }
            for index, item in enumerate(selected_questions)
        ]
    }


def evaluate_answer(answer, question):
    answer = answer.lower().strip()

    if not answer:
        return {
            "score": 0,
            "feedback": "No answer provided."
        }

    keywords = question.get("keywords", [])

    matched_keywords = [
        keyword
        for keyword in keywords
        if keyword.lower() in answer
    ]

    if len(matched_keywords) >= 3:
        score = 90
    elif len(matched_keywords) == 2:
        score = 75
    elif len(matched_keywords) == 1:
        score = 55
    else:
        score = 30

    if score >= 80:
        feedback = "Strong answer. You covered the important concepts."
    elif score >= 60:
        feedback = "Good answer, but you can explain the concept in more detail."
    else:
        feedback = "Your answer needs improvement. Revise the core concept."

    return {
        "score": score,
        "feedback": feedback,
        "matched_keywords": matched_keywords
    }
