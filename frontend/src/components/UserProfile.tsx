import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Navbar from "./Navbar";
import { quizAPI } from "../api";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";

interface Concept {
  id: number;
  name: string;
  mastery: number;
}

const UserProfile: React.FC = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [learningStyle, setLearningStyle] = useState("visual");
  const [bio, setBio] = useState("");

  const [chartData, setChartData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem("access_token");
      try {
        // Φόρτωση Προφίλ από το Backend
        const profileRes = await axios.get(
          "http://127.0.0.1:8000/api/profile/",
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        setFirstName(profileRes.data.first_name || "");
        setLastName(profileRes.data.last_name || "");
        setEmail(profileRes.data.email || "");
        setLearningStyle(profileRes.data.learning_style || "visual");
        setBio(profileRes.data.bio || "");

        // Φόρτωση Ποσοστών για το Γράφημα
        const conceptsRes = await quizAPI.getConceptMap();
        const formattedData = conceptsRes.data.map((c: Concept) => ({
          subject: c.name,
          mastery: c.mastery,
          fullMark: 100,
        }));
        setChartData(formattedData);
      } catch (err) {
        console.error("Σφάλμα φόρτωσης δεδομένων", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");
    try {
      // Στέλνουμε τα νέα δεδομένα στο Backend
      await axios.post(
        "http://127.0.0.1:8000/api/profile/",
        {
          first_name: firstName,
          last_name: lastName,
          email: email,
          learning_style: learningStyle,
          bio: bio,
        },
        { headers: { Authorization: `Bearer ${token}` } },
      );
      // Επιστροφή στον χάρτη
      navigate("/dashboard");
    } catch (error) {
      console.error("Error updating profile:", error);
    }
  };

  //Λογική για το Απλό Ημερολόγιο
  const today = new Date();
  const currentMonth = today.toLocaleString("el-GR", { month: "long" });
  const currentYear = today.getFullYear();
  const daysInMonth = new Date(currentYear, today.getMonth() + 1, 0).getDate();
  const firstDayOfMonth = new Date(currentYear, today.getMonth(), 1).getDay();
  const blanks = Array(firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1).fill(
    null,
  );
  const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);

  if (loading) return <div style={styles.center}>Φόρτωση...</div>;

  return (
    <div style={{ backgroundColor: "#f4f6f8", minHeight: "92vh" }}>
      <Navbar />

      <div style={styles.pageContainer}>
        <div style={styles.header}>
          <h1 style={{ margin: 0, color: "#333" }}>Οι Ρυθμίσεις μου</h1>
          <p style={{ margin: "5px 0 0 0", color: "#666" }}>
            Διαχειριστείτε το προφίλ και τις προτιμήσεις μάθησης.
          </p>
        </div>

        <div style={styles.gridContainer}>
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>Προσωπικά Στοιχεία</h3>
            <form onSubmit={handleSubmit} style={styles.form}>
              <div style={styles.row}>
                <div style={styles.inputGroup}>
                  <label style={styles.label}>Όνομα</label>
                  <input
                    type="text"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    style={styles.input}
                    placeholder="π.χ. Μαρίνος"
                  />
                </div>
                <div style={styles.inputGroup}>
                  <label style={styles.label}>Επώνυμο</label>
                  <input
                    type="text"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    style={styles.input}
                    placeholder="π.χ. Τσελάνι"
                  />
                </div>
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Email</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  style={styles.input}
                  placeholder="marino@example.com"
                />
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Σύντομο Βιογραφικό</label>
                <textarea
                  value={bio}
                  onChange={(e) => setBio(e.target.value)}
                  style={{ ...styles.input, height: "80px", resize: "none" }}
                  placeholder="Bio..."
                />
              </div>

              <h3 style={{ ...styles.cardTitle, marginTop: "30px" }}>
                Προτιμήσεις Μάθησης
              </h3>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Πώς προτιμάτε να μαθαίνετε;</label>
                <select
                  value={learningStyle}
                  onChange={(e) => setLearningStyle(e.target.value)}
                  style={styles.select}
                >
                  <option value="visual">Οπτικά</option>
                  <option value="read_write">Mε Κείμενο ανάγνωσης</option>
                </select>
                <small
                  style={{
                    color: "#888",
                    marginTop: "5px",
                    display: "block",
                    lineHeight: "1.4",
                  }}
                >
                  * Ο αλγόριθμος θα προσαρμόσει την οπτική και δομική παρουσίαση
                  του υλικού ανάλογα με την επιλογή σας.
                </small>
              </div>

              <button type="submit" style={styles.submitBtn}>
                Αποθήκευση Αλλαγών
              </button>
            </form>
          </div>

          <div style={styles.rightColumn}>
            <div style={{ ...styles.card, marginBottom: "20px" }}>
              <h3 style={styles.cardTitle}>Ιστός Δεξιοτήτων </h3>
              <div style={{ width: "100%", height: 250 }}>
                {chartData.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart
                      cx="50%"
                      cy="50%"
                      outerRadius="70%"
                      data={chartData}
                    >
                      <PolarGrid />
                      {/* @ts-ignore */}
                      <PolarAngleAxis
                        dataKey="subject"
                        tick={{
                          fill: "#555",
                          fontSize: 12,
                          fontWeight: "bold",
                        }}
                      />
                      {/* @ts-ignore */}
                      <PolarRadiusAxis
                        angle={30}
                        domain={[0, 100]}
                        tick={false}
                        axisLine={false}
                      />
                      <Radar
                        name="Κατάκτηση (%)"
                        dataKey="mastery"
                        stroke="#77dd77"
                        fill="#77dd77"
                        fillOpacity={0.6}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                ) : (
                  <div style={styles.centerSmall}>Δεν υπάρχουν δεδομένα.</div>
                )}
              </div>
            </div>

            <div style={styles.card}>
              <h3 style={styles.cardTitle}>Ημερολόγιο </h3>
              <div style={styles.calendarHeader}>
                <strong>
                  {currentMonth.charAt(0).toUpperCase() + currentMonth.slice(1)}{" "}
                  {currentYear}
                </strong>
              </div>
              <div style={styles.calendarGrid}>
                {["Δ", "Τ", "Τ", "Π", "Π", "Σ", "Κ"].map((day, i) => (
                  <div key={`header-${i}`} style={styles.calendarDayName}>
                    {day}
                  </div>
                ))}
                {blanks.map((_, i) => (
                  <div key={`blank-${i}`} />
                ))}
                {days.map((day) => (
                  <div
                    key={day}
                    style={{
                      ...styles.calendarDay,
                      ...(day === today.getDate() ? styles.calendarToday : {}),
                    }}
                  >
                    {day}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  center: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
  },
  centerSmall: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100%",
    color: "#999",
  },
  pageContainer: { maxWidth: "1100px", margin: "0 auto", padding: "40px 20px" },
  header: { marginBottom: "30px" },
  gridContainer: {
    display: "grid",
    gridTemplateColumns: "1.5fr 1fr",
    gap: "30px",
    alignItems: "start",
  },
  card: {
    backgroundColor: "white",
    padding: "30px",
    borderRadius: "16px",
    boxShadow: "0 4px 20px rgba(0,0,0,0.05)",
  },
  cardTitle: {
    margin: "0 0 20px 0",
    color: "#333",
    borderBottom: "2px solid #f0f0f0",
    paddingBottom: "10px",
    fontSize: "1.2rem",
  },
  form: { display: "flex", flexDirection: "column", gap: "20px" },
  row: { display: "flex", gap: "20px" },
  inputGroup: { display: "flex", flexDirection: "column", flex: 1 },
  label: {
    marginBottom: "8px",
    fontWeight: "bold",
    color: "#555",
    fontSize: "0.95rem",
  },
  input: {
    padding: "12px 15px",
    borderRadius: "8px",
    border: "1px solid #ddd",
    fontSize: "1rem",
    backgroundColor: "#f9fafb",
    transition: "border 0.3s",
    outline: "none",
  },
  select: {
    padding: "12px 15px",
    borderRadius: "8px",
    border: "1px solid #ddd",
    fontSize: "1rem",
    backgroundColor: "#f9fafb",
    cursor: "pointer",
  },
  submitBtn: {
    marginTop: "10px",
    padding: "15px",
    backgroundColor: "#2196f3",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "1.1rem",
    fontWeight: "bold",
    transition: "background 0.3s",
  },
  rightColumn: { display: "flex", flexDirection: "column" },
  calendarHeader: {
    textAlign: "center",
    marginBottom: "15px",
    fontSize: "1.1rem",
    color: "#333",
  },
  calendarGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(7, 1fr)",
    gap: "5px",
    textAlign: "center",
  },
  calendarDayName: {
    fontWeight: "bold",
    color: "#888",
    marginBottom: "10px",
    fontSize: "0.9rem",
  },
  calendarDay: {
    padding: "8px 0",
    borderRadius: "5px",
    fontSize: "0.95rem",
    color: "#444",
  },
  calendarToday: {
    backgroundColor: "#77dd77",
    color: "white",
    fontWeight: "bold",
    borderRadius: "50%",
  },
};

export default UserProfile;
