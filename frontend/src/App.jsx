import { Routes, Route, useNavigate } from "react-router-dom";
import FeedbackPage from "./pages/FeedbackPage";
import AdminDashboard from "./pages/AdminDashboard";
import AdminLogin from "./pages/AdminLogin";

function Home() {
  const navigate = useNavigate();

  return (
    <>
      <h1>Feedback Centre</h1>

      <button onClick={() => navigate("/submit-feedback")}>
        Submit Feedback
      </button>

      <button onClick={() => navigate("/admin")}>
        Admin Dashboard
      </button>
    </>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/submit-feedback" element={<FeedbackPage />} />
      <Route path="/admin" element={<AdminLogin />} />
      <Route path="/admin/dashboard" element={<AdminDashboard />} />
    </Routes>
  );
}