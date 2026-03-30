import React, { useState } from "react";
import "./App.css";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const upload = async (file, type) => {
    setLoading(true);

    const formData = new FormData();
    formData.append(type, file);

    const res = await fetch(`http://localhost:5000/api/analyze-${type}`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="container">
      <h1 className="title">🛡️ DeepShield AI</h1>

      <div className="card">
        <h2>Upload Audio</h2>
        <input
          type="file"
          onChange={(e) => upload(e.target.files[0], "audio")}
        />
      </div>

      <div className="card">
        <h2>Upload Video</h2>
        <input
          type="file"
          onChange={(e) => upload(e.target.files[0], "video")}
        />
      </div>

      {loading && <p className="loading">🔄 Analyzing...</p>}

      {result && (
        <div className="result-card">
          <h2
            className={
              result.result === "FAKE" || result.result === "DEEPFAKE"
                ? "danger"
                : "safe"
            }
          >
            {result.result}
          </h2>

          <p>Confidence: {result.confidence}%</p>
          <div className="bar">
            <div
              className="fill"
              style={{ width: `${result.confidence}%` }}
            ></div>
          </div>

          <p>Risk Level: {result.risk}</p>
          <p>{result.message}</p>
        </div>
      )}
    </div>
  );
}

export default App;