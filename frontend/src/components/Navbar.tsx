import React from "react";
import { useNavigate } from "react-router-dom";
import { authAPI } from "../api";

const Navbar: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    authAPI.logout();
    navigate("/");
  };

  return (
    <nav style={styles.navbar}>
      {/* Αριστερά: Το Λογότυπο (όταν πατιέται πάει Dashboard) */}
      <div
        onClick={() => navigate("/dashboard")}
        style={styles.logo}
        title="Επιστροφή στο Dashboard"
      >
        &lt;&gt;MyPython&lt;/&gt;
      </div>

      {/* Δεξιά: Τα Κουμπιά */}
      <div style={styles.buttonGroup}>
        <button onClick={() => navigate("/profile")} style={styles.profileBtn}>
          Προφίλ
        </button>
        <button onClick={handleLogout} style={styles.logoutBtn}>
          Αποσύνδεση
        </button>
      </div>
    </nav>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "15px 40px",
    backgroundColor: "#323a3b",
    boxShadow: "0 2px 10px rgba(73, 68, 68, 0.08)", // Ελαφριά σκιά από κάτω
    position: "sticky", // Μένει καρφωμένο πάνω όταν σκρολάρεις
    top: 0,
    zIndex: 1000,
  },
  logo: {
    color: "#37b9a4", // Όμορφο Παστέλ Πράσινο
    fontSize: "2.2rem", // Αρκετά μεγαλύτερο από τα κουμπιά
    fontWeight: "900",
    fontFamily: '"Nunito", "Quicksand", "Comic Sans MS", sans-serif', // Η κυκλική γραμματοσειρά
    cursor: "pointer",
    userSelect: "none",
    letterSpacing: "1px",
  },
  buttonGroup: {
    display: "flex",
    gap: "15px", // Κενό ανάμεσα στα κουμπιά
  },
  profileBtn: {
    padding: "10px 20px",
    cursor: "pointer",
    backgroundColor: "#21d4f3",
    color: "white",
    border: "none",
    borderRadius: "25px", // Στρογγυλεμένα κουμπιά για να ταιριάζουν με το logo
    fontWeight: "bold",
    fontSize: "1rem",
  },
  logoutBtn: {
    padding: "10px 20px",
    cursor: "pointer",
    backgroundColor: "#f44336",
    color: "white",
    border: "none",
    borderRadius: "25px",
    fontWeight: "bold",
    fontSize: "1rem",
  },
};

export default Navbar;
