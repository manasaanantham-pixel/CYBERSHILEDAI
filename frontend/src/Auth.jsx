import { useState } from "react";
import "./Auth.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function Auth({ onLogin, onBack }) {
  const [mode, setMode] = useState("login");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const clearMessages = () => {
    setError("");
    setSuccess("");
  };

  const switchMode = (newMode) => {
    setMode(newMode);
    clearMessages();
    setPassword("");

    if (newMode === "login") {
      setName("");
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    clearMessages();

    const cleanEmail = email.trim().toLowerCase();
    const cleanName = name.trim();

    if (!cleanEmail || !password) {
      setError("Please enter your email and password.");
      return;
    }

    if (mode === "signup" && !cleanName) {
      setError("Please enter your full name.");
      return;
    }

    if (password.length < 6) {
      setError("Password must contain at least 6 characters.");
      return;
    }

    setLoading(true);

    try {
      const endpoint =
        mode === "signup"
          ? `${API_BASE_URL}/auth/signup`
          : `${API_BASE_URL}/auth/login`;

      const requestBody =
        mode === "signup"
          ? {
              name: cleanName,
              email: cleanEmail,
              password: password,
            }
          : {
              email: cleanEmail,
              password: password,
            };

      console.log("CyberShield API:", endpoint);

      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const responseText = await response.text();

      let data = {};

      try {
        data = responseText ? JSON.parse(responseText) : {};
      } catch {
        throw new Error(
          "Backend returned an invalid response. Please make sure FastAPI is running."
        );
      }

      console.log("Backend status:", response.status);
      console.log("Backend response:", data);

      if (!response.ok) {
        let backendError =
          data.detail ||
          data.message ||
          data.error ||
          "Authentication failed.";

        // FastAPI sometimes returns validation errors as an array
        if (Array.isArray(backendError)) {
          backendError = backendError
            .map((item) => item.msg || "Invalid input")
            .join(", ");
        }

        const errorText = String(backendError);

        // Duplicate email
        if (
          errorText.toLowerCase().includes("already registered") ||
          errorText.toLowerCase().includes("already exists") ||
          errorText.toLowerCase().includes("email already")
        ) {
          setError(
            "This email is already registered. Please login instead."
          );

          setMode("login");
          return;
        }

        // Wrong login details
        if (
          errorText.toLowerCase().includes("incorrect") ||
          errorText.toLowerCase().includes("invalid credentials") ||
          errorText.toLowerCase().includes("wrong password")
        ) {
          setError(
            "Incorrect email or password. Please try again."
          );
          return;
        }

        throw new Error(errorText);
      }

      // ==========================================
      // SIGN UP SUCCESS
      // ==========================================

      if (mode === "signup") {
        setSuccess(
          "Account created successfully. Please login."
        );

        setPassword("");

        setTimeout(() => {
          setMode("login");
          setSuccess("");
        }, 1200);

        return;
      }

      // ==========================================
      // LOGIN SUCCESS
      // ==========================================

      const token =
        data.access_token ||
        data.token ||
        data.accessToken;

      if (token) {
        localStorage.setItem("access_token", token);
      }

      const loggedInUser =
        data.user ||
        {
          name:
            data.name ||
            cleanName ||
            cleanEmail.split("@")[0],
          email:
            data.email ||
            cleanEmail,
        };

      localStorage.setItem(
        "user",
        JSON.stringify(loggedInUser)
      );

      setSuccess("Login successful.");

      // Give UI a moment to show success message
      setTimeout(() => {
        onLogin(loggedInUser);
      }, 300);

    } catch (err) {
      console.error("CYBERSHIELD AUTH ERROR:", err);

      if (
        err.message.includes("Failed to fetch") ||
        err.message.includes("NetworkError")
      ) {
        setError(
          "Unable to connect to CyberShield AI server. Make sure FastAPI is running on http://127.0.0.1:8000"
        );
      } else {
        setError(
          err.message || "Something went wrong. Please try again."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">

      {/* =========================================
          LEFT PANEL
      ========================================= */}

      <section className="auth-left">

        <button
          type="button"
          className="auth-back"
          onClick={onBack}
        >
          ← Back to CyberShield
        </button>

        <div className="auth-left-content">

          <div className="auth-brand">
            <div className="auth-brand-icon">
              🛡️
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
            security. CyberShield AI helps identify
            spam, phishing and malicious content before
            it becomes a threat.
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

        </div>

        <div className="auth-left-footer">
          <span>●</span> CYBERSHIELD AI SECURITY ENGINE ONLINE
        </div>

      </section>

      {/* =========================================
          RIGHT PANEL
      ========================================= */}

      <section className="auth-right">

        <div className="auth-card">

          {/* MOBILE BRAND */}

          <div className="mobile-brand">
            <div className="auth-brand-icon">
              🛡️
            </div>

            <span>
              CyberShield <b>AI</b>
            </span>
          </div>

          {/* HEADER */}

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

          {/* MODE SWITCH */}

          <div className="auth-switch">

            <button
              type="button"
              className={mode === "login" ? "active" : ""}
              onClick={() => switchMode("login")}
            >
              Login
            </button>

            <button
              type="button"
              className={mode === "signup" ? "active" : ""}
              onClick={() => switchMode("signup")}
            >
              Sign Up
            </button>

          </div>

          {/* ERROR */}

          {error && (
            <div className="auth-message auth-error">
              <div className="message-icon">!</div>

              <div>
                <strong>Authentication failed</strong>
                <p>{error}</p>

                {error.includes("already registered") && (
                  <button
                    type="button"
                    className="message-action"
                    onClick={() => switchMode("login")}
                  >
                    Go to Login →
                  </button>
                )}
              </div>
            </div>
          )}

          {/* SUCCESS */}

          {success && (
            <div className="auth-message auth-success">
              <div className="message-icon">✓</div>

              <div>
                <strong>Success</strong>
                <p>{success}</p>
              </div>
            </div>
          )}

          {/* FORM */}

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
                  autoComplete="name"
                  disabled={loading}
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
                autoComplete="email"
                disabled={loading}
              />

            </div>

            <div className="form-group">

              <div className="password-header">
                <label htmlFor="password">
                  PASSWORD
                </label>
              </div>

              <input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) =>
                  setPassword(e.target.value)
                }
                autoComplete={
                  mode === "login"
                    ? "current-password"
                    : "new-password"
                }
                disabled={loading}
              />

            </div>

            {mode === "signup" && (
              <div className="password-help">
                Password must contain at least 6 characters.
              </div>
            )}

            {/* SUBMIT */}

            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Please wait...
                </>
              ) : (
                <>
                  {mode === "login"
                    ? "Login to Dashboard"
                    : "Create Account"}

                  <span>→</span>
                </>
              )}
            </button>

          </form>

          {/* BOTTOM SWITCH */}

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
                ? "Create one"
                : "Login"}
            </button>

          </div>

          {/* SECURITY */}

          <div className="auth-security">

            <div className="security-icon">
              🔒
            </div>

            <div>
              <strong>
                Secure authentication
              </strong>

              <p>
                Your credentials are protected using
                secure password hashing and JWT
                authentication.
              </p>
            </div>

          </div>

        </div>

      </section>

    </div>
  );
}

export default Auth;
