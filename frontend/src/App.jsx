import { useEffect, useState } from "react";
import Auth from "./Auth";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const emptySummary = {
  safe: 0,
  spam: 0,
  phishing: 0,
  malware: 0,
  unknown: 0,
};

function App() {
  // =========================================================
  // USER
  // =========================================================

  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("user");

    try {
      return savedUser ? JSON.parse(savedUser) : null;
    } catch {
      return null;
    }
  });

  const [showAuth, setShowAuth] = useState(false);

  // =========================================================
  // GMAIL
  // =========================================================

  const [gmailConnected, setGmailConnected] = useState(false);
  const [gmailEmail, setGmailEmail] = useState("");
  const [emails, setEmails] = useState([]);
  const [summary, setSummary] = useState(emptySummary);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // =========================================================
  // LOGIN
  // =========================================================

  const handleLogin = (loggedInUser) => {
    setUser(loggedInUser);
    setShowAuth(false);
  };

  // =========================================================
  // LOGOUT
  // =========================================================

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    setUser(null);
    setShowAuth(false);

    setGmailConnected(false);
    setGmailEmail("");
    setEmails([]);
    setSummary(emptySummary);

    setMessage("");
    setError("");
  };

  // =========================================================
  // CONNECT GMAIL
  // =========================================================

  const connectGmail = async () => {
    try {
      setLoading(true);
      setMessage("");
      setError("");

      const response = await fetch(`${API_URL}/gmail/connect`, {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      });

      const text = await response.text();

      if (!response.ok) {
        throw new Error(`Server error ${response.status}: ${text}`);
      }

      let data;

      try {
        data = JSON.parse(text);
      } catch {
        throw new Error("Backend returned invalid JSON.");
      }

      if (data.auth_url) {
        window.location.href = data.auth_url;
        return;
      }

      if (data.connected === true) {
        setGmailConnected(true);
        setGmailEmail(data.email || "");

        setMessage(
          data.email
            ? `Gmail connected successfully — ${data.email}`
            : "Gmail connected successfully."
        );

        await analyzeGmail();
        return;
      }

      throw new Error(
        data.detail || "Gmail connection was not completed."
      );
    } catch (err) {
      console.error("GMAIL CONNECTION ERROR:", err);

      setError(
        `Unable to connect to CyberShield AI server.\n${err.message}`
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // ANALYZE GMAIL
  // =========================================================

  const analyzeGmail = async () => {
    try {
      setLoading(true);
      setMessage("");
      setError("");

      const response = await fetch(
        `${API_URL}/analysis/gmail?limit=20`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
          },
        }
      );

      const text = await response.text();

      if (!response.ok) {
        throw new Error(`Analysis error ${response.status}: ${text}`);
      }

      let data;

      try {
        data = JSON.parse(text);
      } catch {
        throw new Error("Analysis endpoint returned invalid JSON.");
      }

      if (!data.success) {
        throw new Error(data.detail || "Gmail analysis failed.");
      }

      setEmails(Array.isArray(data.emails) ? data.emails : []);

      setSummary({
        ...emptySummary,
        ...(data.summary || {}),
      });

      setMessage(
        `${data.count || 0} Gmail messages analyzed successfully.`
      );
    } catch (err) {
      console.error("GMAIL ANALYSIS ERROR:", err);

      setError(`Gmail analysis failed.\n${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // CHECK GMAIL STATUS
  // =========================================================

  useEffect(() => {
    if (!user) return;

    const checkGmailStatus = async () => {
      try {
        const response = await fetch(`${API_URL}/gmail/messages`, {
          method: "GET",
          headers: {
            Accept: "application/json",
          },
        });

        if (!response.ok) return;

        const data = await response.json();

        if (data && Array.isArray(data.messages)) {
          setGmailConnected(true);

          if (data.email) {
            setGmailEmail(data.email);
          }
        }
      } catch (err) {
        console.log("Gmail status:", err.message);
      }
    };

    checkGmailStatus();
  }, [user]);

  // =========================================================
  // AUTH PAGE
  // =========================================================

  if (showAuth && !user) {
    return (
      <Auth
        onLogin={handleLogin}
        onBack={() => setShowAuth(false)}
      />
    );
  }

  // =========================================================
  // DASHBOARD
  // =========================================================

  if (user) {
    const totalScanned =
      summary.safe +
      summary.spam +
      summary.phishing +
      summary.malware +
      summary.unknown;

    return (
      <div className="dashboard-page">
        {/* TOP NAVBAR */}

        <header className="dashboard-navbar">
          <div className="brand">
            <div className="brand-icon">
              <span>✦</span>
            </div>

            <div className="brand-name">
              CyberShield <b>AI</b>
            </div>
          </div>

          <div className="dashboard-nav-right">
            <div className="system-status">
              <span className="status-dot"></span>
              AI ENGINE ONLINE
            </div>

            <div className="user-profile">
              <div className="avatar">
                {user.name?.charAt(0)?.toUpperCase() || "U"}
              </div>

              <div className="profile-text">
                <strong>{user.name}</strong>
                <span>{user.email}</span>
              </div>
            </div>

            <button
              className="logout-button"
              onClick={handleLogout}
            >
              Logout
            </button>
          </div>
        </header>

        <main className="dashboard-content">
          {/* HEADER */}

          <section className="dashboard-header">
            <div>
              <div className="eyebrow">
                <span className="eyebrow-line"></span>
                SECURITY COMMAND CENTER
              </div>

              <h1>
                Good to see you,{" "}
                <span>{user.name?.split(" ")[0]}</span>.
              </h1>

              <p>
                Monitor your inbox and identify suspicious email
                activity with CyberShield AI.
              </p>
            </div>

            <div className="dashboard-time">
              <span>PROTECTION STATUS</span>

              <strong>
                <i></i>
                ACTIVE
              </strong>
            </div>
          </section>

          {/* ALERTS */}

          {message && (
            <div className="dashboard-alert success-alert">
              <span className="alert-icon">✓</span>
              <span>{message}</span>
              <button onClick={() => setMessage("")}>×</button>
            </div>
          )}

          {error && (
            <div className="dashboard-alert error-alert">
              <span className="alert-icon">!</span>
              <span>{error}</span>
              <button onClick={() => setError("")}>×</button>
            </div>
          )}

          {/* GMAIL CONNECTION */}

          <section className="gmail-security-card">
            <div className="gmail-card-glow"></div>

            <div className="gmail-card-content">
              <div className="gmail-card-icon">
                <span>✉</span>
              </div>

              <div className="gmail-card-info">
                <div className="card-kicker">
                  EMAIL PROTECTION
                </div>

                <h2>Secure your Gmail inbox</h2>

                <p>
                  Connect your Gmail account and let our AI engine
                  scan messages for phishing, spam and malicious
                  content.
                </p>

                {gmailConnected && (
                  <div className="connected-account">
                    <span className="connected-dot"></span>
                    Connected
                    {gmailEmail && (
                      <strong>{gmailEmail}</strong>
                    )}
                  </div>
                )}
              </div>

              <div className="gmail-card-action">
                {!gmailConnected ? (
                  <button
                    className="primary-action"
                    onClick={connectGmail}
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="button-spinner"></span>
                        Connecting
                      </>
                    ) : (
                      <>
                        Connect Gmail
                        <span>→</span>
                      </>
                    )}
                  </button>
                ) : (
                  <button
                    className="primary-action"
                    onClick={analyzeGmail}
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="button-spinner"></span>
                        Scanning
                      </>
                    ) : (
                      <>
                        Run AI Scan
                        <span>→</span>
                      </>
                    )}
                  </button>
                )}

                <small>
                  Secure Google authorization
                </small>
              </div>
            </div>
          </section>

          {/* STATISTICS */}

          <section className="dashboard-stats">
            <div className="stat-card total">
              <div className="stat-top">
                <span className="stat-icon">◉</span>
                <span className="stat-label">TOTAL SCANNED</span>
              </div>

              <strong>{totalScanned}</strong>

              <small>Messages analyzed</small>
            </div>

            <div className="stat-card safe">
              <div className="stat-top">
                <span className="stat-icon">✓</span>
                <span className="stat-label">SAFE</span>
              </div>

              <strong>{summary.safe}</strong>

              <small>Clean messages</small>
            </div>

            <div className="stat-card phishing">
              <div className="stat-top">
                <span className="stat-icon">!</span>
                <span className="stat-label">PHISHING</span>
              </div>

              <strong>{summary.phishing}</strong>

              <small>Threats detected</small>
            </div>

            <div className="stat-card danger">
              <div className="stat-top">
                <span className="stat-icon">⚠</span>
                <span className="stat-label">SPAM / MALWARE</span>
              </div>

              <strong>
                {summary.spam + summary.malware}
              </strong>

              <small>Suspicious messages</small>
            </div>
          </section>

          {/* RESULTS */}

          <section className="results-panel">
            <div className="results-header">
              <div>
                <div className="card-kicker">
                  AI SECURITY ENGINE
                </div>

                <h2>Email threat intelligence</h2>

                <p>
                  AI classification results from your connected
                  Gmail account.
                </p>
              </div>

              <div className="engine-badge">
                <span></span>
                ENGINE ONLINE
              </div>
            </div>

            {emails.length === 0 ? (
              <div className="empty-results">
                <div className="empty-icon">⌁</div>

                <h3>Your security feed is ready</h3>

                <p>
                  Connect Gmail and run an AI scan to see
                  analyzed messages here.
                </p>

                {!gmailConnected && (
                  <button
                    onClick={connectGmail}
                    disabled={loading}
                  >
                    Connect Gmail →
                  </button>
                )}
              </div>
            ) : (
              <div className="email-list">
                {emails.map((email, index) => {
                  const prediction = (
                    email.prediction || "unknown"
                  ).toLowerCase();

                  const risk = (
                    email.risk || "unknown"
                  ).toLowerCase();

                  let statusClass = "safe";

                  if (prediction === "phishing") {
                    statusClass = "phishing";
                  } else if (prediction === "spam") {
                    statusClass = "spam";
                  } else if (prediction === "malware") {
                    statusClass = "malware";
                  } else if (prediction === "unknown") {
                    statusClass = "unknown";
                  }

                  return (
                    <div
                      className="email-result"
                      key={email.id || index}
                    >
                      <div
                        className={`email-status-icon ${statusClass}`}
                      >
                        {prediction === "safe" ? "✓" : "!"}
                      </div>

                      <div className="email-details">
                        <div className="email-title-row">
                          <h3>
                            {email.subject || "No subject"}
                          </h3>

                          <span
                            className={`prediction-badge ${statusClass}`}
                          >
                            {prediction.toUpperCase()}
                          </span>
                        </div>

                        <div className="email-meta">
                          <span>
                            From:{" "}
                            <strong>
                              {email.sender || "Unknown sender"}
                            </strong>
                          </span>

                          {email.date && (
                            <span>{email.date}</span>
                          )}
                        </div>

                        {email.reasons &&
                          email.reasons.length > 0 && (
                            <div className="email-reasons">
                              <span>AI indicators:</span>

                              {email.reasons
                                .slice(0, 3)
                                .map((reason, i) => (
                                  <em key={i}>{reason}</em>
                                ))}
                            </div>
                          )}
                      </div>

                      <div className="email-score">
                        <span className={`risk-badge ${risk}`}>
                          {risk.toUpperCase()} RISK
                        </span>

                        <strong>
                          {email.confidence != null
                            ? `${email.confidence}%`
                            : "N/A"}
                        </strong>

                        <small>confidence</small>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </section>

          {/* ACCOUNT */}

          <section className="account-section">
            <div className="account-section-title">
              <div className="card-kicker">ACCOUNT</div>
              <h2>Workspace information</h2>
            </div>

            <div className="account-grid">
              <div>
                <span>USER</span>
                <strong>{user.name}</strong>
              </div>

              <div>
                <span>EMAIL</span>
                <strong>{user.email}</strong>
              </div>

              <div>
                <span>GMAIL</span>
                <strong>
                  {gmailConnected ? "CONNECTED" : "NOT CONNECTED"}
                </strong>
              </div>

              <div>
                <span>PROTECTION</span>
                <strong className="active-text">
                  ACTIVE
                </strong>
              </div>
            </div>
          </section>
        </main>

        <footer className="dashboard-footer">
          <div className="brand">
            <div className="brand-icon">
              <span>✦</span>
            </div>

            <div className="brand-name">
              CyberShield <b>AI</b>
            </div>
          </div>

          <span>
            AI-powered email security • 2026
          </span>
        </footer>
      </div>
    );
  }

  // =========================================================
  // LANDING PAGE
  // =========================================================

  return (
    <div className="app">
      {/* NAVBAR */}

      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">
            <span>✦</span>
          </div>

          <div className="brand-name">
            CyberShield <b>AI</b>
          </div>
        </div>

        <nav className="nav-links">
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
          <a href="#about">About</a>
        </nav>

        <div className="nav-actions">
          <button
            className="login-button"
            onClick={() => setShowAuth(true)}
          >
            Log in
          </button>

          <button
            className="get-started-button"
            onClick={() => setShowAuth(true)}
          >
            Get Started
            <span>→</span>
          </button>
        </div>
      </header>

      {/* HERO */}

      <main>
        <section className="hero">
          <div className="hero-content">
            <div className="security-badge">
              <span className="pulse-dot"></span>
              AI-POWERED EMAIL SECURITY
            </div>

            <h1>
              Detect threats.
              <br />
              <span>Protect every email.</span>
            </h1>

            <p className="hero-description">
              CyberShield AI connects to your Gmail inbox and
              intelligently analyzes messages for phishing, spam,
              malware and suspicious activity.
            </p>

            <div className="hero-actions">
              <button
                className="primary-button"
                onClick={() => setShowAuth(true)}
              >
                Protect My Gmail
                <span>→</span>
              </button>

              <a
                href="#features"
                className="secondary-button"
              >
                Explore Platform
              </a>
            </div>

            <div className="trust-stats">
              <div>
                <strong>99.1%</strong>
                <span>Model Accuracy</span>
              </div>

              <div className="stat-divider"></div>

              <div>
                <strong>AI</strong>
                <span>Threat Analysis</span>
              </div>

              <div className="stat-divider"></div>

              <div>
                <strong>24/7</strong>
                <span>Protection</span>
              </div>
            </div>
          </div>

          {/* HERO SECURITY PANEL */}

          <div className="scanner-area">
            <div className="scanner-card">
              <div className="scanner-grid"></div>

              <div className="scanner-top">
                <div>
                  <small>CYBERSHIELD SECURITY ENGINE</small>
                  <h3>Live Threat Monitor</h3>
                </div>

                <div className="live-indicator">
                  <span></span>
                  LIVE
                </div>
              </div>

              <div className="scanner-circle">
                <div className="circle-orbit orbit-one"></div>
                <div className="circle-orbit orbit-two"></div>
                <div className="circle-ring"></div>

                <div className="scanner-center">
                  <div className="big-shield">✦</div>

                  <strong>PROTECTED</strong>

                  <span>AI engine active</span>
                </div>
              </div>

              <div className="scan-stat-row">
                <div>
                  <span>Threat Detection</span>
                  <strong>ACTIVE</strong>
                </div>

                <div>
                  <span>AI Classification</span>
                  <strong>ON</strong>
                </div>
              </div>

              <div className="protection-bar">
                <div className="protection-header">
                  <span>Gmail Protection</span>
                  <b>READY</b>
                </div>

                <div className="progress">
                  <div></div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* FEATURES */}

        <section id="features" className="section">
          <div className="section-heading">
            <span>SECURITY INTELLIGENCE</span>

            <h2>
              Built for modern email threats.
            </h2>

            <p>
              One intelligent platform for identifying
              suspicious messages before they become a problem.
            </p>
          </div>

          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-number">01</div>

              <div className="feature-icon">⌁</div>

              <h3>AI Email Detection</h3>

              <p>
                Machine learning analyzes message content and
                identifies suspicious patterns and threat
                indicators.
              </p>

              <span className="feature-link">
                Intelligent analysis →
              </span>
            </div>

            <div className="feature-card">
              <div className="feature-number">02</div>

              <div className="feature-icon">↯</div>

              <h3>Automatic Scanning</h3>

              <p>
                Connect Gmail and scan available messages
                without manually copying or uploading email
                content.
              </p>

              <span className="feature-link">
                Automated protection →
              </span>
            </div>

            <div className="feature-card">
              <div className="feature-number">03</div>

              <div className="feature-icon">◇</div>

              <h3>Threat Intelligence</h3>

              <p>
                Get clear SAFE, SPAM, PHISHING and MALWARE
                classifications with risk and confidence.
              </p>

              <span className="feature-link">
                Clear security insights →
              </span>
            </div>
          </div>
        </section>

        {/* HOW IT WORKS */}

        <section
          id="how-it-works"
          className="section workflow-section"
        >
          <div className="section-heading">
            <span>HOW IT WORKS</span>

            <h2>
              Protection without the complexity.
            </h2>

            <p>
              Connect once. Let AI handle the analysis.
            </p>
          </div>

          <div className="workflow">
            <div className="workflow-line"></div>

            <div className="workflow-step">
              <div className="workflow-number">01</div>

              <h3>Connect Gmail</h3>

              <p>
                Authorize your Gmail account through secure
                Google authentication.
              </p>
            </div>

            <div className="workflow-step">
              <div className="workflow-number">02</div>

              <h3>AI Analyzes</h3>

              <p>
                CyberShield AI evaluates message content and
                suspicious indicators.
              </p>
            </div>

            <div className="workflow-step">
              <div className="workflow-number">03</div>

              <h3>See Results</h3>

              <p>
                Review security classifications, risk levels
                and AI confidence.
              </p>
            </div>
          </div>
        </section>

        {/* ABOUT */}

        <section id="about" className="section about-section">
          <div className="about-box">
            <div className="about-visual">
              <div className="about-orbit"></div>
              <div className="about-symbol">✦</div>
            </div>

            <div className="about-content">
              <span>ABOUT CYBERSHIELD AI</span>

              <h2>
                Intelligent security for a safer digital world.
              </h2>

              <p>
                CyberShield AI combines Gmail integration,
                machine learning and automated threat analysis
                to help identify phishing, spam and malicious
                email activity.
              </p>

              <div className="about-points">
                <span>✓ Machine learning powered</span>
                <span>✓ Gmail integrated</span>
                <span>✓ Risk-based classification</span>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* FOOTER */}

      <footer className="footer">
        <div className="brand">
          <div className="brand-icon">
            <span>✦</span>
          </div>

          <div className="brand-name">
            CyberShield <b>AI</b>
          </div>
        </div>

        <p>
          © 2026 CyberShield AI. Intelligent email security.
        </p>

        <span className="footer-status">
          ● SYSTEM OPERATIONAL
        </span>
      </footer>
    </div>
  );
}

export default App;
