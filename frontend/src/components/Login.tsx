import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authAPI } from "../api";

const Login: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await authAPI.login(username, password);
      navigate("/dashboard");
    } catch (err) {
      setError("Λάθος όνομα χρήστη ή κωδικός!");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
          MyPython 🐍
        </h2>
        <h4 style={{ textAlign: "center", color: "#666" }}>Σύνδεση</h4>

        {error && <div style={styles.error}>{error}</div>}

        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: "15px" }}>
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={styles.input}
              required
            />
          </div>
          <div style={{ marginBottom: "20px" }}>
            <label>Password</label>
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
          Δεν έχεις λογαριασμό; Ζήτα από τον διαχειριστή να σε προσθέσει.
        </p>
      </div>
    </div>
  );
};

// Απλό CSS μέσα στο αρχείο για ταχύτητα
const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    backgroundColor: "#f0f2f5",
  },
  card: {
    width: "400px",
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
  },
  button: {
    width: "100%",
    padding: "12px",
    backgroundColor: "#306998",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "16px",
    fontWeight: "bold" as "bold",
  },
  error: {
    backgroundColor: "#ffebee",
    color: "#c62828",
    padding: "10px",
    borderRadius: "4px",
    marginBottom: "15px",
    textAlign: "center" as "center",
  },
};

export default Login;
