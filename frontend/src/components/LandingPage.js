import React from 'react';
import '../styles/LandingPage.css';

function LandingPage({ onGetStarted }) {
  return (
    <div className="landing-container">
      {/* Header/Navigation */}
      <header className="landing-header">
        <div className="logo">
          <span className="logo-icon">✓</span>
          <span className="logo-text">RESUME<span className="logo-dot">·</span>OPTICS</span>
        </div>
        <nav className="nav-links">
          <a href="#features">Features</a>
          <a href="#how-it-works">How it Works</a>
          <a href="#benefits">Benefits</a>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            Intelligent Career Review
          </h1>
          <p className="hero-subtitle">
            Get instant feedback on your resume and increase your chances of landing interviews
          </p>
          <button className="cta-button" onClick={onGetStarted}>
            Get Started Now
            <span className="button-arrow">→</span>
          </button>
          <div className="trust-badges">
            <span className="badge">✓ 100% Private</span>
            <span className="badge">⚡ Instant Results</span>
            <span className="badge">🎯 AI Powered</span>
          </div>
        </div>
        <div className="hero-illustration">
          <div className="illustration-box">
            <div className="document-icon">📊</div>
            <div className="sparkles">✨</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <h2>Key Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Job Matching Score</h3>
            <p>Get an instant match percentage between your resume and job description</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>ATS Optimization</h3>
            <p>See how well your resume will perform with Applicant Tracking Systems</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Skill Detection</h3>
            <p>Identify all skills in your resume and see what's missing</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💡</div>
            <h3>Smart Recommendations</h3>
            <p>Get actionable suggestions to improve your resume immediately</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚙️</div>
            <h3>Multiple Job Types</h3>
            <p>Analyze your resume against 8 different job role descriptions</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💾</div>
            <h3>Analysis History</h3>
            <p>Keep track of all your previous analyses in one place</p>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="how-it-works-section">
        <h2>How It Works</h2>
        <div className="steps-container">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Upload Your Resume</h3>
            <p>Select your resume file in PDF or DOCX format</p>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>Choose Job Type</h3>
            <p>Pick from 8 predefined job roles or paste a custom job description</p>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Get Analysis</h3>
            <p>Receive detailed feedback in seconds with improvement tips</p>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="benefits-section">
        <h2>Why Use ResumeChecker?</h2>
        <div className="benefits-content">
          <div className="benefits-list">
            <div className="benefit-item">
              <span className="benefit-check">✓</span>
              <div>
                <h4>Save Time</h4>
                <p>Get instant feedback instead of waiting for recruiter responses</p>
              </div>
            </div>
            <div className="benefit-item">
              <span className="benefit-check">✓</span>
              <div>
                <h4>Increase Success Rate</h4>
                <p>Optimize your resume for both ATS systems and recruiters</p>
              </div>
            </div>
            <div className="benefit-item">
              <span className="benefit-check">✓</span>
              <div>
                <h4>Actionable Insights</h4>
                <p>Get specific recommendations on what to add or improve</p>
              </div>
            </div>
            <div className="benefit-item">
              <span className="benefit-check">✓</span>
              <div>
                <h4>Multiple Job Types</h4>
                <p>Test your resume against different roles and industries</p>
              </div>
            </div>
          </div>
          <div className="benefits-stats">
            <div className="stat-box">
              <h3>8+</h3>
              <p>Job Types</p>
            </div>
            <div className="stat-box">
              <h3>100+</h3>
              <p>Technical Skills</p>
            </div>
            <div className="stat-box">
              <h3>3</h3>
              <p>Analysis Metrics</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <h2>Ready to Improve Your Resume?</h2>
        <button className="cta-button-secondary" onClick={onGetStarted}>
          Start Your Free Analysis
        </button>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <p>&copy; 2026 Resume·Optics. Intelligent Career Review powered by AI.</p>
      </footer>
    </div>
  );
}

export default LandingPage;
