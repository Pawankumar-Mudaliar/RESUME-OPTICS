import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import LandingPage from './components/LandingPage';

const API_BASE_URL = 'http://localhost:5000';

// Predefined job types with their descriptions
const JOB_TYPES = {
  'Full Stack Developer': 'We are seeking a Full Stack Developer with experience in React, Node.js, Python, and Flask. Strong knowledge of JavaScript, TypeScript, HTML, CSS, REST APIs, MongoDB, PostgreSQL, and Git. Experience with Docker, AWS, CI/CD, and agile development is required.',
  
  'Data Scientist': 'Looking for a Data Scientist with expertise in Python, R, Machine Learning, Deep Learning, TensorFlow, PyTorch, Scikit-learn, and NLP. Strong skills in SQL, NoSQL databases, data visualization, statistics, and cloud platforms (AWS/Azure/GCP). Experience with Docker and Jupyter is a plus.',
  
  'Frontend Developer': 'Seeking a Frontend Developer proficient in React, Vue, Angular, JavaScript, TypeScript, HTML5, CSS3, and Responsive Design. Knowledge of Redux, Webpack, REST APIs, GraphQL, Git, and modern UI/UX principles. Experience with NextJS and TailwindCSS is preferred.',
  
  'Backend Developer': 'We need a Backend Developer with strong skills in Python, Java, Node.js, Flask, Django, Spring Boot, or Express. Experience with REST APIs, GraphQL, PostgreSQL, MongoDB, Redis, Docker, Kubernetes, AWS, and microservices architecture is required.',
  
  'DevOps Engineer': 'Looking for a DevOps Engineer experienced in Docker, Kubernetes, Jenkins, GitLab CI/CD, Terraform, Ansible, AWS, Azure, GCP, Linux, Shell scripting, monitoring (Prometheus/Grafana), and infrastructure as code. Strong Git and agile knowledge required.',
  
  'Machine Learning Engineer': 'Seeking an ML Engineer with expertise in Python, TensorFlow, PyTorch, Scikit-learn, NLP, Deep Learning, Computer Vision, MLOps, Docker, Kubernetes, AWS/GCP/Azure ML services, REST APIs, and Git. Strong mathematics and statistics background required.',
  
  'Mobile App Developer': 'We are hiring a Mobile Developer proficient in React Native, Flutter, Kotlin, Swift, JavaScript, TypeScript, REST APIs, Firebase, and Git. Experience with iOS/Android development, app deployment, and mobile UI/UX design principles is essential.',
  
  'Cloud Architect': 'Looking for a Cloud Architect with deep knowledge of AWS, Azure, GCP, cloud migration, serverless architecture, Docker, Kubernetes, Terraform, microservices, security best practices, cost optimization, and DevOps. Relevant certifications preferred.'
};

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobType, setJobType] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState(null);
  const [showLanding, setShowLanding] = useState(true);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.name.endsWith('.pdf') || file.name.endsWith('.docx')) {
        setResumeFile(file);
        setError('');
      } else {
        setError('Please upload a PDF or DOCX file');
        setResumeFile(null);
      }
    }
  };

  const handleJobTypeChange = (e) => {
    const selectedJobType = e.target.value;
    setJobType(selectedJobType);
    setJobDescription(JOB_TYPES[selectedJobType] || '');
    setError('');
  };

  const handleAnalyze = async () => {
    if (!resumeFile) {
      setError('Please upload a resume file');
      return;
    }

    if (!jobType) {
      setError('Please select a job type');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('resume_file', resumeFile);
      formData.append('job_description', jobDescription);

      const response = await axios.post(`${API_BASE_URL}/api/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setResults(response.data.analysis);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleNewAnalysis = () => {
    setResumeFile(null);
    setJobType('');
    setJobDescription('');
    setResults(null);
    setError('');
  };

  const getImprovementSuggestions = (results) => {
    const suggestions = [];
    
    // Based on ATS score
    if (results.ats_score < 60) {
      suggestions.push({
        category: '📄 Resume Format',
        issue: 'Your resume format needs improvement',
        tips: [
          'Ensure your resume is 400-1000 words long',
          'Include clear sections: Summary, Experience, Skills, Education, Projects',
          'Add your contact information (email and phone)',
          'Use bullet points for better readability',
          'Avoid complex formatting that ATS systems cannot read'
        ]
      });
    }

    // Based on job match score
    if (results.job_match_score < 40) {
      suggestions.push({
        category: '🎯 Keyword Optimization',
        issue: 'Low keyword match with job description',
        tips: [
          'Add more relevant keywords from the job description',
          'Quantify your achievements with numbers and metrics',
          'Use action verbs (developed, implemented, designed, etc.)',
          'Mirror the language used in the job posting',
          'Include industry-specific terminology'
        ]
      });
    }

    // Based on missing skills
    if (results.missing_skills.count > 5) {
      suggestions.push({
        category: '💡 Skills Gap',
        issue: `You're missing ${results.missing_skills.count} important skills`,
        tips: [
          `Priority skills to add: ${results.missing_skills.list.slice(0, 3).join(', ')}`,
          'Consider taking online courses (Coursera, Udemy, Pluralsight)',
          'Build small projects to demonstrate these skills',
          'Add a "Currently Learning" section to show growth mindset',
          'Update your resume after completing each new project or course'
        ]
      });
    }

    // General suggestions
    if (results.skills_found.total < 10) {
      suggestions.push({
        category: '🚀 Skills Enhancement',
        issue: 'Limited technical skills shown in resume',
        tips: [
          'List all programming languages, frameworks, and tools you know',
          'Include both hard skills (technical) and soft skills (teamwork, communication)',
          'Add version control systems (Git, GitHub)',
          'Mention any relevant certifications',
          'Include personal or open-source projects'
        ]
      });
    }

    // Always provide career growth tips
    suggestions.push({
      category: '📈 Career Growth Tips',
      issue: 'Ways to stand out from other candidates',
      tips: [
        'Create a GitHub portfolio with 3-5 quality projects',
        'Write technical blog posts or tutorials',
        'Contribute to open-source projects',
        'Network on LinkedIn and attend tech meetups',
        'Get relevant certifications for your target role',
        'Tailor your resume for each specific job application'
      ]
    });

    return suggestions;
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#4caf50';
    if (score >= 60) return '#ff9800';
    return '#f44336';
  };

  // If landing page is shown, display it
  if (showLanding) {
    return <LandingPage onGetStarted={() => setShowLanding(false)} />;
  }

  return (
    <div className="app">
      <header className="header">
        <h1>RESUME·OPTICS</h1>
        <p>Intelligent Career Review - Analyze your resume against job descriptions using AI & Machine Learning</p>
      </header>

      <div className="main-container">
        {!results ? (
          <div className="upload-section">
            <div className="form-group">
              <label htmlFor="resume-upload">📄 Upload Your Resume</label>
              <div className="file-input-wrapper">
                <input
                  type="file"
                  id="resume-upload"
                  className="file-input"
                  accept=".pdf,.docx"
                  onChange={handleFileChange}
                />
                <label
                  htmlFor="resume-upload"
                  className={`file-input-button ${resumeFile ? 'file-selected' : ''}`}
                >
                  {resumeFile
                    ? `✅ ${resumeFile.name}`
                    : '📎 Click to upload resume (PDF or DOCX)'}
                </label>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="job-type">💼 Select Job Type</label>
              <select
                id="job-type"
                className="select-input"
                value={jobType}
                onChange={handleJobTypeChange}
              >
                <option value="">-- Choose a job type --</option>
                {Object.keys(JOB_TYPES).map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
              {jobDescription && (
                <div className="job-preview">
                  <p><strong>Job Description:</strong></p>
                  <p>{jobDescription}</p>
                </div>
              )}
            </div>

            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={loading || !resumeFile || !jobType}
            >
              {loading ? '🔄 Analyzing...' : '🚀 Analyze Resume'}
            </button>

            {error && <div className="error-message">❌ {error}</div>}

            {loading && (
              <div className="loading">
                <div className="loading-spinner"></div>
                <p>Analyzing your resume with AI...</p>
              </div>
            )}
          </div>
        ) : (
          <div className="results-container">
            <div className="results-header">
              <h2>📊 Analysis Results</h2>
              <p>Here's how your resume matches the job description</p>
            </div>

            <div className="score-cards">
              <div className="score-card" style={{ background: `linear-gradient(135deg, ${getScoreColor(results.job_match_score)} 0%, ${getScoreColor(results.job_match_score)}dd 100%)` }}>
                <h3>Job Match Score</h3>
                <div className="score-value">{results.job_match_score}%</div>
                <div className="score-label">Resume-JD Similarity</div>
              </div>

              <div className="score-card" style={{ background: `linear-gradient(135deg, ${getScoreColor(results.ats_score)} 0%, ${getScoreColor(results.ats_score)}dd 100%)` }}>
                <h3>ATS Score</h3>
                <div className="score-value">{results.ats_score}%</div>
                <div className="score-label">System Compatibility</div>
              </div>

              <div className="score-card">
                <h3>Resume Strength</h3>
                <div className="score-value">{results.skills_found.total}</div>
                <div className="score-label">{results.resume_strength}</div>
              </div>
            </div>

            <div className="details-section">
              <h3>✅ Skills Found in Your Resume</h3>
              <p>Total Skills Detected: <strong>{results.skills_found.total}</strong></p>
              <div className="skills-grid">
                {Object.entries(results.skills_found.by_category).map(([category, skills]) =>
                  skills.length > 0 ? (
                    skills.map((skill, idx) => (
                      <div key={`${category}-${idx}`} className="skill-tag">
                        {skill}
                      </div>
                    ))
                  ) : null
                )}
              </div>
            </div>

            {results.missing_skills.count > 0 && (
              <div className="missing-skills">
                <h4>⚠️ Missing Skills ({results.missing_skills.count})</h4>
                <p>These skills from the job description are not in your resume:</p>
                <div className="missing-skills-list">
                  {results.missing_skills.list.map((skill, idx) => (
                    <span key={idx} className="missing-skill-tag">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="recommendation">
              <h4>💡 Overall Recommendation</h4>
              <p>{results.recommendation}</p>
            </div>

            {/* Improvement Suggestions Section */}
            <div className="improvements-section">
              <h3>🎯 What's Lacking & How to Improve</h3>
              {getImprovementSuggestions(results).map((suggestion, idx) => (
                <div key={idx} className="improvement-card">
                  <div className="improvement-header">
                    <h4>{suggestion.category}</h4>
                    <p className="issue-text">{suggestion.issue}</p>
                  </div>
                  <div className="improvement-tips">
                    <strong>Action Steps:</strong>
                    <ul>
                      {suggestion.tips.map((tip, tipIdx) => (
                        <li key={tipIdx}>{tip}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>

            <button className="new-analysis-button" onClick={handleNewAnalysis}>
              🔄 Analyze Another Resume
            </button>
          </div>
        )}
      </div>

      <footer style={{ textAlign: 'center', color: 'white', marginTop: '20px', opacity: 0.8 }}>
        <p>Resume·Optics - Intelligent Career Review | Made with ❤️ using React, Flask & AI</p>
      </footer>
    </div>
  );
}

export default App;