import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { quizAPI } from "../api";

interface Question {
  id: number;
  concept: number;
  text: string;
  code_snippet?: string;
  difficulty: "easy" | "medium" | "hard";
  remedial_resource?: string;
  options: { id: string; text: string }[];
}

interface QuizResult {
  questionText: string;
  isCorrect: boolean;
  userAnswer: string;
  explanation: string;
  remedialLink?: string;
}

const Quiz: React.FC = () => {
  const [question, setQuestion] = useState<Question | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [feedback, setFeedback] = useState<{
    msg: string;
    isCorrect: boolean;
  } | null>(null);
  const [quizHistory, setQuizHistory] = useState<QuizResult[]>([]);
  const [showSummary, setShowSummary] = useState(false);

  const conceptIdRef = useRef<number | null>(null);
  const navigate = useNavigate();

  // Ανάκτηση του ID από το LocalStorage (το βάζουμε εκεί όταν πατάμε στο Dashboard)
  useEffect(() => {
    const storedId = localStorage.getItem("currentConceptId");
    if (storedId) {
      conceptIdRef.current = parseInt(storedId);
    }
  }, []);

  const fetchNextQuestion = async () => {
    setLoading(true);
    setIsAnswered(false);
    setFeedback(null);
    setSelectedOption(null);

    try {
      // Στέλνουμε το ID αν το έχουμε, για να πάρουμε ερώτηση για ΤΟ ΣΥΓΚΕΚΡΙΜΕΝΟ μάθημα
      const res = await quizAPI.getNextQuestion(conceptIdRef.current);

      if (res.data.message === "Course completed!" || !res.data.options) {
        // Αν δεν είχαμε το ID πριν (π.χ. Adaptive mode), το παίρνουμε τώρα από το backend
        if (res.data.concept) {
          conceptIdRef.current = res.data.concept;
          localStorage.setItem("currentConceptId", res.data.concept); // Το σώζουμε για το Restart
        }

        // Φορτώνουμε το ιστορικό
        if (conceptIdRef.current) {
          await loadHistory(conceptIdRef.current);
        } else {
          setShowSummary(true);
        }
      } else {
        setQuestion(res.data);
        conceptIdRef.current = res.data.concept;
        localStorage.setItem("currentConceptId", res.data.concept.toString());
      }
    } catch (err) {
      console.error("Error fetching question", err);
      // navigate('/dashboard'); // Προσωρινά σχόλιο για debugging
    } finally {
      setLoading(false);
    }
  };

  const loadHistory = async (id: number) => {
    try {
      const res = await quizAPI.getHistory(id);
      setQuizHistory(res.data);
      setShowSummary(true);
    } catch (err) {
      console.error("Could not load history", err);
    }
  };

  useEffect(() => {
    // Καλούμε το fetch μόλις φορτώσει το component
    fetchNextQuestion();
  }, []);

  const handleSubmit = async () => {
    if (!question || !selectedOption) return;
    try {
      const res = await quizAPI.submitAnswer(question.id, selectedOption);
      setIsAnswered(true);
      const isCorrect = res.data.correct;
      const explanation = res.data.explanation || "";

      setFeedback({
        msg: isCorrect
          ? "✅ Σωστά! " + explanation
          : "❌ Λάθος. " + explanation,
        isCorrect,
      });

      // Προσθέτουμε στο προσωρινό ιστορικό (για άμεση εμφάνιση)
      setQuizHistory((prev) => [
        ...prev,
        {
          questionText: question.text,
          isCorrect: isCorrect,
          userAnswer: selectedOption,
          explanation: explanation,
          remedialLink: question.remedial_resource,
        },
      ]);
    } catch (err) {
      console.error("Error submitting answer", err);
    }
  };

  const handleRestart = async () => {
    const id = conceptIdRef.current;
    if (!id) {
      alert("Δεν βρέθηκε ID μαθήματος.");
      return;
    }

    if (window.confirm("Θέλεις να παίξεις ξανά; Το ιστορικό θα διαγραφεί.")) {
      setLoading(true);
      try {
        await quizAPI.restartConcept(id);
        setQuizHistory([]);
        setShowSummary(false);
        setQuestion(null);

        // Μικρή καθυστέρηση και ξανακαλούμε ερώτηση (τώρα θα είναι mastery=0)
        setTimeout(() => fetchNextQuestion(), 500);
      } catch (error) {
        alert("Σφάλμα επανεκκίνησης.");
        setLoading(false);
      }
    }
  };

  // --- RENDER ---
  const renderDifficultyBadge = (difficulty: string) => {
    const colors: any = { easy: "#4caf50", medium: "#ff9800", hard: "#f44336" };
    return (
      <span
        style={{
          backgroundColor: colors[difficulty],
          color: "white",
          padding: "4px 8px",
          borderRadius: "12px",
          fontSize: "0.75rem",
          marginLeft: "10px",
        }}
      >
        {difficulty}
      </span>
    );
  };

  if (showSummary) {
    const total = quizHistory.length;
    const correct = quizHistory.filter((r) => r.isCorrect).length;
    const score = total > 0 ? Math.round((correct / total) * 100) : 0;

    return (
      <div style={styles.container}>
        <div style={{ ...styles.card, maxWidth: "800px" }}>
          <h2 style={{ textAlign: "center", color: "#333" }}>
            {total > 0 ? "🎉 Τέλος Ενότητας!" : "🏁 Ενότητα Ολοκληρωμένη"}
          </h2>

          {total > 0 && (
            <div
              style={{
                textAlign: "center",
                margin: "20px 0",
                padding: "20px",
                backgroundColor: "#e3f2fd",
                borderRadius: "10px",
              }}
            >
              <h1 style={{ margin: 0, color: "#1976d2" }}>{score}%</h1>
              <p>
                Σωστά: {correct} / {total}
              </p>
            </div>
          )}

          <h3>📜 Ιστορικό:</h3>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "15px",
              marginTop: "15px",
            }}
          >
            {quizHistory.length > 0 ? (
              quizHistory.map((result, index) => (
                <div
                  key={index}
                  style={{
                    padding: "15px",
                    borderLeft: result.isCorrect
                      ? "5px solid #4caf50"
                      : "5px solid #f44336",
                    backgroundColor: "#fff",
                    boxShadow: "0 2px 5px rgba(0,0,0,0.05)",
                  }}
                >
                  <div style={{ fontWeight: "bold" }}>
                    {index + 1}. {result.questionText}
                  </div>
                  <div
                    style={{ color: result.isCorrect ? "#2e7d32" : "#c62828" }}
                  >
                    {result.isCorrect
                      ? "✅ Σωστό"
                      : `❌ Λάθος (Επέλεξες: ${result.userAnswer})`}
                  </div>
                  <div style={{ marginTop: "10px" }}>
                    {result.isCorrect ? (
                      " "
                    ) : (
                      <a
                        href={result.remedialLink}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          display: "inline-block",
                          backgroundColor: "#fff3e0",
                          color: "#e65100",
                          padding: "8px 12px",
                          borderRadius: "5px",
                          textDecoration: "none",
                          fontWeight: "bold",
                          fontSize: "0.9rem",
                          border: "1px solid #ffcc80",
                        }}
                      >
                        📖 Διάβασε τη θεωρία
                      </a>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <p>Δεν βρέθηκε ιστορικό.</p>
            )}
          </div>

          <div
            style={{
              display: "flex",
              gap: "10px",
              marginTop: "30px",
              justifyContent: "center",
            }}
          >
            <button
              onClick={() => navigate("/dashboard")}
              style={{
                ...styles.mainBtn,
                backgroundColor: "#555",
                width: "auto",
              }}
            >
              🏠 Dashboard
            </button>
            <button
              onClick={handleRestart}
              style={{
                ...styles.mainBtn,
                backgroundColor: "#ff9800",
                width: "auto",
              }}
            >
              🔄 Παίξε Ξανά
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (loading) return <div style={styles.center}>🔄 Φόρτωση...</div>;
  if (!question) return <div style={styles.center}>...</div>;

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <button onClick={() => navigate("/dashboard")} style={styles.backBtn}>
            ⬅ Έξοδος
          </button>
          <div>
            <span style={{ color: "#888" }}>Επίπεδο:</span>
            {renderDifficultyBadge(question.difficulty)}
          </div>
        </div>
        <h3 style={{ marginBottom: "20px" }}>{question.text}</h3>
        {question.code_snippet && (
          <div style={styles.codeBlock}>
            <pre>{question.code_snippet}</pre>
          </div>
        )}

        <div style={styles.optionsGrid}>
          {question.options &&
            question.options.map((opt) => (
              <button
                key={opt.id}
                onClick={() => !isAnswered && setSelectedOption(opt.id)}
                disabled={isAnswered}
                style={{
                  ...styles.optionBtn,
                  backgroundColor:
                    selectedOption === opt.id ? "#e3f2fd" : "white",
                  borderColor: selectedOption === opt.id ? "#2196f3" : "#ddd",
                }}
              >
                <span style={{ fontWeight: "bold", marginRight: "10px" }}>
                  {opt.id}.
                </span>{" "}
                {opt.text}
              </button>
            ))}
        </div>

        {feedback && (
          <div
            style={{
              ...styles.feedback,
              backgroundColor: feedback.isCorrect ? "#e8f5e9" : "#ffebee",
            }}
          >
            {feedback.msg}
          </div>
        )}

        {!isAnswered ? (
          <button
            onClick={handleSubmit}
            disabled={!selectedOption}
            style={styles.mainBtn}
          >
            Έλεγχος
          </button>
        ) : (
          <button
            onClick={fetchNextQuestion}
            style={{ ...styles.mainBtn, backgroundColor: "#4caf50" }}
          >
            Επόμενο ➡
          </button>
        )}
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
    backgroundColor: "#f4f6f8",
    padding: "20px",
  },
  card: {
    width: "100%",
    maxWidth: "600px",
    backgroundColor: "white",
    padding: "40px",
    borderRadius: "16px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.05)",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "25px",
    borderBottom: "1px solid #eee",
    paddingBottom: "15px",
  },
  center: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    fontSize: "1.2rem",
    color: "#666",
  },
  backBtn: {
    background: "none",
    border: "none",
    cursor: "pointer",
    color: "#666",
    fontSize: "0.95rem",
    padding: 0,
    fontWeight: 500,
  },
  codeBlock: {
    marginBottom: "25px",
    borderRadius: "8px",
    overflow: "hidden",
    border: "1px solid #ccc",
    backgroundColor: "#f5f5f5",
    padding: "15px",
  },
  optionsGrid: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
    marginBottom: "25px",
  },
  optionBtn: {
    padding: "16px",
    border: "2px solid #ddd",
    borderRadius: "10px",
    cursor: "pointer",
    fontSize: "1rem",
    textAlign: "left",
    transition: "all 0.2s ease",
    display: "flex",
    alignItems: "center",
  },
  mainBtn: {
    width: "100%",
    padding: "16px",
    color: "white",
    border: "none",
    borderRadius: "10px",
    fontSize: "1.1rem",
    fontWeight: "bold",
    transition: "background 0.3s ease",
    marginTop: "10px",
    cursor: "pointer",
    backgroundColor: "#2196f3",
  },
  feedback: {
    padding: "15px",
    borderRadius: "10px",
    marginBottom: "20px",
    fontWeight: "500",
    lineHeight: "1.5",
    textAlign: "center",
  },
};

export default Quiz;
