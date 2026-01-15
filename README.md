# 🧠 AI Resume Analyzer & Job Matcher

An AI-powered web application that analyzes resumes, extracts skills, and matches candidates with job descriptions using NLP and machine learning.

## ✨ Features

✅ Resume upload (PDF / DOCX)
✅ Job description input
✅ Skill extraction using NLP
✅ ATS compatibility score
✅ Resume–JD similarity score (0-100%)
✅ Missing skill suggestions
✅ Detailed analysis report
✅ Simple web interface

## 📊 Example Output

| Metric          | Value       |
| --------------- | ----------- |
| ATS Score       | 82%         |
| Job Match       | 76%         |
| Missing Skills  | Docker, AWS |
| Resume Strength | Strong      |

---

## 🛠️ Tech Stack

**Backend:**
- Flask (Python web framework)
- NLP: spaCy / NLTK / Scikit-learn
- TF-IDF + Cosine Similarity for matching

**Frontend:**
- React.js
- Tailwind CSS
- Axios for API calls

**File Processing:**
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)

---

## 📂 Project Structure

```
AI-Resume-Analyzer/
│── backend/
│   ├── app.py                 # Main Flask application
│   ├── resume_parser.py       # Extract text from PDF/DOCX
│   ├── skill_extractor.py     # Extract skills from text
│   ├── matcher.py             # Calculate matching scores
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
│
│── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   └── App.js            # Main App
│   └── package.json
│
└── README.md
```

---

## 🚀 Getting Started

### Backend Setup

1. **Navigate to backend folder:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask app:**
   ```bash
   python app.py
   ```
   
   The API will start at `http://localhost:5000`

### Frontend Setup (Coming Next)

1. **Navigate to frontend folder:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start React server:**
   ```bash
   npm start
   ```
   
   The app will open at `http://localhost:3000`

---

## 📡 API Endpoints

### 1. **Main Analysis** (POST)
```
POST /api/analyze
Content-Type: multipart/form-data

Request:
- resume_file: File (PDF or DOCX)
- job_description: String

Response:
{
  "success": true,
  "analysis": {
    "job_match_score": 76.5,
    "ats_score": 82,
    "resume_strength": "Strong",
    "skills_found": {...},
    "missing_skills": [...],
    "recommendation": "..."
  }
}
```

### 2. **Extract Skills Only** (POST)
```
POST /api/extract-skills
Content-Type: multipart/form-data

Request:
- resume_file: File

Response:
{
  "success": true,
  "skills": {
    "total_skills_found": 12,
    "by_category": {...}
  }
}
```

### 3. **Calculate ATS Score** (POST)
```
POST /api/calculate-ats
Content-Type: multipart/form-data

Request:
- resume_file: File

Response:
{
  "success": true,
  "ats_score": 82,
  "file_size": 2500
}
```

### 4. **Health Check** (GET)
```
GET /health

Response:
{
  "status": "Backend is running!"
}
```

---

## 🧠 How It Works

### Step 1: Resume Parsing
- Reads PDF/DOCX files
- Extracts and cleans text
- Removes special characters and extra whitespace

### Step 2: Skill Extraction
- Uses keyword matching against a predefined skill database
- Identifies 100+ technical skills
- Categorizes by: Programming Languages, Frameworks, Databases, Cloud, DevOps, AI/ML

### Step 3: ATS Scoring
- Checks text length (ideal: 400-1000 words)
- Verifies important sections (Experience, Skills, Education)
- Looks for contact info (email, phone)
- Returns score 0-100

### Step 4: Job Matching
- Converts both texts to TF-IDF vectors
- Calculates cosine similarity
- Returns match percentage (0-100%)

### Step 5: Missing Skills
- Finds skills in job description not in resume
- Suggests top 10 missing skills for improvement

---

## 📝 Usage Example

```python
from resume_parser import ResumeParser
from skill_extractor import SkillExtractor
from matcher import JobMatcher

# 1. Parse resume
resume = ResumeParser.parse_resume("my_resume.pdf")
print(resume['cleaned_text'])

# 2. Extract skills
skills = SkillExtractor.extract_skills(resume['cleaned_text'])
print(skills)

# 3. Calculate ATS score
ats = JobMatcher.calculate_ats_score(resume['cleaned_text'])
print(f"ATS Score: {ats}")

# 4. Match with job
job_desc = "Python developer with AWS experience..."
match_score = JobMatcher.calculate_match_score(
    resume['cleaned_text'], 
    job_desc
)
print(f"Match Score: {match_score}")
```

---

## 🔮 Advanced Features (Optional)

- LLM-based feedback (Gemini / OpenAI API)
- Multi-language support
- Recruiter dashboard
- Resume ranking for multiple candidates
- Email notifications
- Database storage of analyses

---

## 📚 Learning Resources

This project teaches:

1. **Backend Development** - Flask, REST APIs, file handling
2. **NLP Basics** - Text processing, tokenization, keyword extraction
3. **Machine Learning** - TF-IDF, cosine similarity, similarity metrics
4. **Full Stack** - Frontend + Backend integration
5. **Best Practices** - Code organization, error handling, API design

---

## 🐛 Troubleshooting

**Issue: PDF not reading properly**
- Make sure you have PyPDF2 installed: `pip install PyPDF2`
- Try with a different PDF file (some PDFs have special encoding)

**Issue: No skills found**
- The resume might not contain common technical terms
- Check if skills are spelled correctly (case-insensitive matching works)

**Issue: CORS errors**
- Make sure `Flask-CORS` is installed
- The backend is running on port 5000

---

## 🎯 Resume Description (For Your Resume)

> **AI Resume Analyzer & Job Matcher**  
> Developed an AI-powered web application that analyzes resumes and matches them with job descriptions using NLP and machine learning. Implemented skill extraction, ATS scoring, and cosine similarity-based matching to identify skill gaps and provide personalized improvement suggestions. Built using Python, Flask, NLP techniques, and React.

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

---

**Made with ❤️ for learning and interviews**
