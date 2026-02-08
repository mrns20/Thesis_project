import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { quizAPI, authAPI } from "../api";

interface Concept {
  id: number;
  name: string;
  description: string;
  mastery: number;
  is_unlocked: boolean;
}

const Dashboard: React.FC = () => {
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMap = async () => {
      try {
        const res = await quizAPI.getConceptMap();
        setConcepts(res.data);
      } catch (err) {
        console.error("Failed to fetch map", err);
      }
    };
    fetchMap();
  }, []);

  const handleLogout = () => {
    authAPI.logout();
    navigate("/");
  };

  return (
    <div style={{ padding: "40px", maxWidth: "1000px", margin: "0 auto" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "40px",
        }}
      >
        <h1>🗺️ Ο Χάρτης της Python</h1>
        <button
          onClick={handleLogout}
          style={{ padding: "8px 16px", cursor: "pointer" }}
        >
          Αποσύνδεση
        </button>
      </div>

      <div style={styles.grid}>
        {concepts.map((concept) => (
          <div
            key={concept.id}
            style={{
              ...styles.card,
              opacity: concept.is_unlocked ? 1 : 0.6,
              borderLeft:
                concept.mastery === 100
                  ? "5px solid #4caf50"
                  : "5px solid #2196f3",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <h3>{concept.name}</h3>
              {concept.mastery === 100 && <span>✅</span>}
              {!concept.is_unlocked && <span>🔒</span>}
            </div>

            <p style={{ color: "#666", fontSize: "0.9rem" }}>
              {concept.description}
            </p>

            <div style={styles.progressBar}>
              <div
                style={{ ...styles.progressFill, width: `${concept.mastery}%` }}
              ></div>
            </div>
            <p style={{ fontSize: "0.8rem", textAlign: "right" }}>
              {concept.mastery}% Κατάκτηση
            </p>

            {concept.is_unlocked && concept.mastery < 100 && (
              <button
                onClick={() => navigate("/quiz")}
                style={styles.actionBtn}
              >
                Συνέχισε τη Μάθηση ▶
              </button>
            )}
          </div>
        ))}
      </div>

      <div style={{ marginTop: "50px", textAlign: "center" }}>
        <button onClick={() => navigate("/quiz")} style={styles.bigButton}>
          🚀 Πάμε στο Κουίζ!
        </button>
      </div>
    </div>
  );
};

const styles = {
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
    gap: "20px",
  },
  card: {
    backgroundColor: "white",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
    position: "relative" as "relative",
  },
  progressBar: {
    height: "10px",
    backgroundColor: "#e0e0e0",
    borderRadius: "5px",
    marginTop: "15px",
    marginBottom: "5px",
    overflow: "hidden",
  },
  progressFill: {
    height: "100%",
    backgroundColor: "#4caf50",
    transition: "width 0.3s ease",
  },
  actionBtn: {
    marginTop: "15px",
    width: "100%",
    padding: "10px",
    backgroundColor: "#2196f3",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  bigButton: {
    padding: "15px 40px",
    fontSize: "1.2rem",
    backgroundColor: "#306998",
    color: "white",
    border: "none",
    borderRadius: "50px",
    cursor: "pointer",
    boxShadow: "0 4px 15px rgba(48, 105, 152, 0.4)",
  },
};

export default Dashboard;
