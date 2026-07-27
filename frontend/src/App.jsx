import { useState } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("Welcome to HireMate AI 🚀");

  const [jdFile, setJdFile] = useState(null);
  const [resumeFiles, setResumeFiles] = useState([]);

  // Upload Job Description
  const uploadJD = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setJdFile(file);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8001/upload-jd",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      alert(res.data.message);
    } catch (err) {
      console.error(err);
      alert("JD Upload Failed");
    }
  };

  // Upload Resumes
  const uploadResumes = async (event) => {
    const files = Array.from(event.target.files);

    if (files.length === 0) return;

    setResumeFiles(files);

    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const res = await axios.post(
        "http://127.0.0.1:8001/upload-resumes",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      alert(res.data.message);
    } catch (err) {
      console.error(err);
      alert("Resume Upload Failed");
    }
  };

  // Analyze
  const sendMessage = async () => {
    if (!message.trim()) return;

    try {
      const res = await axios.post(
        "http://127.0.0.1:8001/analyze",
        {
          question: message,
        }
      );

      setReply(res.data.analysis);
      setMessage("");
    } catch (err) {
      console.error(err);
      setReply("Backend connection failed.");
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h1>HireMate AI</h1>

        <div className="upload">
          <label>Upload Job Description</label>
          <input
            type="file"
            accept=".pdf,.doc,.docx,.txt"
            onChange={uploadJD}
          />

          {jdFile && (
            <p>
              <b>Selected:</b> {jdFile.name}
            </p>
          )}
        </div>

        <div className="upload">
          <label>Upload Resumes</label>
          <input
            type="file"
            multiple
            accept=".pdf,.doc,.docx,.txt"
            onChange={uploadResumes}
          />

          {resumeFiles.length > 0 && (
            <div>
              <p>
                <b>Uploaded Resumes:</b>
              </p>

              <ul>
                {resumeFiles.map((file, index) => (
                  <li key={index}>{file.name}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className="chat">
          <div className="messages">
            <p>
              <b>AI:</b>
            </p>

            <pre
              style={{
                whiteSpace: "pre-wrap",
                fontFamily: "inherit",
                textAlign: "left",
              }}
            >
              {reply}
            </pre>
          </div>

          <div className="input-area">
            <input
              type="text"
              placeholder="Ask anything..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />

            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      </div>
    </div>
  );
}