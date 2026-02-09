import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Dashboard from "./components/Dashboard";
import Quiz from "./components/Quiz";
import Footer from "./components/Footer"; // <--- Μην ξεχάσεις αυτό!
import UserProfile from "./components/UserProfile";

// Έλεγχος αν ο χρήστης είναι συνδεδεμένος
const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const token = localStorage.getItem("access_token");
  return token ? <>{children}</> : <Navigate to="/" />;
};

function App() {
  return (
    <Router>
      {/* Αλλαγή Layout: Χρησιμοποιούμε Flexbox για να πιάνει όλο το ύψος 
          και να σπρώχνει το Footer κάτω.
      */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          minHeight: "100vh",
          backgroundColor: "#f0f2f5",
        }}
      >
        {/* Ο κυρίως χώρος που θα μπαίνουν οι σελίδες */}
        <div style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route
              path="/dashboard"
              element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              }
            />

            <Route
              path="/quiz"
              element={
                <PrivateRoute>
                  <Quiz />
                </PrivateRoute>
              }
            />

            <Route
              path="/profile"
              element={
                <PrivateRoute>
                  <UserProfile />
                </PrivateRoute>
              }
            />
          </Routes>
        </div>

        {/* Το Footer μπαίνει εδώ, έξω από τα Routes αλλά μέσα στο Router */}
        <Footer />
      </div>
    </Router>
  );
}

export default App;
