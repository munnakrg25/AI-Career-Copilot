from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from database.database import engine, Base, SessionLocal
from models.user import User
from schemas.user import UserCreate, UserLogin
from utils.security import hash_password, verify_password, create_access_token
from utils.file_validation import validate_and_save_resume

import os
import shutil

from services.resume_parser import extract_text_from_pdf
from services.resume_parser_engine import parse_resume
from services.career_engine import recommend_careers
from services.skill_gap_engine import analyze_skill_gap
from services.roadmap_engine import generate_roadmap
from services.job_readiness_engine import calculate_job_readiness
from services.github_analyzer import analyze_github
from services.github_repository_analyzer import get_repository_analysis
from services.unified_profile_engine import generate_unified_profile

from services.mock_interview_engine import (
    start_mock_interview,
    evaluate_answer,
    INTERVIEW_QUESTIONS
)

from services.interview_feedback_engine import calculate_interview_feedback
from services.llm_service import evaluate_interview_answer


app = FastAPI(
    title="AI Career Copilot",
    description="AI-powered career guidance and interview preparation platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# DATABASE
# =========================

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================
# BASIC ROUTES
# =========================

@app.get("/")
def root():
    return {
        "message": "AI Career Copilot API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================
# AUTHENTICATION
# =========================

@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": str(existing_user.id),
            "email": existing_user.email
        }
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# RESUME UPLOAD
# =========================

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):
    try:
        file_path = await validate_and_save_resume(file, "uploads")

        return {
            "message": "Resume uploaded successfully",
            "filename": os.path.basename(file_path)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# PARSE RESUME
# =========================

@app.post("/parse-resume")
async def parse_resume_endpoint(
    file: UploadFile = File(...)
):
    try:
        file_path = await validate_and_save_resume(file, "uploads")

        resume_text = extract_text_from_pdf(file_path)
        parsed_data = parse_resume(resume_text)

        return {
            "message": "Resume parsed successfully",
            "data": parsed_data
        }

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# CAREER RECOMMENDATION
# =========================

@app.post("/career-recommendation")
async def career_recommendation(
    file: UploadFile = File(...)
):
    try:
        file_path = await validate_and_save_resume(file, "uploads")

        resume_text = extract_text_from_pdf(file_path)
        parsed_data = parse_resume(resume_text)
        recommendations = recommend_careers(parsed_data.get("skills", []))

        return {
            "message": "Career recommendations generated successfully",
            "data": recommendations
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# SKILL GAP
# =========================

@app.get("/skill-gap-by-skills")
async def skill_gap_by_skills(
    target_role: str = "AI/ML Engineer",
    skills: str = ""
):
    try:
        skill_list = [s.strip() for s in skills.split(",") if s.strip()]
        result = analyze_skill_gap(skill_list, target_role)
        return {
            "message": "Skill gap analysis generated successfully",
            "data": result
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/skill-gap")
async def skill_gap(
    file: UploadFile = File(...),
    target_role: str = "AI/ML Engineer"
):
    try:
        file_path = await validate_and_save_resume(file, "uploads")

        resume_text = extract_text_from_pdf(file_path)
        parsed_data = parse_resume(resume_text)
        result = analyze_skill_gap(parsed_data.get("skills", []), target_role)

        return {
            "message": "Skill gap analysis generated successfully",
            "data": result
        }

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# ROADMAP
# =========================

@app.get("/roadmap-by-skills")
async def roadmap_by_skills(
    target_role: str = "AI/ML Engineer",
    skills: str = ""
):
    try:
        skill_list = [s.strip() for s in skills.split(",") if s.strip()]
        result = generate_roadmap(skill_list, target_role)
        return {
            "message": "Personalized roadmap generated successfully",
            "data": result
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/roadmap")
async def roadmap(
    file: UploadFile = File(...),
    target_role: str = "AI/ML Engineer"
):
    try:
        file_path = await validate_and_save_resume(file, "uploads")

        resume_text = extract_text_from_pdf(file_path)
        parsed_data = parse_resume(resume_text)
        result = generate_roadmap(parsed_data.get("skills", []), target_role)

        return {
            "message": "Personalized roadmap generated successfully",
            "data": result
        }

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# JOB READINESS
# =========================

@app.post("/job-readiness")
async def job_readiness(
    file: UploadFile = File(...),
    target_role: str = "AI/ML Engineer"
):
    try:
        file_path = await validate_and_save_resume(file, "uploads")

        resume_text = extract_text_from_pdf(file_path)
        parsed_data = parse_resume(resume_text)
        result = calculate_job_readiness(parsed_data, target_role, None)

        return {
            "message": "Job readiness analysis generated successfully",
            "data": result
        }

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# GITHUB ANALYSIS
# =========================

@app.post("/github-analysis")
async def github_analysis(
    username: str
):
    try:
        result = await analyze_github(
            username
        )

        return {
            "message": "GitHub profile analyzed successfully",
            "data": result
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# GITHUB REPOSITORY ANALYSIS
# =========================

@app.post("/github-repository-analysis")
async def github_repository_analysis(
    username: str,
    repo_name: str
):
    try:
        result = await get_repository_analysis(
            username,
            repo_name
        )

        return {
            "message": "GitHub repository analyzed successfully",
            "data": result
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# UNIFIED PROFILE
# =========================

@app.post("/unified-profile")
async def unified_profile(
    file: UploadFile = File(...),
    target_role: str = "AI/ML Engineer",
    github_username: str | None = None
):
    try:
        file_path = await validate_and_save_resume(file, "uploads")

        resume_text = extract_text_from_pdf(file_path)
        parsed_data = parse_resume(resume_text)

        github_data = None
        if github_username:
            github_data = await analyze_github(github_username)

        result = await generate_unified_profile(
            parsed_data,
            target_role,
            github_data
        )

        return {
            "message": "Unified career profile generated successfully",
            "data": result
        }

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# MOCK INTERVIEW
# =========================

@app.post("/start-interview")
async def start_interview(
    target_role: str = "AI/ML Engineer",
    number_of_questions: int = 5
):
    try:
        result = start_mock_interview(
            target_role,
            number_of_questions
        )

        return {
            "message": "Mock interview started successfully",
            "data": result
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================
# BASIC INTERVIEW ANSWER
# =========================

@app.post("/evaluate-answer")
async def evaluate_interview_answer_endpoint(
    question: str,
    answer: str
):
    try:
        question_data = None

        for questions in INTERVIEW_QUESTIONS.values():
            for item in questions:
                if item["question"] == question:
                    question_data = item
                    break

            if question_data:
                break

        if not question_data:
            raise HTTPException(
                status_code=404,
                detail="Question not found"
            )

        result = evaluate_answer(
            answer,
            question_data
        )

        return {
            "message": "Answer evaluated successfully",
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# OLD INTERVIEW FEEDBACK
# =========================

@app.post("/interview-feedback-basic")
async def interview_feedback_basic(
    target_role: str,
    results: list[dict]
):
    try:
        feedback = calculate_interview_feedback(
            results,
            target_role
        )

        return {
            "message": "Interview feedback generated successfully",
            "data": feedback
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# REAL AI INTERVIEW FEEDBACK
# =========================

@app.post("/interview-feedback")
async def interview_feedback(
    target_role: str,
    results: list[dict]
):
    try:
        processed_results = []

        for result in results:

            question = result.get(
                "question",
                ""
            )

            answer = result.get(
                "answer",
                ""
            )

            if not question or not answer:
                continue

            ai_response = evaluate_interview_answer(
                question,
                answer,
                target_role
            )

            processed_results.append({
                "question": question,
                "answer": answer,
                "ai_feedback": ai_response
            })

        return {
            "message": "AI interview feedback generated successfully",
            "data": {
                "target_role": target_role,
                "total_questions": len(processed_results),
                "results": processed_results
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
