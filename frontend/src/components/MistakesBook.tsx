import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { quizAPI } from "../api";
import Navbar from "./Navbar";

interface MistakeLink {
  question: string;
  link: string;
  video_link: string; // Προσθήκη του νέου πεδίου
  learning_style: string; // Προσθήκη του τύπου μάθησης
}

const MistakesBook: React.FC = () => {
  const [links, setLinks] = useState<MistakeLink[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLinks = async () => {
      try {
        const res = await quizAPI.getMistakeLinks();
        setLinks(res.data);
      } catch (err) {
        console.error("Error fetching links", err);
      } finally {
        setLoading(false);
      }
    };
    fetchLinks();
  }, []);

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

        {loading ? (
          <p style={{ textAlign: "center" }}>Φόρτωση...</p>
        ) : links.length === 0 ? (
          <div style={styles.emptyState}>
            <h2> Το μονοπάτι μάθησης είναι άδειο!</h2>
            <p>Δεν υπάρχουν καταγεγραμμένα λάθη ακόμα.</p>
          </div>
        ) : (
          <div style={styles.listContainer}>
            {links.map((item, index) => {
              // Λογική για το ποιο link θα δείξουμε:
              const isVisual = item.learning_style === "visual"; // ή όποια λέξη έχεις για το "Οπτικά"
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
                    style={{ display: "flex", gap: "10px", marginTop: "10px" }}
                  >
                    {/* Αν είναι Οπτικός τύπος και υπάρχει βίντεο */}
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

                    {/* Αν ΔΕΝ είναι Οπτικός τύπος, Ή αν είναι αλλά δεν βρήκαμε βίντεο, δείξε το κείμενο */}
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

                    {/* Αν δεν υπάρχει ούτε κείμενο ούτε βίντεο */}
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
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: { maxWidth: "800px", margin: "0 auto", padding: "40px 20px" },
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
    color: "#1565c0",
    padding: "10px 15px",
    borderRadius: "8px",
    textDecoration: "none",
    fontWeight: "bold",
    fontSize: "0.9rem",
    border: "1px solid #bbdefb",
    transition: "all 0.2s",
  },

  // Νέο style για το κουμπί του βίντεο (έβαλα ένα κοκκινωπό στυλ τύπου YouTube)
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
