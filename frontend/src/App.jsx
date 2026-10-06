import React, { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:5000";

const demoJobs = [
  {
    title: "Software Engineer",
    company: "Demo Technology Company",
    type: "REAL JOB",
    url: `${API_URL}/demo/real-job`,
  },
  {
    title: "Work From Home Opportunity",
    company: "Unknown Company",
    type: "FAKE JOB",
    url: `${API_URL}/demo/fake-job`,
  },
];

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const checkJob = async (jobUrl = url) => {
    if (!jobUrl.trim()) {
      setError("Please enter a job URL.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/detect`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: jobUrl.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Unable to analyze the job.");
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Could not connect to the Fake Job Detection API."
      );
    } finally {
      setLoading(false);
    }
  };

  const openAndCheckJob = (jobUrl) => {
    window.open(jobUrl, "_blank", "noopener,noreferrer");
    setUrl(jobUrl);
    checkJob(jobUrl);
  };

  const getPredictionTitle = () => {
    if (!result) return "";

    if (result.prediction === "FAKE") {
      return "Potentially Fake Job";
    }

    if (result.prediction === "REAL") {
      return "Likely Legitimate Job";
    }

    return "Analysis Result";
  };

  const getPredictionClass = () => {
    if (!result) return "";

    if (result.prediction === "FAKE") {
      return "fake";
    }

    if (result.prediction === "REAL") {
      return "real";
    }

    return "unknown";
  };

  const getRiskClass = () => {
    if (!result) return "unknown";

    const level = result.risk_level;

    if (level === "HIGH") return "high";
    if (level === "MEDIUM") return "medium";
    if (level === "LOW") return "low";

    return "unknown";
  };

  const formatValue = (value) => {
    if (
      value === null ||
      value === undefined ||
      value === ""
    ) {
      return "Not available";
    }

    return value;
  };

  const jobDetails = result?.job_details || {};

  return (
    <div className="app">

      {/* =====================================================
          HEADER
      ====================================================== */}

      <header className="header">
        <div className="header-inner">

          <div className="brand">
            <div className="brand-icon">🛡️</div>

            <div>
              <h2>Fake Job Detection</h2>
              <p>AI-Powered Job Safety Platform</p>
            </div>
          </div>

          <div className="api-status">
            <span className="status-dot"></span>
            API Online
          </div>

        </div>
      </header>


      {/* =====================================================
          HERO
      ====================================================== */}

      <section className="hero">

        <div className="hero-content">

          <div className="hero-badge">
            🧠 Intelligent Job Verification
          </div>

          <h1>
            Detect Fake Jobs Before{" "}
            <span>You Apply</span>
          </h1>

          <p>
            Analyze job postings using machine learning,
            webpage content, and URL security indicators.
          </p>

          {/* =================================================
              CHECKER
          ================================================= */}

          <div className="checker-card">

            <div className="checker-title">
              🔗 &nbsp;Check a Job Posting
            </div>

            <div className="checker-row">

              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    checkJob();
                  }
                }}
                placeholder="Paste a public job posting URL here..."
              />

              <button
                className="check-button"
                onClick={() => checkJob()}
                disabled={loading}
              >
                {loading ? "⏳ Checking..." : "🔍 Check Job"}
              </button>

            </div>

            <div className="checker-features">
              <span>✓ Works with public job websites</span>
              <span>✓ URL + webpage analysis</span>
              <span>✓ No login required</span>
            </div>

          </div>

        </div>

      </section>


      {/* =====================================================
          MAIN
      ====================================================== */}

      <main className="main-content">

        {/* ERROR */}

        {error && (
          <div className="error-box">
            ⚠️ {error}
          </div>
        )}


        {/* LOADING */}

        {loading && (
          <div className="loading-box">
            <div className="spinner"></div>
            <h3>Analyzing Job Posting...</h3>
            <p>
              Checking the URL and extracting public webpage
              information.
            </p>
          </div>
        )}


        {/* =================================================
            RESULT
        ================================================== */}

        {result && !loading && (

          <div className="results">

            {/* ---------------------------------------------
                RESULT HEADER
            ---------------------------------------------- */}

            <div className={`result-header ${getPredictionClass()}`}>

              <div className="result-left">

                <div className="result-icon">
                  {result.prediction === "FAKE"
                    ? "⚠️"
                    : result.prediction === "REAL"
                    ? "✓"
                    : "?"
                  }
                </div>

                <div>

                  <div className="result-label">
                    ANALYSIS RESULT
                  </div>

                  <h2>
                    {getPredictionTitle()}
                  </h2>

                  <p className="result-url">
                    {result.url}
                  </p>

                </div>

              </div>

              <div className={`risk-badge ${getRiskClass()}`}>
                {result.risk_level || "UNKNOWN"} RISK
              </div>

            </div>


            {/* ---------------------------------------------
                METRICS
            ---------------------------------------------- */}

            {result.analysis_status === "COMPLETED" && (

              <div className="metric-grid">

                {/* Risk Score */}

                <div className="metric-card">

                  <div className="metric-icon">
                    🎯
                  </div>

                  <div className="metric-label">
                    Risk Score
                  </div>

                  <div className="metric-value">
                    {formatValue(result.risk_score)}
                    <small>/100</small>
                  </div>

                  <div className="progress">
                    <div
                      className="progress-bar risk-progress"
                      style={{
                        width: `${Math.min(
                          result.risk_score || 0,
                          100
                        )}%`,
                      }}
                    ></div>
                  </div>

                </div>


                {/* Fake Probability */}

                <div className="metric-card">

                  <div className="metric-icon fake-icon">
                    ⚠️
                  </div>

                  <div className="metric-label">
                    Fake Probability
                  </div>

                  <div className="metric-value">
                    {formatValue(result.fake_probability)}%
                  </div>

                  <div className="progress">
                    <div
                      className="progress-bar fake-progress"
                      style={{
                        width: `${Math.min(
                          result.fake_probability || 0,
                          100
                        )}%`,
                      }}
                    ></div>
                  </div>

                </div>


                {/* Real Probability */}

                <div className="metric-card">

                  <div className="metric-icon real-icon">
                    ✓
                  </div>

                  <div className="metric-label">
                    Real Probability
                  </div>

                  <div className="metric-value">
                    {formatValue(result.real_probability)}%
                  </div>

                  <div className="progress">
                    <div
                      className="progress-bar real-progress"
                      style={{
                        width: `${Math.min(
                          result.real_probability || 0,
                          100
                        )}%`,
                      }}
                    ></div>
                  </div>

                </div>

              </div>
            )}


            {/* ---------------------------------------------
                UNAVAILABLE
            ---------------------------------------------- */}

            {result.analysis_status === "UNAVAILABLE" && (

              <div className="unavailable-box">

                <div className="unavailable-icon">
                  🔒
                </div>

                <div>

                  <h3>
                    Unable to Analyze This Webpage
                  </h3>

                  <p>
                    {result.message ||
                      "The webpage could not be analyzed."}
                  </p>

                  {result.error && (
                    <p className="technical-error">
                      Reason: {result.error}
                    </p>
                  )}

                </div>

              </div>
            )}


            {/* ---------------------------------------------
                JOB INFORMATION
            ---------------------------------------------- */}

            {result.analysis_status === "COMPLETED" && (

              <div className="two-column">

                <section className="panel">

                  <div className="panel-header">
                    <h3>📄 Job Information</h3>
                  </div>

                  <div className="job-info-grid">

                    <div className="info-item">
                      <span>Job Title</span>
                      <strong>
                        {formatValue(
                          jobDetails.job_title
                        )}
                      </strong>
                    </div>

                    <div className="info-item">
                      <span>Company</span>
                      <strong>
                        {formatValue(
                          jobDetails.company
                        )}
                      </strong>
                    </div>

                    <div className="info-item">
                      <span>Location</span>
                      <strong>
                        {formatValue(
                          jobDetails.location
                        )}
                      </strong>
                    </div>

                    <div className="info-item">
                      <span>Employment Type</span>
                      <strong>
                        {formatValue(
                          jobDetails.employment_type
                        )}
                      </strong>
                    </div>

                    <div className="info-item">
                      <span>Experience</span>
                      <strong>
                        {formatValue(
                          jobDetails.experience
                        )}
                      </strong>
                    </div>

                    <div className="info-item">
                      <span>Education</span>
                      <strong>
                        {formatValue(
                          jobDetails.education
                        )}
                      </strong>
                    </div>

                    <div className="info-item">
                      <span>Industry</span>
                      <strong>
                        {formatValue(
                          jobDetails.industry
                        )}
                      </strong>
                    </div>

                    <div className="info-item">
                      <span>Salary</span>
                      <strong>
                        {formatValue(
                          jobDetails.salary
                        )}
                      </strong>
                    </div>

                  </div>


                  <div className="info-row">

                    <span>Page Title</span>

                    <strong>
                      {formatValue(
                        result.page_title
                      )}
                    </strong>

                  </div>


                  <div className="info-row">

                    <span>Extraction Method</span>

                    <strong>
                      {formatValue(
                        result.extraction_method
                      )}
                    </strong>

                  </div>


                  <div className="info-row">

                    <span>Final URL</span>

                    <strong className="url-value">
                      {formatValue(
                        result.final_url ||
                        result.url
                      )}
                    </strong>

                  </div>

                </section>


                {/* -----------------------------------------
                    URL SECURITY
                ------------------------------------------ */}

                <section className="panel">

                  <div className="panel-header">
                    <h3>🔗 URL Security Analysis</h3>
                  </div>

                  <div className="security-grid">

                    <div className="security-item">
                      <span>HTTPS</span>
                      <strong>
                        {result.url_analysis?.https
                          ? "✓ Yes"
                          : "✕ No"}
                      </strong>
                    </div>

                    <div className="security-item">
                      <span>URL Length</span>
                      <strong>
                        {formatValue(
                          result.url_analysis?.url_length
                        )}
                      </strong>
                    </div>

                    <div className="security-item">
                      <span>Domain Length</span>
                      <strong>
                        {formatValue(
                          result.url_analysis?.domain_length
                        )}
                      </strong>
                    </div>

                    <div className="security-item">
                      <span>Dots</span>
                      <strong>
                        {formatValue(
                          result.url_analysis?.dot_count
                        )}
                      </strong>
                    </div>

                    <div className="security-item">
                      <span>Hyphens</span>
                      <strong>
                        {formatValue(
                          result.url_analysis?.hyphen_count
                        )}
                      </strong>
                    </div>

                    <div className="security-item">
                      <span>Subdomains</span>
                      <strong>
                        {formatValue(
                          result.url_analysis?.subdomain_count
                        )}
                      </strong>
                    </div>

                    <div className="security-item">
                      <span>Special Characters</span>
                      <strong>
                        {formatValue(
                          result.url_analysis
                            ?.special_character_count
                        )}
                      </strong>
                    </div>

                    <div className="security-item">
                      <span>Suspicious Words</span>
                      <strong>
                        {result.url_analysis
                          ?.suspicious_words?.length || 0}
                      </strong>
                    </div>

                  </div>

                </section>

              </div>
            )}


            {/* ---------------------------------------------
                DETECTION REASONS
            ---------------------------------------------- */}

            {result.analysis_status === "COMPLETED" && (

              <section className="panel reasons-panel">

                <div className="panel-header">
                  <h3>⚠️ Detection Reasons</h3>
                </div>

                {result.reasons &&
                result.reasons.length > 0 ? (

                  <div className="reasons-grid">

                    {result.reasons.map(
                      (reason, index) => (

                        <div
                          className="reason-item"
                          key={index}
                        >
                          ⚠️
                          <span>{reason}</span>
                        </div>

                      )
                    )}

                  </div>

                ) : (

                  <div className="no-reasons">
                    ✓ No major suspicious indicators
                    were detected.
                  </div>

                )}

              </section>
            )}


            {/* ---------------------------------------------
                MODEL PERFORMANCE
            ---------------------------------------------- */}

            <section className="panel model-panel">

              <div className="panel-header">
                <h3>📊 Model Performance</h3>
              </div>

              <p className="model-description">
                These metrics represent the performance of
                the trained machine learning model on the
                held-out test dataset.
              </p>

              <div className="model-grid">

                <div className="model-metric">
                  <span>Accuracy</span>
                  <strong>
                    {result.model_metrics?.accuracy || 97.65}%
                  </strong>
                </div>

                <div className="model-metric">
                  <span>Precision</span>
                  <strong>
                    {result.model_metrics?.precision || 70.51}%
                  </strong>
                </div>

                <div className="model-metric">
                  <span>Recall</span>
                  <strong>
                    {result.model_metrics?.recall || 88.44}%
                  </strong>
                </div>

                <div className="model-metric highlighted">
                  <span>F3 Score</span>
                  <strong>
                    {result.model_metrics?.f3 || 86.25}%
                  </strong>
                </div>

              </div>

              <div className="model-note">
                <strong>Selected model:</strong>{" "}
                Logistic Regression using TF-IDF features
                and SMOTE.
              </div>

            </section>


            {/* ---------------------------------------------
                ANALYZE ANOTHER
            ---------------------------------------------- */}

            <button
              className="another-button"
              onClick={() => {
                setResult(null);
                setUrl("");
                setError("");
                window.scrollTo({
                  top: 0,
                  behavior: "smooth",
                });
              }}
            >
              ↻ &nbsp; Analyze Another Job
            </button>

          </div>
        )}


        {/* =================================================
            BEFORE ANALYSIS
        ================================================== */}

        {!result && !loading && !error && (

          <div className="before-analysis">

            <div className="welcome-card">

              <div className="welcome-icon">
                🛡️
              </div>

              <h2>
                Protect Yourself From Fake Jobs
              </h2>

              <p>
                Paste a public job posting URL above to
                analyze its webpage content, URL security
                indicators, and fraud risk.
              </p>

            </div>


            {/* DEMO JOBS */}

            <section className="demo-section">

              <div className="section-heading">
                <h2>Try Demo Job Postings</h2>

                <p>
                  Test the detection system with these
                  built-in examples.
                </p>
              </div>

              <div className="demo-grid">

                {demoJobs.map(
                  (job, index) => (

                    <div
                      className="demo-card"
                      key={index}
                    >

                      <div className="demo-top">

                        <div className="demo-icon">
                          💼
                        </div>

                        <span
                          className={
                            job.type === "FAKE JOB"
                              ? "demo-type fake"
                              : "demo-type real"
                          }
                        >
                          {job.type}
                        </span>

                      </div>

                      <h3>
                        {job.title}
                      </h3>

                      <p>
                        {job.company}
                      </p>

                      <button
                        onClick={() =>
                          openAndCheckJob(job.url)
                        }
                      >
                        Check This Job →
                      </button>

                    </div>

                  )
                )}

              </div>

            </section>


            {/* HOW IT WORKS */}

            <section className="how-section">

              <div className="section-heading">
                <h2>How It Works</h2>
                <p>
                  Three stages work together to evaluate
                  a job posting.
                </p>
              </div>

              <div className="steps">

                <div className="step">
                  <div className="step-number">1</div>
                  <h3>Enter Job URL</h3>
                  <p>
                    Paste a public job posting URL into
                    the checker.
                  </p>
                </div>

                <div className="step">
                  <div className="step-number">2</div>
                  <h3>Analyze</h3>
                  <p>
                    The system extracts webpage content
                    and analyzes URL security indicators.
                  </p>
                </div>

                <div className="step">
                  <div className="step-number">3</div>
                  <h3>Get Risk Result</h3>
                  <p>
                    Machine learning predicts the risk
                    and provides reasons for the result.
                  </p>
                </div>

              </div>

            </section>


            {/* TECHNOLOGIES */}

            <section className="technology-section">

              <div className="section-heading">
                <h2>Technologies Used</h2>
              </div>

              <div className="technology-grid">

                <div>🐍 Python</div>
                <div>🤖 Scikit-learn</div>
                <div>📊 TF-IDF</div>
                <div>⚖️ SMOTE</div>
                <div>🌐 Flask</div>
                <div>⚛️ React</div>
                <div>🔎 BeautifulSoup</div>
                <div>🎭 Playwright</div>

              </div>

            </section>

          </div>
        )}

      </main>


      {/* =====================================================
          FOOTER
      ====================================================== */}

      <footer className="footer">

        <div className="footer-inner">

          <div>
            <strong>🛡️ Fake Job Detection</strong>
            <p>
              Machine Learning Based Job Safety Platform
            </p>
          </div>

          <div className="footer-right">
            Built with Python + React
            <span>•</span>
            B.Tech CSE Project
          </div>

        </div>

      </footer>

    </div>
  );
}

export default App;