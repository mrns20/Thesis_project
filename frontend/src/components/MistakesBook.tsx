import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { quizAPI } from "../api";
import Navbar from "./Navbar";

// Το Interface πρέπει να ταιριάζει ΑΚΡΙΒΩΣ με αυτό που στέλνει το Backend
interface MistakeLink {
  question: string; // Αυτό πρέπει να είναι 'question' όπως στο views.py
  link: string;
}

const MistakesBook: React.FC = () => {
  const [links, setLinks] = useState<MistakeLink[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLinks = async () => {
      try {
        const res = await quizAPI.getMistakeLinks();
        console.log("Mistakes Data:", res.data); // Δες την κονσόλα (F12) για να σιγουρευτείς
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
            <h2> Κανένα λάθος!</h2>
            <p>Δεν υπάρχουν καταγεγραμμένα λάθη ακόμα.</p>
          </div>
        ) : (
          <div style={styles.listContainer}>
            {links.map((item, index) => (
              <div key={index} style={styles.card}>
                <div style={styles.questionText}>
                  {/* Εδώ εμφανίζεται η ερώτηση. Αν είναι κενό, θα γράψει "Άγνωστη ερώτηση" */}
                  <span
                    style={{
                      color: "#d32f2f",
                      fontWeight: "bold",
                      marginRight: "10px",
                    }}
                  >
                    ❌
                  </span>
                  {item.question || "Άγνωστη ερώτηση (Δεν βρέθηκε κείμενο)"}
                </div>

                {/* Εμφάνιση Link μόνο αν υπάρχει */}
                {item.link ? (
                  <a
                    href={item.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={styles.linkButton}
                  >
                    📖 Διάβασε τη Θεωρία
                  </a>
                ) : (
                  <span style={styles.noLinkText}>
                    (Δεν υπάρχει link θεωρίας για αυτή την ερώτηση)
                  </span>
                )}
              </div>
            ))}
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
    gap: "15px",
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
