import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { quizAPI } from "../api";
import Navbar from "./Navbar";

interface MistakeLink {
  question: string;
  link: string;
  video_link: string;
  learning_style: string;
}

interface EvaluationData {
  score: number;
  message: string;
}

const MistakesBook: React.FC = () => {
  const [links, setLinks] = useState<MistakeLink[]>([]);
  const [evaluation, setEvaluation] = useState<EvaluationData | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLinks = async () => {
      try {
        const res = await quizAPI.getMistakeLinks();
        // Ενημέρωση των States με τη νέα δομή δεδομένων
        setLinks(res.data.links);
        setEvaluation(res.data.evaluation);
      } catch (err) {
        console.error("Error fetching links", err);
      } finally {
        setLoading(false);
      }
    };
    fetchLinks();
  }, []);

  // Βοηθητική συνάρτηση για το χρώμα της μπάρας σκορ
  const getScoreColor = (score: number) => {
    if (score >= 80) return "#4caf50";
    if (score >= 50) return "#ff9800";
    return "#f44336";
  };

  return (
    <div style={{ minHeight: "80vh", backgroundColor: "#f0f2f5" }}>
      <Navbar />
      <div style={styles.container}>
        <div style={styles.headerRow}>
          <button onClick={() => navigate("/dashboard")} style={styles.backBtn}>
            ⬅
          </button>
          <h1 style={{ margin: 0, color: "#333" }}>Mονοπάτι μάθησης</h1>
        </div>

        <div style={styles.contentWrapper}>
          {/* ΑΡΙΣΤΕΡΗ ΣΤΗΛΗ: Λίστα Λαθών */}
          <div style={styles.listColumn}>
            {loading ? (
              <p style={{ textAlign: "center" }}>Φόρτωση...</p>
            ) : links.length === 0 ? (
              <div style={styles.emptyState}>
                <h2>Το μονοπάτι μάθησης είναι άδειο!</h2>
                <p>
                  Δεν υπάρχουν καταγεγραμμένα λάθη ακόμα. Συνέχισε την καλή
                  δουλειά!
                </p>
              </div>
            ) : (
              <div style={styles.listContainer}>
                {links.map((item, index) => {
                  const isVisual = item.learning_style === "visual";
                  const hasVideo = !!item.video_link;
                  const hasText = !!item.link;

                  return (
                    <div key={index} style={styles.card}>
                      <div style={styles.questionText}>
                        <span
                          style={{
                            color: "#ffffff",
                            fontWeight: "bold",
                            marginRight: "10px",
                          }}
                        >
                          {index + 1}.
                        </span>
                        {item.question || "Άγνωστη ερώτηση"}
                      </div>

                      <div
                        style={{
                          display: "flex",
                          gap: "10px",
                          marginTop: "10px",
                        }}
                      >
                        {isVisual && hasVideo ? (
                          <a
                            href={item.video_link}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={styles.videoLinkButton}
                          >
                            Δες το Βίντεο
                          </a>
                        ) : null}

                        {(!isVisual || !hasVideo) && hasText ? (
                          <a
                            href={item.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={styles.linkButton}
                          >
                            Διάβασε τη Θεωρία
                          </a>
                        ) : null}

                        {!hasText && (!isVisual || !hasVideo) ? (
                          <span style={styles.noLinkText}>
                            (Δεν υπάρχει διαθέσιμο υλικό)
                          </span>
                        ) : null}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* ΔΕΞΙΑ ΣΤΗΛΗ: Πλαίσιο Αξιολόγησης */}
          {!loading && evaluation && (
            <div style={styles.evalColumn}>
              <div style={styles.evalCard}>
                <h3 style={{ margin: "0 0 10px 0", color: "#333" }}>
                  Αξιολόγηση Επιπέδου Γνώσεων
                </h3>
                <p
                  style={{
                    margin: "0 0 15px 0",
                    fontSize: "0.95rem",
                    color: "#555",
                    lineHeight: "1.4",
                  }}
                >
                  {evaluation.message}
                </p>

                {/* Μπάρα Προόδου */}
                <div style={styles.progressBarContainer}>
                  <div
                    style={{
                      ...styles.progressBarFill,
                      width: `${evaluation.score}%`,
                      backgroundColor: getScoreColor(evaluation.score),
                    }}
                  />
                </div>
                <div
                  style={{
                    textAlign: "right",
                    fontSize: "0.85rem",
                    color: "#666",
                    marginTop: "5px",
                    fontWeight: "bold",
                  }}
                >
                  Σκορ: {evaluation.score}%
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: { maxWidth: "1100px", margin: "0 auto", padding: "40px 20px" },
  headerRow: {
    display: "flex",
    alignItems: "center",
    gap: "20px",
    marginBottom: "30px",
  },
  backBtn: {
    padding: "8px 16px",
    borderRadius: "8px",
    border: "1px solid #ccc",
    background: "white",
    cursor: "pointer",
    fontWeight: "bold",
  },

  // Διάταξη Flexbox για τις 2 στήλες
  contentWrapper: {
    display: "flex",
    gap: "40px",
    alignItems: "flex-start",
    flexWrap: "wrap",
  },

  listColumn: { flex: "2 1 600px" },

  evalColumn: { flex: "1 1 300px", top: "20px" },

  evalCard: {
    backgroundColor: "#fff",
    padding: "20px",
    borderRadius: "12px",
    boxShadow: "0 4px 15px rgba(0,0,0,0.05)",
  },
  progressBarContainer: {
    height: "10px",
    width: "100%",
    backgroundColor: "#e0e0e0",
    borderRadius: "5px",
    overflow: "hidden",
  },
  progressBarFill: { height: "100%", transition: "width 0.5s ease-in-out" },

  listContainer: { display: "flex", flexDirection: "column", gap: "15px" },
  card: {
    backgroundColor: "white",
    padding: "25px",
    borderRadius: "12px",
    boxShadow: "0 4px 15px rgba(0,0,0,0.05)",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  questionText: {
    fontSize: "1.1rem",
    color: "#333",
    fontWeight: 500,
    lineHeight: "1.5",
  },
  linkButton: {
    alignSelf: "flex-start",
    backgroundColor: "#e3f2fd",
    padding: "10px 15px",
    borderRadius: "8px",
    textDecoration: "none",
    fontWeight: "bold",
    fontSize: "0.9rem",
    border: "1px solid #bbdefb",
    transition: "all 0.2s",
  },
  videoLinkButton: {
    alignSelf: "flex-start",
    backgroundColor: "#ffebee",
    color: "#c62828",
    padding: "10px 15px",
    borderRadius: "8px",
    textDecoration: "none",
    fontWeight: "bold",
    fontSize: "0.9rem",
    border: "1px solid #ffcdd2",
    transition: "all 0.2s",
  },
  noLinkText: {
    fontSize: "0.85rem",
    color: "#999",
    fontStyle: "italic",
    marginTop: "5px",
  },
  emptyState: {
    textAlign: "center",
    padding: "50px",
    backgroundColor: "white",
    borderRadius: "12px",
  },
};

export default MistakesBook;
