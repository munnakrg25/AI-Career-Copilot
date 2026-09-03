# 🚀 AI Career Copilot

> An AI-powered career guidance platform that helps students understand their skills, identify career opportunities, close skill gaps, build personalized learning roadmaps, assess job readiness, and practice mock interviews.

![AI Career Copilot](https://img.shields.io/badge/AI-Career%20Copilot-blue)
![React](https://img.shields.io/badge/Frontend-React%2019-61DAFB)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![Python](https://img.shields.io/badge/Python-3.x-3776AB)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4)
![IBM Bob](https://img.shields.io/badge/Development-IBM%20Bob-0F62FE)

---

## 📌 Project Overview

AI Career Copilot is an AI-powered career assistant designed primarily for students and early-career developers.

Many students have technical skills but struggle to understand:

- Which career path is suitable for them
- Which skills they are missing
- How prepared they are for a job
- What they should learn next
- How to improve their resume and GitHub profile
- How to prepare for technical interviews

AI Career Copilot brings these activities together into one personalized platform.

The application analyzes a student's resume and GitHub profile, identifies strengths and skill gaps, recommends career paths, generates a personalized roadmap, evaluates job readiness, and provides AI-powered mock interview practice.

---

# 🎯 Problem Statement

Students often find it difficult to identify the right career path and understand the skills required for their target jobs.

Traditional career guidance is often generic and does not consider the student's complete technical profile.

Students may have:

- Skills listed in their resume
- Projects and certifications
- GitHub repositories
- Internship or training experience

However, they often lack a unified system that analyzes this information and converts it into actionable career guidance.

AI Career Copilot addresses this problem by providing personalized, profile-based career recommendations and preparation guidance.

---

# 💡 Proposed Solution

AI Career Copilot uses AI and profile analysis to create a personalized career preparation experience.

The platform:

1. Analyzes the student's resume
2. Extracts skills and profile information
3. Analyzes public GitHub activity
4. Recommends suitable career paths
5. Identifies role-specific skill gaps
6. Generates a personalized learning roadmap
7. Calculates job-readiness insights
8. Provides AI-powered mock interviews
9. Generates feedback and improvement suggestions

This allows students to understand **where they are, where they want to go, and what they need to do next.**

---

# ✨ Key Features

## 📄 1. Resume Analysis

Students can upload their resume in PDF format.

The system extracts information such as:

- Name
- Email
- Education
- Technical skills
- Projects
- Experience
- Certifications

The extracted information is used throughout the career analysis workflow.

---

## 💼 2. Career Path Recommendations

The platform analyzes the student's profile and recommends suitable career paths.

Supported career directions include:

- AI/ML Engineer
- Backend Developer
- Frontend Developer
- Data Scientist
- Data Analyst
- Cybersecurity and other technology-oriented roles

The recommendations help students understand which roles match their current skills.

---

## 📊 3. Skill Gap Analysis

The system compares the student's current skills with the skills expected for the selected career role.

It identifies:

- Existing skills
- Missing skills
- Skills that should be improved
- Role-specific preparation areas

This gives students a clear direction for learning.

---

## 🗺️ 4. Personalized Career Roadmap

Based on the selected career role and current skills, AI Career Copilot generates a structured roadmap.

The roadmap helps students understand:

- What to learn
- Which skills to improve
- What projects to build
- What interview preparation to complete
- How to progress toward job readiness

---

## 🎯 5. Job Readiness Assessment

The platform provides a profile-based view of job readiness.

It considers areas such as:

- Technical skills
- Projects
- Experience
- Certifications
- GitHub activity
- Interview preparation

Students can use this assessment to identify areas requiring improvement.

---

## 💻 6. GitHub Analyzer

The application can analyze a public GitHub profile.

It provides insights into:

- Public repositories
- Repository activity
- Development profile
- Project visibility
- GitHub profile quality

GitHub API rate-limit handling is also implemented for improved reliability.

---

## 🎤 7. AI Mock Interview

Students can practice interviews based on their selected career role.

The system can:

- Generate role-specific interview questions
- Conduct mock interview sessions
- Analyze responses
- Generate feedback
- Suggest improvement areas

This helps students prepare for real technical interviews.

---

# 🔄 Application Workflow

```text
                    ┌─────────────────┐
                    │  Student Resume │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Resume Analysis │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Unified Profile │
                    └────────┬────────┘
                             ↓
              ┌──────────────┴──────────────┐
              ↓                             ↓
      ┌───────────────┐             ┌───────────────┐
      │ Career Paths  │             │ GitHub Analyzer│
      └───────┬───────┘             └───────┬───────┘
              │                             │
              └──────────────┬──────────────┘
                             ↓
                    ┌─────────────────┐
                    │ Skill Gap       │
                    │ Analysis        │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Career Roadmap  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Job Readiness   │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ AI Mock         │
                    │ Interview       │
                    └─────────────────┘
