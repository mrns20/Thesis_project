import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      // 1. ΣΥΝΔΕΣΗ
      const res = await axios.post("http://127.0.0.1:8000/api/login/", {
        username: username,
        password: password,
      });

      // 2. ΑΠΟΘΗΚΕΥΣΗ TOKENS
      const accessToken = res.data.access;
      localStorage.setItem("access_token", accessToken);
      localStorage.setItem("refresh_token", res.data.refresh);

      // 3. ΕΛΕΓΧΟΣ ΠΡΟΦΙΛ (First Login Check)
      try {
        const profileRes = await axios.get(
          "http://127.0.0.1:8000/api/profile/",
          {
            headers: { Authorization: `Bearer ${accessToken}` },
          },
        );

        if (profileRes.data.first_login === true) {
          navigate("/profile");
          return;
        }
      } catch (profileErr) {
        console.warn(
          "Το προφίλ δεν βρέθηκε ή υπήρξε σφάλμα. Συνεχίζουμε...",
          profileErr,
        );
      }

      navigate("/dashboard");
    } catch (err: any) {
      console.error("Σφάλμα Login:", err);
      setError("Λάθος όνομα χρήστη ή κωδικός.");
    }
  };

  return (
    <div style={{ ...styles.container, flexDirection: "column" }}>
      <h1
        style={{
          color: "#37b9a4",
          fontSize: "3.5rem",
          fontWeight: "900",
          fontFamily: '"Nunito", sans-serif',
          marginBottom: "30px",
          textShadow: "2px 2px 4px rgba(0,0,0,0.1)",
          userSelect: "none",
        }}
      >
        &lt;&gt;MyPython&lt;/&gt;
      </h1>

      <div style={styles.card}>
        <h2
          style={{ textAlign: "center", marginBottom: "20px", color: "#333" }}
        >
          Σύνδεση
        </h2>

        {error && <div style={styles.error}>{error}</div>}

        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: "15px" }}>
            <label
              style={{
                display: "block",
                marginBottom: "5px",
                fontWeight: "bold",
              }}
            >
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={styles.input}
              required
            />
          </div>
          <div style={{ marginBottom: "20px" }}>
            <label
              style={{
                display: "block",
                marginBottom: "5px",
                fontWeight: "bold",
              }}
            >
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
              required
            />
          </div>
          <button type="submit" style={styles.button}>
            Είσοδος
          </button>
        </form>

        <p
          style={{ marginTop: "20px", textAlign: "center", fontSize: "0.9rem" }}
        >
          Δεν έχεις λογαριασμό;
          <span
            onClick={() => navigate("/register")}
            style={{
              color: "#306998",
              cursor: "pointer",
              fontWeight: "bold",
              marginLeft: "5px",
            }}
          >
            Κάνε Εγγραφή
          </span>
        </p>
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
    width: "350px",
    padding: "40px",
    backgroundColor: "white",
    borderRadius: "8px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
  },
  input: {
    width: "100%",
    padding: "10px",
    marginTop: "5px",
    borderRadius: "4px",
    border: "1px solid #ddd",
    boxSizing: "border-box" as "border-box",
    fontSize: "16px",
  },
  button: {
    width: "100%",
    padding: "12px",
    backgroundColor: "#3785b9",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "16px",
    fontWeight: "bold" as "bold",
    marginTop: "10px",
  },
  error: {
    backgroundColor: "#ffebee",
    color: "#c62828",
    padding: "10px",
    borderRadius: "4px",
    marginBottom: "15px",
    textAlign: "center" as "center",
    border: "1px solid #ef9a9a",
  },
};

export default Login;
