import { useState } from "react";
import api from "./services/api";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import DashboardContent from "./components/DashboardContent";
import CandidateDrawer from "./components/CandidateDrawer";

export default function App() {
  // ===========================
  // State
  // ===========================

  const [atsResults, setAtsResults] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  // ===========================
  // Upload Job Description
  // ===========================

  const uploadJD = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      await api.post("/upload-jd", formData);
      alert("✅ Job Description Uploaded");
    } catch (err) {
      console.error(err);
      alert("JD Upload Failed");
    }
  };

  // ===========================
  // Upload Resume(s)
  // ===========================

  const uploadResumes = async (event) => {
    const files = Array.from(event.target.files);

    if (files.length === 0) return;

    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      await api.post("/upload-resumes", formData);
      alert("✅ Resume Upload Successful");
    } catch (err) {
      console.error(err);
      alert("Resume Upload Failed");
    }
  };

  // ===========================
  // Calculate ATS
  // ===========================

  const calculateATS = async () => {
    try {
      const res = await api.post("/calculate-ats");
      setAtsResults(res.data.results);
    } catch (err) {
      console.error(err);
      alert("ATS Calculation Failed");
    }
  };

  // ===========================
  // AI Recruiter Chat
  // ===========================

  const sendMessage = async (message) => {
    try {
      const res = await api.post("/chat", { message });
      return res.data.answer;
    } catch (err) {
      console.error(err);
      return "Unable to connect to backend.";
    }
  };

  // ===========================
  // UI
  // ===========================

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <main className="flex-1 overflow-y-auto">
        <Header />

        <DashboardContent
          uploadJD={uploadJD}
          uploadResumes={uploadResumes}
          calculateATS={calculateATS}
          atsResults={atsResults}
          sendMessage={sendMessage}
          onView={setSelectedCandidate}
        />
      </main>

      <CandidateDrawer
        candidate={selectedCandidate}
        onClose={() => setSelectedCandidate(null)}
      />
    </div>
  );
}