import { useState } from "react";
import "./Auth.css";
import { API_URL } from "./api";

export default function Auth({ onLogin, onBack }) {
  const [mode, setMode] = useState("login");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const switchMode = (newMode) => {
    setMode(newMode);
    setError("");
    setSuccess("");
    setPassword("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const cleanEmail = email.trim().toLowerCase();

      if (!cleanEmail) {
        throw new Error("Please enter your email.");
      }

      if (password.length < 6) {
        throw new Error(
          "Password must contain at least 6 characters."
        );
      }

      if (mode === "signup" && !name.trim()) {
        throw new Error("Please enter your name.");
      }

      const endpoint =
        mode === "login"
          ? "/auth/login"
          : "/auth/signup";

      const body =
        mode === "login"
          ? {
              email: cleanEmail,
              password,
            }
          : {
              name: name.trim(),
              email: cleanEmail,
              password,
            };

      const response = await fetch(
        `${API_URL}${endpoint}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify(body),
        }
      );

      const text = await response.text();

      let data = {};

      try {
        data = JSON.parse(text);
      } catch {
        throw new Error(
          "Backend returned invalid JSON."
        );
      }

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            "Authentication failed."
        );
      }

      const token = data.access_token;

      if (!token) {
        throw new Error(
          "Login succeeded but backend did not return an access token."
        );
      }

      const loggedInUser = data.user;

      if (!loggedInUser) {
        throw new Error(
          "Backend did not return user information."
        );
      }

      localStorage.setItem(
        "access_token",
        token
      );

      localStorage.setItem(
        "user",
        JSON.stringify(loggedInUser)
      );

      setSuccess(
        mode === "login"
          ? "Login successful."
          : "Account created successfully."
      );

      setTimeout(() => {
        onLogin(loggedInUser);
      }, 400);
    } catch (err) {
      console.error(
        "CYBERSHIELD AUTH ERROR:",
        err
      );

      if (
        err.message.includes("Failed to fetch")
      ) {
        setError(
          "Unable to connect to CyberShield AI server. Start FastAPI first."
        );
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <section className="auth-left">
        <button
          type="button"
          className="auth-back"
          onClick={onBack}
        >
          ← Back
        </button>

        <div className="auth-brand">
          <div className="auth-brand-icon">
            ✦
          </div>

          <span>
            CyberShield <b>AI</b>
          </span>
        </div>

        <div className="auth-badge">
          <span className="auth-pulse"></span>
          INTELLIGENT SECURITY PLATFORM
        </div>

        <h1>
          Secure your
          <br />
          <span>digital world.</span>
        </h1>

        <p>
          Protect your Gmail with AI-powered email
          security. CyberShield AI identifies spam,
          phishing and malicious content.
        </p>

        <div className="auth-features">
          <div>
            <span>✓</span>
            AI-powered email threat analysis
          </div>

          <div>
            <span>✓</span>
            Spam and phishing detection
          </div>

          <div>
            <span>✓</span>
            Secure Gmail integration
          </div>

          <div>
            <span>✓</span>
            JWT-based authentication
          </div>
        </div>

        <div className="auth-left-footer">
          <span className="footer-dot"></span>
          CYBERSHIELD AI SECURITY ENGINE ONLINE
        </div>
      </section>

      <section className="auth-right">
        <div className="auth-card">
          <div className="mobile-brand">
            <div className="auth-brand-icon">
              ✦
            </div>

            <span>
              CyberShield <b>AI</b>
            </span>
          </div>

          <div className="auth-card-header">
            <div className="auth-card-label">
              {mode === "login"
                ? "SECURE LOGIN"
                : "CREATE ACCOUNT"}
            </div>

            <h2>
              {mode === "login"
                ? "Welcome back"
                : "Create your account"}
            </h2>

            <p>
              {mode === "login"
                ? "Login to access your CyberShield AI security dashboard."
                : "Create your account and start protecting your email."}
            </p>
          </div>

          <div className="auth-switch">
            <button
              type="button"
              className={
                mode === "login"
                  ? "active"
                  : ""
              }
              onClick={() =>
                switchMode("login")
              }
            >
              Login
            </button>

            <button
              type="button"
              className={
                mode === "signup"
                  ? "active"
                  : ""
              }
              onClick={() =>
                switchMode("signup")
              }
            >
              Sign Up
            </button>
          </div>

          {error && (
            <div className="auth-message auth-error">
              <div className="message-icon">
                !
              </div>

              <div>
                <strong>
                  Authentication failed
                </strong>

                <p>{error}</p>
              </div>
            </div>
          )}

          {success && (
            <div className="auth-message auth-success">
              <div className="message-icon">
                ✓
              </div>

              <div>
                <strong>Success</strong>
                <p>{success}</p>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {mode === "signup" && (
              <div className="form-group">
                <label htmlFor="name">
                  FULL NAME
                </label>

                <input
                  id="name"
                  type="text"
                  placeholder="Enter your full name"
                  value={name}
                  onChange={(e) =>
                    setName(e.target.value)
                  }
                  disabled={loading}
                  autoComplete="name"
                />
              </div>
            )}

            <div className="form-group">
              <label htmlFor="email">
                EMAIL ADDRESS
              </label>

              <input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) =>
                  setEmail(e.target.value)
                }
                disabled={loading}
                autoComplete="email"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">
                PASSWORD
              </label>

              <input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) =>
                  setPassword(e.target.value)
                }
                disabled={loading}
                autoComplete={
                  mode === "login"
                    ? "current-password"
                    : "new-password"
                }
              />
            </div>

            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >
              {loading
                ? "Please wait..."
                : mode === "login"
                ? "Login to Dashboard"
                : "Create Account"}

              {!loading && (
                <span>→</span>
              )}
            </button>
          </form>

          <div className="auth-bottom-text">
            {mode === "login"
              ? "Don't have an account?"
              : "Already have an account?"}

            <button
              type="button"
              onClick={() =>
                switchMode(
                  mode === "login"
                    ? "signup"
                    : "login"
                )
              }
            >
              {mode === "login"
                ? "Sign Up"
                : "Login"}
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
