import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { quizAPI } from "../api";

interface Question {
  id: number;
  text: string;
  code_snippet?: string;
  question_type: "MC" | "TF";
  option_a: string;
  option_b: string;
  option_c?: string;
  option_d?: string;
}

interface Feedback {
  correct: boolean;
  correct_option: string;
  message: string;
  new_mastery: number;
  recommendation?: {
    text: string;
    link: string;
  };
}

const Quiz: React.FC = () => {
  const [question, setQuestion] = useState<Question | null>(null);
  const [selectedOption, setSelectedOption] = useState<string>("");
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [loading, setLoading] = useState(true);
  const [finished, setFinished] = useState(false);

  const navigate = useNavigate();

  // Συνάρτηση για φόρτωση επόμενης ερώτησης
  const fetchQuestion = async () => {
    setLoading(true);
    setFeedback(null);
    setSelectedOption("");

    try {
      const res = await quizAPI.getNextQuestion();
      if (res.data.completed) {
        setFinished(true);
      } else {
        setQuestion(res.data);
      }
    } catch (err) {
      console.error("Error fetching question", err);
    } finally {
      setLoading(false);
    }
  };

  // Φόρτωση κατά την εκκίνηση
  useEffect(() => {
    fetchQuestion();
  }, []);

  // Υποβολή απάντησης
  const handleSubmit = async () => {
    if (!question || !selectedOption) return;

    try {
      const res = await quizAPI.submitAnswer(question.id, selectedOption);
      setFeedback(res.data);
    } catch (err) {
      console.error("Error submitting answer", err);
    }
  };

  if (loading) return <div style={styles.center}>Φόρτωση ερώτησης... ⏳</div>;

  if (finished)
    return (
      <div style={styles.center}>
        <div style={styles.card}>
          <h2>🎉 Συγχαρητήρια!</h2>
          <p>Έχεις ολοκληρώσει όλες τις διαθέσιμες έννοιες για τώρα.</p>
          <button onClick={() => navigate("/dashboard")} style={styles.button}>
            Επιστροφή στο Χάρτη
          </button>
        </div>
      </div>
    );

  if (!question) return <div style={styles.center}>Κάτι πήγε στραβά.</div>;

  return (
    <div style={styles.container}>
      <button onClick={() => navigate("/dashboard")} style={styles.backBtn}>
        ⬅ Πίσω
      </button>

      <div style={styles.card}>
        <span style={styles.badge}>
          {question.question_type === "MC"
            ? "Πολλαπλής Επιλογής"
            : "Σωστό / Λάθος"}
        </span>

        <h3 style={styles.questionText}>{question.text}</h3>

        {question.code_snippet && (
          <pre style={styles.codeBlock}>
            <code>{question.code_snippet}</code>
          </pre>
        )}

        <div style={styles.optionsGrid}>
          {["A", "B", "C", "D"].map((opt) => {
            // Ανάκτηση κειμένου επιλογής (π.χ. option_a)
            const optText =
              question[`option_${opt.toLowerCase()}` as keyof Question];
            if (!optText) return null; // Αν δεν υπάρχει (π.χ. C, D σε True/False)

            let btnStyle = styles.optionBtn;

            // Χρωματισμός μετά την απάντηση
            if (feedback) {
              if (opt === feedback.correct_option)
                btnStyle = { ...btnStyle, ...styles.correctBtn };
              else if (opt === selectedOption && !feedback.correct)
                btnStyle = { ...btnStyle, ...styles.wrongBtn };
              else btnStyle = { ...btnStyle, opacity: 0.5 };
            } else if (selectedOption === opt) {
              btnStyle = { ...btnStyle, ...styles.selectedBtn };
            }

            return (
              <button
                key={opt}
                onClick={() => !feedback && setSelectedOption(opt)}
                style={btnStyle}
                disabled={!!feedback}
              >
                <span style={{ fontWeight: "bold" }}>{opt}. </span> {optText}
              </button>
            );
          })}
        </div>

        {!feedback ? (
          <button
            onClick={handleSubmit}
            style={
              selectedOption
                ? styles.submitBtn
                : { ...styles.submitBtn, ...styles.disabledBtn }
            }
            disabled={!selectedOption}
          >
            Υποβολή Απάντησης
          </button>
        ) : (
          <div style={styles.feedbackArea}>
            <h3 style={{ color: feedback.correct ? "#2e7d32" : "#c62828" }}>
              {feedback.message}
            </h3>
            <p>
              Νέο επίπεδο γνώσης: <strong>{feedback.new_mastery}%</strong>
            </p>

            {feedback.recommendation && (
              <div style={styles.remedialBox}>
                <p>💡 {feedback.recommendation.text}</p>
                <a
                  href={feedback.recommendation.link}
                  target="_blank"
                  rel="noreferrer"
                >
                  Διάβασε τη θεωρία εδώ
                </a>
              </div>
            )}

            <button onClick={fetchQuestion} style={styles.nextBtn}>
              Επόμενη Ερώτηση ➡
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: { maxWidth: "800px", margin: "40px auto", padding: "0 20px" },
  center: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    fontSize: "1.2rem",
  },
  card: {
    backgroundColor: "white",
    padding: "30px",
    borderRadius: "15px",
    boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
  },
  backBtn: {
    marginBottom: "20px",
    background: "none",
    border: "none",
    cursor: "pointer",
    fontSize: "1rem",
    color: "#666",
  },
  badge: {
    backgroundColor: "#e3f2fd",
    color: "#1565c0",
    padding: "5px 10px",
    borderRadius: "4px",
    fontSize: "0.8rem",
    fontWeight: "bold",
  },
  questionText: { marginTop: "15px", fontSize: "1.3rem", lineHeight: "1.5" },
  codeBlock: {
    backgroundColor: "#282c34",
    color: "#abb2bf",
    padding: "15px",
    borderRadius: "8px",
    overflowX: "auto",
    fontFamily: "monospace",
  },
  optionsGrid: { display: "grid", gap: "10px", marginTop: "20px" },
  optionBtn: {
    padding: "15px",
    textAlign: "left",
    border: "2px solid #eee",
    borderRadius: "8px",
    backgroundColor: "white",
    cursor: "pointer",
    fontSize: "1rem",
    transition: "all 0.2s",
  },
  selectedBtn: { borderColor: "#2196f3", backgroundColor: "#e3f2fd" },
  correctBtn: {
    borderColor: "#4caf50",
    backgroundColor: "#e8f5e9",
    color: "#1b5e20",
  },
  wrongBtn: {
    borderColor: "#ef5350",
    backgroundColor: "#ffebee",
    color: "#c62828",
  },
  submitBtn: {
    width: "100%",
    padding: "15px",
    marginTop: "20px",
    backgroundColor: "#306998",
    color: "white",
    border: "none",
    borderRadius: "8px",
    fontSize: "1.1rem",
    cursor: "pointer",
    fontWeight: "bold",
  },
  disabledBtn: { backgroundColor: "#ccc", cursor: "not-allowed" },
  feedbackArea: {
    marginTop: "20px",
    padding: "20px",
    backgroundColor: "#fafafa",
    borderRadius: "10px",
    textAlign: "center",
  },
  remedialBox: {
    margin: "15px 0",
    padding: "10px",
    backgroundColor: "#fff3cd",
    border: "1px solid #ffeeba",
    borderRadius: "5px",
    color: "#856404",
  },
  nextBtn: {
    padding: "10px 20px",
    backgroundColor: "#2196f3",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "1rem",
    marginTop: "10px",
  },
};

export default Quiz;
