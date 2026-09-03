import os
import json
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_career_advice_llm(parsed_data, github_data, target_role):
    """
    Call Gemini to generate personalised career advice.
    Returns a dict with the same keys as the rule-based fallback:
      target_role, career_summary, advice, strengths, improvements, next_steps
    Raises on any Gemini / JSON error so the caller can fall back gracefully.
    """
    skills = parsed_data.get("skills", [])
    projects = parsed_data.get("projects", [])
    experience = parsed_data.get("experience", [])
    certifications = parsed_data.get("certifications", [])

    # Build a compact GitHub summary only when data is available
    github_summary = ""
    if github_data:
        github_summary = (
            f"\nGitHub Profile:"
            f"\n  Total repositories: {github_data.get('total_repositories', 0)}"
            f"\n  Profile score: {github_data.get('profile_score', 0)}/100"
            f"\n  Languages used: {', '.join(github_data.get('languages', {}).keys()) or 'none'}"
        )

    prompt = f"""
You are an expert AI career advisor helping a candidate prepare for a job in the tech industry.

Target Role: {target_role}

Candidate Profile:
  Skills ({len(skills)}): {', '.join(skills) if skills else 'none listed'}
  Projects ({len(projects)}): {', '.join(p.get('name', '') for p in projects if p.get('name')) if projects else 'none listed'}
  Experience entries: {len(experience)}
  Certifications: {len(certifications)}{github_summary}

Give personalised, specific, actionable career advice for this candidate targeting {target_role}.

Return ONLY valid JSON with no markdown formatting:

{{
    "career_summary": "",
    "advice": [],
    "strengths": [],
    "improvements": [],
    "next_steps": []
}}

Rules:
- career_summary: 2-3 sentence personalised summary of their profile for this role.
- advice: list of 3-5 specific advice strings based on their actual skills and gaps.
- strengths: list of 2-4 specific strengths observed in their profile.
- improvements: list of 2-4 specific areas to improve with actionable suggestions.
- next_steps: list of 4-6 concrete next steps ordered by priority.
- Be specific to their actual skills, not generic.
- Do not repeat the same point across advice, strengths, improvements and next_steps.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    text = response.text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    data = json.loads(text)

    # Ensure all required keys exist with correct types
    result = {
        "target_role": target_role,
        "career_summary": str(data.get("career_summary", "")),
        "advice": data.get("advice", []) if isinstance(data.get("advice"), list) else [],
        "strengths": data.get("strengths", []) if isinstance(data.get("strengths"), list) else [],
        "improvements": data.get("improvements", []) if isinstance(data.get("improvements"), list) else [],
        "next_steps": data.get("next_steps", []) if isinstance(data.get("next_steps"), list) else [],
    }
    return result


def evaluate_interview_answer(question, answer, target_role):

    prompt = f"""
You are an expert technical interviewer.

Target Role: {target_role}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the candidate's answer.

Return ONLY valid JSON with no markdown formatting:

{{
    "score": 0,
    "technical_accuracy": 0,
    "clarity": 0,
    "confidence": 0,
    "feedback": "",
    "strengths": [],
    "weaknesses": [],
    "better_answer": ""
}}

Rules:
- score: 0 to 100
- technical_accuracy: 0 to 100
- clarity: 0 to 100
- confidence: 0 to 100
- Give specific feedback.
- Identify strengths and weaknesses.
- Give a concise ideal answer.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Strip markdown code fences if Gemini wraps the JSON
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

        return json.loads(text)

    except json.JSONDecodeError:
        return {
            "score": 0,
            "technical_accuracy": 0,
            "clarity": 0,
            "confidence": 0,
            "feedback": "Unable to parse AI feedback. Please try again.",
            "strengths": [],
            "weaknesses": [],
            "better_answer": ""
        }

    except Exception:
        return {
            "score": 0,
            "technical_accuracy": 0,
            "clarity": 0,
            "confidence": 0,
            "feedback": "AI evaluation is currently unavailable. Please try again later.",
            "strengths": [],
            "weaknesses": [],
            "better_answer": ""
        }
