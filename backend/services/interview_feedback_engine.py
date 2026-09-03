def calculate_interview_feedback(results, target_role):
    if not results:
        raise ValueError("No interview answers found")

    scores = [result.get("score", 0) for result in results]

    overall_score = round(sum(scores) / len(scores), 2)

    if overall_score >= 85:
        level = "Excellent"
    elif overall_score >= 70:
        level = "Good"
    elif overall_score >= 50:
        level = "Needs Improvement"
    else:
        level = "Beginner"

    strengths = []
    weaknesses = []

    for result in results:
        score = result.get("score", 0)
        topic = result.get("topic", "General")

        if score >= 80:
            strengths.append(
                f"Good understanding of {topic}"
            )
        elif score < 60:
            weaknesses.append(
                f"Needs improvement in {topic}"
            )

    strengths = list(dict.fromkeys(strengths))
    weaknesses = list(dict.fromkeys(weaknesses))

    recommendations = []

    if overall_score < 70:
        recommendations.append(
            "Revise core concepts related to the target role."
        )

    if weaknesses:
        recommendations.append(
            "Practice interview questions from your weak topics."
        )

    if overall_score >= 70:
        recommendations.append(
            "Continue practicing advanced role-specific interview questions."
        )

    recommendations.append(
        "Improve answer clarity by explaining concepts with examples."
    )

    return {
        "target_role": target_role,
        "overall_score": overall_score,
        "level": level,
        "total_questions": len(results),
        "question_scores": [
            {
                "question_number": index + 1,
                "score": result.get("score", 0),
                "feedback": result.get("feedback", ""),
                "topic": result.get("topic", "General")
            }
            for index, result in enumerate(results)
        ],
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }
