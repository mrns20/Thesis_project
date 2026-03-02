import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authAPI } from "../api";

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await authAPI.register(formData);
      setSuccess(true);
      // Μετά από 2 sec, πήγαινε τον στο Login
      setTimeout(() => {
        navigate("/");
      }, 2000);
    } catch (err) {
      setError("Αποτυχία εγγραφής. Δοκίμασε άλλο όνομα χρήστη.");
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
        <h2 style={{ textAlign: "center", marginBottom: "20px" }}>Εγγραφή</h2>

        {success ? (
          <div style={styles.success}>
            Ο λογαριασμός δημιουργήθηκε! <br /> Μεταφορά στη σύνδεση...
          </div>
        ) : (
          <form onSubmit={handleRegister}>
            {error && <div style={styles.error}>{error}</div>}

            <div style={{ marginBottom: "15px" }}>
              <label>Username</label>
              <input
                name="username"
                type="text"
                value={formData.username}
                onChange={handleChange}
                style={styles.input}
                required
              />
            </div>
            <div style={{ marginBottom: "15px" }}>
              <label>Email</label>
              <input
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                style={styles.input}
                required
              />
            </div>
            <div style={{ marginBottom: "20px" }}>
              <label>Password</label>
              <input
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                style={styles.input}
                required
              />
            </div>
            <button type="submit" style={styles.button}>
              Δημιουργία Λογαριασμού
            </button>
          </form>
        )}

        <p
          style={{ marginTop: "20px", textAlign: "center", fontSize: "0.9rem" }}
        >
          Έχεις ήδη λογαριασμό;
          <span
            onClick={() => navigate("/")}
            style={{
              color: "#306998",
              cursor: "pointer",
              fontWeight: "bold",
              marginLeft: "5px",
            }}
          >
            Σύνδεση
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
    minHeight: "80vh",
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
    backgroundColor: "#37b9a4",
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
  success: {
    backgroundColor: "#e8f5e9",
    color: "#37b9a4",
    padding: "20px",
    borderRadius: "4px",
    textAlign: "center" as "center",
    fontSize: "1.1rem",
  },
};

export default Register;
