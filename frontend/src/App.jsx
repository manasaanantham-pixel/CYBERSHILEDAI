
<div className="cyber-visual">
  <div className="cyber-core">
    <div className="cyber-shield"></div>
  </div>

  <span className="cyber-node"></span>
  <span className="cyber-node"></span>
  <span className="cyber-node"></span>
  <span className="cyber-node"></span>
  <span className="cyber-node"></span>

  <span className="cyber-line one"></span>
  <span className="cyber-line two"></span>
  <span className="cyber-line three"></span>
  <span className="cyber-line four"></span>

  <div className="cyber-scan"></div>

  <div className="cyber-status">
    AI SECURITY ENGINE ONLINE
  </div>
</div>

import { useEffect, useState } from "react";
import Auth from "./Auth";
import "./App.css";


const API_URL = "https://cybershieldai-gg60.onrender.com";


const emptySummary = {

  safe: 0,

  spam: 0,

  phishing: 0,

  malware: 0,

  unknown: 0

};


async function apiFetch(
  endpoint,
  options = {}
) {

  const token =
    localStorage.getItem(
      "access_token"
    );


  const headers = {

    Accept:
      "application/json",

    ...(options.headers || {})

  };


  if (token) {

    headers.Authorization =
      `Bearer ${token}`;

  }


  const response = await fetch(

    `${API_URL}${endpoint}`,

    {
      ...options,
      headers
    }

  );


  const text =
    await response.text();


  let data = {};

  try {

    data = text
      ? JSON.parse(text)
      : {};

  } catch {

    data = {
      detail: text
    };

  }


  if (response.status === 401) {

    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "user"
    );

    throw new Error(
      "Your session expired. Please login again."
    );

  }


  if (!response.ok) {

    throw new Error(
      data.detail ||
      `Server error ${response.status}`
    );

  }


  return data;

}


function App() {

  const [user, setUser] =
    useState(() => {

      const saved =
        localStorage.getItem(
          "user"
        );

      try {

        return saved
          ? JSON.parse(saved)
          : null;

      } catch {

        return null;

      }

    });


  const [showAuth, setShowAuth] =
    useState(false);


  const [gmailConnected, setGmailConnected] =
    useState(false);


  const [gmailEmail, setGmailEmail] =
    useState("");


  const [emails, setEmails] =
    useState([]);


  const [summary, setSummary] =
    useState(emptySummary);


  const [loading, setLoading] =
    useState(false);


  const [message, setMessage] =
    useState("");


  const [error, setError] =
    useState("");


 

  const handleLogin = (
    loggedInUser
  ) => {

    setUser(
      loggedInUser
    );

    setShowAuth(false);

    setError("");

    setMessage("");

  };



  const handleLogout = () => {

    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "user"
    );


    setUser(null);

    setShowAuth(false);

    setGmailConnected(false);

    setGmailEmail("");

    setEmails([]);

    setSummary(
      emptySummary
    );

    setMessage("");

    setError("");

  };


 

  const checkGmailStatus =
    async () => {

      if (!user) return;


      try {

        const data =
          await apiFetch(
            "/gmail/status"
          );


        if (
          data.connected
        ) {

          setGmailConnected(
            true
          );

          setGmailEmail(
            data.email || ""
          );

        } else {

          setGmailConnected(
            false
          );

          setGmailEmail("");

        }

      } catch (err) {

        console.log(
          "Gmail status:",
          err.message
        );

      }

    };


  

  const connectGmail =
    async () => {

      try {

        setLoading(true);

        setError("");

        setMessage("");


        const data =
          await apiFetch(
            "/gmail/connect"
          );


        if (
          data.connected
        ) {

          setGmailConnected(
            true
          );

          setGmailEmail(
            data.email || ""
          );


          setMessage(
            `Gmail connected successfully — ${data.email}`
          );

        }

      } catch (err) {

        setError(
          err.message
        );

      } finally {

        setLoading(false);

      }

    };




  const switchGmail =
    async () => {

      try {

        setLoading(true);

        setError("");

        setMessage("");


        const data =
          await apiFetch(
            "/gmail/connect?force=true"
          );


        if (
          data.connected
        ) {

          setGmailConnected(
            true
          );

          setGmailEmail(
            data.email || ""
          );


          setEmails([]);

          setSummary(
            emptySummary
          );


          setMessage(
            `Gmail switched successfully — ${data.email}`
          );

        }

      } catch (err) {

        setError(
          err.message
        );

      } finally {

        setLoading(false);

      }

    };


  

  const analyzeGmail =
    async () => {

      try {

        setLoading(true);

        setError("");

        setMessage("");


        const data =
          await apiFetch(
            "/analysis/gmail?limit=20"
          );


        setEmails(
          Array.isArray(
            data.emails
          )
            ? data.emails
            : []
        );


        setSummary({

          ...emptySummary,

          ...(data.summary || {})

        });


        setMessage(
          `${data.count || 0} Gmail messages analyzed successfully.`
        );


      } catch (err) {

        setError(
          `Gmail analysis failed. ${err.message}`
        );

      } finally {

        setLoading(false);

      }

    };




  useEffect(() => {

    if (!user) return;

    checkGmailStatus();

  }, [user]);


  

  if (
    showAuth &&
    !user
  ) {

    return (

      <Auth

        onLogin={
          handleLogin
        }

        onBack={() =>
          setShowAuth(false)
        }

      />

    );

  }




  if (user) {

    const totalScanned =
      summary.safe +
      summary.spam +
      summary.phishing +
      summary.malware +
      summary.unknown;


    return (

      <div className="dashboard-page">

        <header className="dashboard-navbar">

          <div className="brand">

            <div className="brand-icon">
              ✦
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

                {user.name
                  ?.charAt(0)
                  ?.toUpperCase() || "U"}

              </div>


              <div className="profile-text">

                <strong>
                  {user.name}
                </strong>

                <span>
                  {user.email}
                </span>

              </div>

            </div>


            <button
              className="logout-button"
              onClick={
                handleLogout
              }
            >
              Logout
            </button>

          </div>

        </header>


        <main className="dashboard-main">

          <div className="dashboard-heading">

            <div>

              <div className="card-kicker">
                SECURITY COMMAND CENTER
              </div>

              <h1>
                Good to see you,{" "}
                <span>
                  {user.name}.
                </span>
              </h1>

              <p>
                Monitor your inbox and
                identify suspicious email
                activity with CyberShield AI.
              </p>

            </div>


            <div className="protection-status">

              <small>
                PROTECTION STATUS
              </small>

              <strong>
                ● ACTIVE
              </strong>

            </div>

          </div>


          {error && (

            <div className="dashboard-alert">

              <span>!</span>

              <div>
                {error}
              </div>

              <button
                onClick={() =>
                  setError("")
                }
              >
                ×
              </button>

            </div>

          )}


          {message && (

            <div className="dashboard-success">

              ✓ {message}

            </div>

          )}


          {/* GMAIL */}

          <section className="gmail-security-card">

            <div className="gmail-card-content">

              <div className="gmail-card-icon">
                ✉
              </div>


              <div className="gmail-card-info">

                <div className="card-kicker">
                  EMAIL PROTECTION
                </div>

                <h2>
                  Secure your Gmail inbox
                </h2>

                <p>
                  Connect your Gmail account
                  and let our AI engine scan
                  messages for phishing,
                  spam and malicious content.
                </p>


                {gmailConnected && (

                  <div className="connected-account">

                    <span className="connected-dot"></span>

                    Connected

                    <strong>
                      {gmailEmail}
                    </strong>

                  </div>

                )}

              </div>


              <div className="gmail-card-action">

                {!gmailConnected ? (

                  <button
                    className="primary-action"
                    onClick={
                      connectGmail
                    }
                    disabled={loading}
                  >

                    {loading
                      ? "Connecting..."
                      : "Connect Gmail →"}

                  </button>

                ) : (

                  <div className="gmail-actions">

                    <button
                      className="primary-action"
                      onClick={
                        analyzeGmail
                      }
                      disabled={loading}
                    >

                      {loading
                        ? "Scanning..."
                        : "Run AI Scan →"}

                    </button>


                    <button
                      className="secondary-action"
                      onClick={
                        switchGmail
                      }
                      disabled={loading}
                    >
                      Switch Gmail
                    </button>

                  </div>

                )}

                <small>
                  Secure Google authorization
                </small>

              </div>

            </div>

          </section>


          {/* STATISTICS */}

          <section className="dashboard-stats">

            <div className="stat-card">

              <span>
                TOTAL SCANNED
              </span>

              <strong>
                {totalScanned}
              </strong>

              <small>
                Messages analyzed
              </small>

            </div>


            <div className="stat-card">

              <span>
                SAFE
              </span>

              <strong>
                {summary.safe}
              </strong>

              <small>
                Clean messages
              </small>

            </div>


            <div className="stat-card">

              <span>
                PHISHING
              </span>

              <strong>
                {summary.phishing}
              </strong>

              <small>
                Threats detected
              </small>

            </div>


            <div className="stat-card">

              <span>
                SPAM / MALWARE
              </span>

              <strong>
                {summary.spam +
                  summary.malware}
              </strong>

              <small>
                Suspicious messages
              </small>

            </div>

          </section>


          {/* RESULTS */}

          <section className="results-section">

            <div className="section-heading">

              <div className="card-kicker">
                AI ANALYSIS
              </div>

              <h2>
                Email security results
              </h2>

            </div>


            {!emails.length ? (

              <div className="empty-state">

                {gmailConnected
                  ? "Click Run AI Scan to analyze your Gmail messages."
                  : "Connect Gmail to start scanning."}

              </div>

            ) : (

              <div className="email-list">

                {emails.map(
                  (email, index) => (

                    <div
                      className="email-card"
                      key={
                        email.id ||
                        index
                      }
                    >

                      <div>

                        <h3>
                          {email.subject ||
                            "No subject"}
                        </h3>

                        <p>
                          From:{" "}
                          {email.sender ||
                            "Unknown"}
                        </p>

                        {email.date && (
                          <small>
                            {email.date}
                          </small>
                        )}

                      </div>


                      <div>

                        <strong>
                          {(
                            email.prediction ||
                            email.result ||
                            "unknown"
                          ).toUpperCase()}
                        </strong>


                        {email.confidence != null && (

                          <small>
                            {email.confidence}%
                            confidence
                          </small>

                        )}

                      </div>

                    </div>

                  )
                )}

              </div>

            )}

          </section>


          {/* ACCOUNT */}

          <section className="account-section">

            <div className="card-kicker">
              ACCOUNT
            </div>

            <h2>
              Workspace information
            </h2>


            <div className="account-grid">

              <div>
                <span>USER</span>
                <strong>
                  {user.name}
                </strong>
              </div>

              <div>
                <span>EMAIL</span>
                <strong>
                  {user.email}
                </strong>
              </div>

              <div>
                <span>GMAIL</span>
                <strong>
                  {gmailConnected
                    ? gmailEmail
                    : "NOT CONNECTED"}
                </strong>
              </div>

              <div>
                <span>PROTECTION</span>
                <strong>
                  ACTIVE
                </strong>
              </div>

            </div>

          </section>

        </main>

      </div>

    );

  }


  

  return (

    <div className="app">

      <header className="navbar">

        <div className="brand">

          <div className="brand-icon">
            ✦
          </div>

          <div className="brand-name">
            CyberShield <b>AI</b>
          </div>

        </div>


        <div className="nav-actions">

          <button
            className="login-button"
            onClick={() =>
              setShowAuth(true)
            }
          >
            Log in
          </button>


          <button
            className="get-started-button"
            onClick={() =>
              setShowAuth(true)
            }
          >
            Get Started →
          </button>

        </div>

      </header>


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

              <span>
                Protect every email.
              </span>

            </h1>


            <p className="hero-description">

              CyberShield AI connects to
              your Gmail inbox and
              intelligently analyzes messages
              for phishing, spam, malware
              and suspicious activity.

            </p>


            <div className="hero-actions">

              <button
                className="primary-button"
                onClick={() =>
                  setShowAuth(true)
                }
              >
                Protect My Gmail →
              </button>

            </div>

          </div>

        </section>

      </main>

    </div>

  );

}


export default App;


