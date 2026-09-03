import { useState } from "react";
import api from "../api/api";

function MockInterview() {
  const [targetRole, setTargetRole] =
    useState("AI/ML Engineer");

  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [answers, setAnswers] = useState([]);
  const [feedback, setFeedback] = useState(null);

  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const [finished, setFinished] = useState(false);
  const [error, setError] = useState("");

  const startInterview = async () => {
    setLoading(true);
    setError("");
    setQuestions([]);
    setAnswers([]);
    setCurrentIndex(0);
    setAnswer("");
    setFeedback(null);
    setFinished(false);

    try {
      const response = await api.post(
        `/start-interview?target_role=${encodeURIComponent(
          targetRole
        )}&number_of_questions=5`
      );

      setQuestions(response.data.data.questions || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to start interview."
      );
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!answer.trim()) {
      setError("Please write your answer.");
      return;
    }

    const currentQuestion =
      questions[currentIndex];

    setEvaluating(true);
    setError("");

    try {
      const response = await api.post(
        "/evaluate-answer",
        null,
        {
          params: {
            question: currentQuestion.question,
            answer: answer,
          },
        }
      );

      const evaluation = response.data.data;

      const newAnswer = {
        question: currentQuestion.question,
        answer: answer,
        topic: currentQuestion.topic,
        difficulty: currentQuestion.difficulty,
        score: evaluation.score,
        feedback: evaluation.feedback,
      };

      const updatedAnswers = [
        ...answers,
        newAnswer,
      ];

      setAnswers(updatedAnswers);
      setFeedback(evaluation);

      if (currentIndex < questions.length - 1) {
        setTimeout(() => {
          setCurrentIndex((prev) => prev + 1);
          setAnswer("");
          setFeedback(null);
        }, 1000);
      } else {
        await getAIInterviewFeedback(updatedAnswers);
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to evaluate answer."
      );
    } finally {
      setEvaluating(false);
    }
  };

  const getAIInterviewFeedback = async (results) => {
    try {
      const response = await api.post(
        `/interview-feedback?target_role=${encodeURIComponent(
          targetRole
        )}`,
        results
      );

      setFeedback(response.data.data);
      setFinished(true);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to generate AI feedback."
      );
    }
  };

  if (finished && feedback) {
    return (
      <div className="page-container">

        <div className="page-intro">
          <span className="section-badge">AI FEEDBACK</span>
          <h2>Interview Results</h2>
          <p>Your AI-powered interview performance report.</p>
        </div>

        <section className="interview-result-card">

          <div className="interview-score">
            <strong>{feedback.results?.length
              ? Math.round(
                  feedback.results.reduce(
                    (sum, item) =>
                      sum + (item.ai_feedback?.score || 0),
                    0
                  ) / feedback.results.length
                )
              : 0}</strong>

            <span>Overall Score</span>
          </div>

          <h3>AI Interview Feedback</h3>

          <div className="ai-feedback-list">

            {(feedback.results || []).map(
              (item, index) => (
                <div
                  className="ai-feedback-card"
                  key={index}
                >

                  <span className="question-number">
                    Question {index + 1}
                  </span>

                  <h4>{item.question}</h4>

                  <div className="answer-box">
                    <span>Your Answer</span>
                    <p>{item.answer}</p>
                  </div>

                  {item.ai_feedback && (
                    <div className="ai-evaluation">

                      <div className="evaluation-scores">

                        <div>
                          <span>Score</span>
                          <strong>
                            {item.ai_feedback.score}
                          </strong>
                        </div>

                        <div>
                          <span>Accuracy</span>
                          <strong>
                            {item.ai_feedback.technical_accuracy}
                          </strong>
                        </div>

                        <div>
                          <span>Clarity</span>
                          <strong>
                            {item.ai_feedback.clarity}
                          </strong>
                        </div>

                        <div>
                          <span>Confidence</span>
                          <strong>
                            {item.ai_feedback.confidence}
                          </strong>
                        </div>

                      </div>

                      <div className="feedback-text">
                        <h5>AI Feedback</h5>
                        <p>
                          {item.ai_feedback.feedback}
                        </p>
                      </div>

                      {item.ai_feedback.strengths?.length > 0 && (
                        <div className="feedback-block">
                          <h5>Strengths</h5>

                          {item.ai_feedback.strengths.map(
                            (strength, i) => (
                              <p key={i}>
                                ✓ {strength}
                              </p>
                            )
                          )}
                        </div>
                      )}

                      {item.ai_feedback.weaknesses?.length > 0 && (
                        <div className="feedback-block">
                          <h5>Areas to Improve</h5>

                          {item.ai_feedback.weaknesses.map(
                            (weakness, i) => (
                              <p key={i}>
                                → {weakness}
                              </p>
                            )
                          )}
                        </div>
                      )}

                      {item.ai_feedback.better_answer && (
                        <div className="better-answer">
                          <h5>Better Answer</h5>
                          <p>
                            {item.ai_feedback.better_answer}
                          </p>
                        </div>
                      )}

                    </div>
                  )}

                </div>
              )
            )}

          </div>

          <button
            className="primary-btn"
            onClick={startInterview}
          >
            Start New Interview
          </button>

        </section>

      </div>
    );
  }

  return (
    <div className="page-container">

      <div className="page-intro">
        <span className="section-badge">GEMINI AI</span>
        <h2>AI Mock Interview</h2>
        <p>
          Practice technical interviews and receive AI feedback.
        </p>
      </div>

      {questions.length === 0 ? (
        <section className="interview-start-card">

          <div className="interview-icon">🎤</div>

          <h2>Ready for your interview?</h2>

          <p>
            You will receive 5 technical questions based on
            your selected role.
          </p>

          <div className="interview-role">

            <label>Target Role</label>

            <select
              value={targetRole}
              onChange={(e) =>
                setTargetRole(e.target.value)
              }
            >
              <option>AI/ML Engineer</option>
              <option>Backend Developer</option>
              <option>Full Stack Developer</option>
            </select>

          </div>

          {error && (
            <div className="error-box">
              ⚠ {error}
            </div>
          )}

          <button
            className="primary-btn"
            onClick={startInterview}
            disabled={loading}
          >
            {loading
              ? "Starting Interview..."
              : "Start Interview →"}
          </button>

        </section>
      ) : (
        <section className="interview-question-card">

          <div className="question-progress">

            <span>
              Question {currentIndex + 1} of{" "}
              {questions.length}
            </span>

            <div className="progress-bar">
              <div
                style={{
                  width: `${
                    ((currentIndex + 1) /
                      questions.length) *
                    100
                  }%`,
                }}
              ></div>
            </div>

          </div>

          <div className="question-meta">
            <span>{questions[currentIndex].topic}</span>
            <span>
              {questions[currentIndex].difficulty}
            </span>
          </div>

          <h2>
            {questions[currentIndex].question}
          </h2>

          <textarea
            value={answer}
            onChange={(e) =>
              setAnswer(e.target.value)
            }
            placeholder="Write your answer here..."
            rows={8}
          />

          {feedback && !finished && (
            <div className="basic-feedback">
              <strong>
                Score: {feedback.score}/100
              </strong>
              <p>{feedback.feedback}</p>
            </div>
          )}

          {error && (
            <div className="error-box">
              ⚠ {error}
            </div>
          )}

          <button
            className="primary-btn"
            onClick={submitAnswer}
            disabled={evaluating}
          >
            {evaluating
              ? "Evaluating..."
              : currentIndex === questions.length - 1
              ? "Finish Interview →"
              : "Submit Answer →"}
          </button>

        </section>
      )}

    </div>
  );
}

export default MockInterview;
