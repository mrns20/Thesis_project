import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const UserProfile: React.FC = () => {
  const [bio, setBio] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // ΝΕΟ: Φόρτωση των υπαρχόντων στοιχείων μόλις ανοίξει η σελίδα
  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem("access_token");
      try {
        const res = await axios.get("http://127.0.0.1:8000/api/profile/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        // Γεμίζουμε τα πεδία με αυτά που ήρθαν από τη βάση
        setBio(res.data.bio || "");
        setPhone(res.data.phone || "");
      } catch (err) {
        console.error("Δεν βρέθηκε προφίλ ή υπήρξε σφάλμα");
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");
    try {
      await axios.post(
        "http://127.0.0.1:8000/api/profile/",
        {
          bio: bio,
          phone: phone,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );
      navigate("/dashboard");
    } catch (error) {
      console.error("Error updating profile:", error);
    }
  };

  if (loading) return <div style={styles.center}>Φόρτωση...</div>;

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        {/* Κουμπί Πίσω */}
        <button onClick={() => navigate("/dashboard")} style={styles.backBtn}>
          ⬅ Πίσω
        </button>

        <h2> Το Προφίλ μου</h2>
        <p>Επεξεργασία προσωπικών στοιχείων</p>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "15px" }}>
            <label>Σύντομο Βιογραφικό:</label>
            <textarea
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              style={{ ...styles.input, height: "80px" }}
            />
          </div>
          <div style={{ marginBottom: "20px" }}>
            <label>Τηλέφωνο:</label>
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              style={styles.input}
            />
          </div>
          <button type="submit" style={styles.button}>
            Αποθήκευση Αλλαγών
          </button>
        </form>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100%",
    minHeight: "80vh",
    backgroundColor: "#f0f2f5",
  },
  card: {
    width: "400px",
    padding: "30px",
    backgroundColor: "white",
    borderRadius: "10px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
  },
  input: {
    width: "100%",
    padding: "10px",
    marginTop: "5px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    boxSizing: "border-box" as "border-box",
  },
  button: {
    width: "100%",
    padding: "12px",
    backgroundColor: "#2196f3",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  },
  backBtn: {
    background: "none",
    border: "none",
    cursor: "pointer",
    color: "#666",
    marginBottom: "10px",
    fontSize: "1rem",
  },
  center: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
  },
};

export default UserProfile;
