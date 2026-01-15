# RESUME OPTICS

AI-powered resume analyzer and job matcher. Upload a resume, provide a job description, and get ATS and similarity scores with suggested skill gaps.

## Features
- Resume upload (PDF/DOCX) and JD input
- Skill extraction and missing-skill suggestions
- ATS and similarity scoring (TF-IDF + cosine similarity)
- Simple React UI over a Flask API

## Tech Stack
- Backend: Flask, scikit-learn, spaCy/NLTK, PyPDF2, python-docx
- Frontend: React, Axios, basic CSS

## Project Structure
```
backend/
  app.py              # Flask API
  resume_parser.py    # PDF/DOCX text extraction
  skill_extractor.py  # Skill detection
  matcher.py          # ATS + similarity scoring
  requirements.txt
frontend/
  src/ (React app)
README.md
```

## Quickstart
Backend
1) cd backend
2) pip install -r requirements.txt
3) python app.py  # serves on http://localhost:5000

Frontend
1) cd frontend
2) npm install
3) npm start     # serves on http://localhost:3000

## API (summary)
- POST /api/analyze: multipart with resume_file + job_description → scores + missing skills
- POST /api/extract-skills: resume_file → extracted skills
- POST /api/calculate-ats: resume_file → ATS score
- GET /health: service check

## Notes
- Keep secrets in backend/.env (ignored by git).
- Default config expects local dev; update CORS/URLs for deployment.

## License
MIT
