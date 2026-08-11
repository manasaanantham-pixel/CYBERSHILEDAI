import { useRef, useState } from "react";
import "./Scanner.css";
import { apiFetch } from "./api";

export default function Scanner() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const fileInputRef = useRef(null);

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    setFile(selectedFile);
    setResult(null);
    setError("");
  };

  const startScan = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const data = await apiFetch(
        "/analysis/malware",
        {
          method: "POST",
          body: formData,
        }
      );

      const analysis =
        data.analysis ||
        data.result ||
        data;

      setResult(analysis);
    } catch (err) {
      console.error(
        "Malware Analysis:",
        err
      );

      setError(
        err.message ||
          "Unable to analyze the file."
      );
    } finally {
      setLoading(false);
    }
  };

  const prediction = String(
    result?.prediction ||
      result?.result ||
      "unknown"
  ).toLowerCase();

  const risk = String(
    result?.risk ||
      result?.status ||
      "unknown"
  ).toLowerCase();

  return (
    <section className="scanner-page">
      <div className="scanner-heading">
        <div>
          <div className="card-kicker">
            MALWARE INTELLIGENCE
          </div>

          <h1>AI Malware Scanner</h1>

          <p>
            Upload a suspicious file and let
            CyberShield AI analyze it for
            malicious behavior.
          </p>
        </div>

        <div className="scanner-status">
          <span></span>
          ENGINE READY
        </div>
      </div>

      {error && (
        <div className="scanner-error">
          <span>!</span>
          {error}

          <button
            onClick={() => setError("")}
          >
            ×
          </button>
        </div>
      )}

      <div className="scanner-grid">
        <div className="scanner-upload-card">
          <div
            className="drop-zone"
            onClick={() =>
              fileInputRef.current?.click()
            }
          >
            <input
              ref={fileInputRef}
              type="file"
              onChange={(e) =>
                handleFile(e.target.files?.[0])
              }
              hidden
            />

            <div className="upload-icon">
              ↑
            </div>

            <h2>
              {file
                ? file.name
                : "Upload suspicious file"}
            </h2>

            <p>
              Click to browse your computer
            </p>

            <span>
              EXE • DLL • ZIP • PDF • DOC
            </span>
          </div>

          {file && (
            <div className="selected-file">
              <div>
                <strong>
                  Selected file
                </strong>

                <span>
                  {(file.size / 1024).toFixed(1)} KB
                </span>
              </div>

              <button
                onClick={() => {
                  setFile(null);
                  setResult(null);
                }}
              >
                Remove
              </button>
            </div>
          )}

          <button
            className="scanner-button"
            onClick={startScan}
            disabled={!file || loading}
          >
            {loading
              ? "Analyzing file..."
              : "Run AI Malware Scan →"}
          </button>
        </div>

        <div className="scanner-result-card">
          <div className="card-kicker">
            ANALYSIS RESULT
          </div>

          {!result ? (
            <div className="scanner-empty">
              <div className="scanner-empty-icon">
                ◈
              </div>

              <h3>
                Waiting for scan
              </h3>

              <p>
                Upload a file and start an
                AI-powered malware analysis.
              </p>
            </div>
          ) : (
            <div className="scanner-result">
              <div
                className={`result-orb ${prediction}`}
              >
                {prediction === "malware"
                  ? "!"
                  : prediction === "safe" ||
                    prediction === "legitimate"
                  ? "✓"
                  : "?"}
              </div>

              <div
                className={`prediction-label ${prediction}`}
              >
                {prediction.toUpperCase()}
              </div>

              <div className="risk-label">
                Risk level:{" "}
                <strong>
                  {risk.toUpperCase()}
                </strong>
              </div>

              {result.confidence != null && (
                <div className="confidence-box">
                  <div>
                    <span>
                      AI CONFIDENCE
                    </span>

                    <strong>
                      {result.confidence}%
                    </strong>
                  </div>

                  <div className="confidence-bar">
                    <span
                      style={{
                        width: `${Math.min(
                          Number(
                            result.confidence
                          ) || 0,
                          100
                        )}%`,
                      }}
                    ></span>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
