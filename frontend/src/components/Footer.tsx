import React from "react";

const Footer: React.FC = () => {
  return (
    <footer style={styles.footer}>
      <p style={styles.text}>
        © 2026 MyPython | Διπλωματική Εργασία :Ανάπτυξη διαδικτυακής εφαρμογής
        για εξατομικευμένες προτάσεις μαθησιακών μονοπατιών με στόχο την
        ενίσχυση δεξιοτήτων
      </p>
      <p style={styles.subText}>
        Created by <strong>ΜΑΡΙΝΟ ΤΣΕΛΑΝΙ, Α.Μ: 20390241</strong>
      </p>
    </footer>
  );
};

const styles = {
  footer: {
    backgroundColor: "#282c34", // Σκούρο χρώμα για contrast
    color: "white",
    textAlign: "center" as "center",
    padding: "20px",
    marginTop: "auto", // Αυτό βοηθάει να σπρώχνεται προς τα κάτω
    width: "100%",
  },
  text: {
    margin: "0",
    fontSize: "1rem",
    fontWeight: "bold",
  },
  subText: {
    margin: "5px 0 0",
    fontSize: "0.8rem",
    color: "#abb2bf",
  },
};

export default Footer;
