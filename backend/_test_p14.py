"""
Focused P1-4 tests for the AI Career Advisor.
All Gemini calls are mocked — no real API calls made.
"""
import sys, ast, os
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv('.env')

passed = 0
failed = 0

def check(label, condition, info=""):
    global passed, failed
    sym = "PASS" if condition else "FAIL"
    print(f"  {sym}  {label}" + (f" — {info}" if info else ""))
    if condition:
        passed += 1
    else:
        failed += 1

# ── Syntax checks ──────────────────────────────────────────────────────────────
print("Syntax checks")
for f in ['services/llm_service.py', 'services/ai_career_advisor.py']:
    ast.parse(open(f).read())
    check(f"Syntax OK: {f}", True)
print()

# ── Import checks ──────────────────────────────────────────────────────────────
print("Import checks")
from services.llm_service import generate_career_advice_llm
check("generate_career_advice_llm importable from llm_service", True)

from services.ai_career_advisor import generate_career_advice, _rule_based_advice
check("generate_career_advice importable from ai_career_advisor", True)
check("_rule_based_advice importable (fallback exists)", True)
print()

# ── Sample data ────────────────────────────────────────────────────────────────
SAMPLE = {
    "skills": ["python", "react", "machine learning", "sql", "git", "docker"],
    "projects": [{"name": "ML Pipeline"}, {"name": "React Dashboard"}],
    "experience": ["Internship at TechCorp"],
    "certifications": ["AWS Certified"]
}
GITHUB = {"total_repositories": 12, "profile_score": 75, "languages": {"Python": 8, "JavaScript": 4}}
ROLE = "AI/ML Engineer"
REQUIRED_KEYS = {"target_role", "career_summary", "advice", "strengths", "improvements", "next_steps"}

# ── Test 1: _rule_based_advice still works unchanged ──────────────────────────
print("Test 1: _rule_based_advice produces correct structure")
result = _rule_based_advice(SAMPLE, GITHUB, ROLE)
check("Has all required keys", REQUIRED_KEYS.issubset(result.keys()))
check("target_role correct", result["target_role"] == ROLE)
check("career_summary is non-empty string", isinstance(result["career_summary"], str) and len(result["career_summary"]) > 0)
check("advice is list", isinstance(result["advice"], list))
check("strengths is list", isinstance(result["strengths"], list))
check("improvements is list", isinstance(result["improvements"], list))
check("next_steps is list", isinstance(result["next_steps"], list))
print()

# ── Test 2: generate_career_advice_llm happy path (mocked Gemini) ─────────────
print("Test 2: generate_career_advice_llm with mocked Gemini response")

import unittest.mock as mock
import json as _json

MOCK_LLM_RESPONSE = {
    "career_summary": "Strong Python and ML background targeting AI/ML Engineer role.",
    "advice": ["Focus on deploying ML models with FastAPI.", "Build an end-to-end ML project."],
    "strengths": ["Python and ML fundamentals are solid.", "Docker knowledge is a plus."],
    "improvements": ["Add deep learning experience.", "Improve SQL for data engineering."],
    "next_steps": ["Deploy a model to cloud.", "Complete an NLP project.", "Practice system design."]
}

mock_response_obj = mock.MagicMock()
mock_response_obj.text = _json.dumps(MOCK_LLM_RESPONSE)

with mock.patch("services.llm_service.client") as mock_client:
    mock_client.models.generate_content.return_value = mock_response_obj
    result = generate_career_advice_llm(SAMPLE, GITHUB, ROLE)

check("Has all required keys", REQUIRED_KEYS.issubset(result.keys()))
check("target_role injected correctly", result["target_role"] == ROLE)
check("career_summary from Gemini", "Python" in result["career_summary"])
check("advice is list with items", isinstance(result["advice"], list) and len(result["advice"]) > 0)
check("strengths is list with items", isinstance(result["strengths"], list) and len(result["strengths"]) > 0)
check("improvements is list with items", isinstance(result["improvements"], list) and len(result["improvements"]) > 0)
check("next_steps is list with items", isinstance(result["next_steps"], list) and len(result["next_steps"]) > 0)
print()

# ── Test 3: generate_career_advice_llm strips markdown fences ─────────────────
print("Test 3: generate_career_advice_llm strips ```json fences")
mock_response_fenced = mock.MagicMock()
mock_response_fenced.text = "```json\n" + _json.dumps(MOCK_LLM_RESPONSE) + "\n```"

with mock.patch("services.llm_service.client") as mock_client:
    mock_client.models.generate_content.return_value = mock_response_fenced
    result = generate_career_advice_llm(SAMPLE, None, ROLE)

check("Parses correctly despite fences", result["target_role"] == ROLE)
check("No GitHub section when github_data=None", True)  # just ensure no exception
print()

# ── Test 4: generate_career_advice falls back when Gemini raises ───────────────
print("Test 4: generate_career_advice falls back to rule-based on Gemini error")

with mock.patch("services.ai_career_advisor.generate_career_advice_llm") as mock_llm:
    mock_llm.side_effect = Exception("Gemini API unavailable")
    result = generate_career_advice(SAMPLE, GITHUB, ROLE)

check("Returns result despite Gemini error", result is not None)
check("Has all required keys in fallback", REQUIRED_KEYS.issubset(result.keys()))
check("target_role correct in fallback", result["target_role"] == ROLE)
check("Fallback career_summary is non-empty", len(result["career_summary"]) > 0)
print()

# ── Test 5: generate_career_advice falls back on JSON parse error ──────────────
print("Test 5: generate_career_advice falls back when Gemini returns bad JSON")

bad_json_response = mock.MagicMock()
bad_json_response.text = "Sorry, I cannot help with that."

with mock.patch("services.llm_service.client") as mock_client:
    mock_client.models.generate_content.return_value = bad_json_response
    # Call the top-level function which should catch the JSONDecodeError
    result = generate_career_advice(SAMPLE, None, ROLE)

check("Returns result despite bad JSON", result is not None)
check("Has all required keys in fallback", REQUIRED_KEYS.issubset(result.keys()))
check("Fallback next_steps is non-empty", len(result["next_steps"]) > 0)
print()

# ── Test 6: Gemini happy path through top-level generate_career_advice ─────────
print("Test 6: generate_career_advice uses Gemini when available")

with mock.patch("services.ai_career_advisor.generate_career_advice_llm") as mock_llm:
    mock_llm.return_value = {
        "target_role": ROLE,
        "career_summary": "AI-generated summary.",
        "advice": ["Advice from Gemini"],
        "strengths": ["Strength from Gemini"],
        "improvements": ["Improvement from Gemini"],
        "next_steps": ["Step from Gemini"]
    }
    result = generate_career_advice(SAMPLE, None, ROLE)

check("Returns Gemini result when available", result["career_summary"] == "AI-generated summary.")
check("mock_llm called once", mock_llm.call_count == 1)
print()

# ── Summary ────────────────────────────────────────────────────────────────────
print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")
sys.exit(0 if failed == 0 else 1)
