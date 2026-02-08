import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import Quiz from "./components/Quiz";

// Έλεγχος αν ο χρήστης είναι συνδεδεμένος
const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const token = localStorage.getItem("access_token");
  // ΠΡΟΣΟΧΗ: Βάζουμε το <>{children}</> για να είναι valid JSX Element
  return token ? <>{children}</> : <Navigate to="/" />;
};

function App() {
  return (
    <Router>
      <div
        className="App"
        style={{ minHeight: "100vh", backgroundColor: "#f0f2f5" }}
      >
        <Routes>
          <Route path="/" element={<Login />} />

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
        </Routes>
      </div>
    </Router>
  );
}

export default App;
