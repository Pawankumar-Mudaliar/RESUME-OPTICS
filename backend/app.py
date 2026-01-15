"""
Flask Backend API
Main application file
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import json
from datetime import datetime
from resume_parser import ResumeParser
from skill_extractor import SkillExtractor
from matcher import JobMatcher
from models import db, ResumeAnalysis

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Database Configuration
# Uses DATABASE_URL env if provided; falls back to local Postgres with default creds.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:pawan@localhost:5432/postgres"
)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create temp folder for uploaded files
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create database tables
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def home():
    """Welcome endpoint"""
    return jsonify({
        "message": "🧠 AI Resume Analyzer API",
        "version": "1.0",
        "endpoints": {
            "health": "/health",
            "analyze_resume": "/api/analyze (POST)",
            "extract_skills": "/api/extract-skills (POST)",
            "calculate_ats": "/api/calculate-ats (POST)"
        },
        "status": "Running successfully!"
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "Backend is running!"}), 200


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """
    Main endpoint to analyze resume against job description
    
    Expected request:
    {
        "job_description": "string",
        "resume_file": file (PDF or DOCX)
    }
    """
    try:
        # Check if job description is provided
        if 'job_description' not in request.form:
            return jsonify({"error": "Job description is required"}), 400
        
        # Check if file is provided
        if 'resume_file' not in request.files:
            return jsonify({"error": "Resume file is required"}), 400
        
        job_description = request.form['job_description']
        resume_file = request.files['resume_file']
        
        # Validate file
        if resume_file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not (resume_file.filename.lower().endswith('.pdf') or 
                resume_file.filename.lower().endswith('.docx')):
            return jsonify({"error": "Only PDF and DOCX files are supported"}), 400
        
        # Save file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(temp_path)
        
        # Step 1: Parse resume
        parse_result = ResumeParser.parse_resume(temp_path)
        
        if "error" in parse_result:
            return jsonify(parse_result), 400
        
        resume_text = parse_result['cleaned_text']
        
        # Step 2: Extract skills from resume
        resume_skills_dict = SkillExtractor.extract_skills(resume_text)
        resume_skills_flat = SkillExtractor.get_all_skills_flat(resume_skills_dict)
        
        # Step 3: Extract skills from job description
        job_skills_dict = SkillExtractor.extract_skills(job_description)
        job_skills_flat = SkillExtractor.get_all_skills_flat(job_skills_dict)
        
        # Step 4: Find missing skills
        missing_skills = JobMatcher.find_missing_skills(
            resume_skills_flat, 
            job_skills_flat
        )
        
        # Step 5: Generate matching report
        report = JobMatcher.generate_match_report(
            resume_text,
            job_description,
            resume_skills_flat,
            missing_skills
        )
        
        # Clean up temp file
        os.remove(temp_path)
        
        # Save analysis to database
        try:
            analysis_record = ResumeAnalysis(
                filename=resume_file.filename,
                job_type=job_description[:100],  # Store first 100 chars as job type
                job_description=job_description,
                job_match_score=report['job_match_score'],
                ats_score=report['ats_score'],
                resume_strength=report['resume_strength'],
                skills_found=json.dumps(resume_skills_dict),
                missing_skills=json.dumps({'count': len(missing_skills), 'list': missing_skills}),
                recommendation=report['recommendation']
            )
            db.session.add(analysis_record)
            db.session.commit()
        except Exception as db_error:
            print(f"Database save error: {str(db_error)}")
            # Continue even if database save fails
        
        # Return complete analysis
        return jsonify({
            "success": True,
            "analysis": {
                "job_match_score": report['job_match_score'],
                "ats_score": report['ats_score'],
                "resume_strength": report['resume_strength'],
                "skills_found": {
                    "total": report['total_skills_found'],
                    "by_category": resume_skills_dict
                },
                "missing_skills": {
                    "count": report['missing_skills_count'],
                    "list": report['missing_skills']
                },
                "recommendation": report['recommendation']
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500


@app.route('/api/extract-skills', methods=['POST'])
def extract_skills_only():
    """
    Endpoint to extract skills from just a resume
    """
    try:
        if 'resume_file' not in request.files:
            return jsonify({"error": "Resume file is required"}), 400
        
        resume_file = request.files['resume_file']
        
        if resume_file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(temp_path)
        
        # Parse and extract skills
        parse_result = ResumeParser.parse_resume(temp_path)
        resume_text = parse_result['cleaned_text']
        
        skills_dict = SkillExtractor.extract_skills(resume_text)
        summary = SkillExtractor.skill_summary(skills_dict)
        
        os.remove(temp_path)
        
        return jsonify({
            "success": True,
            "skills": summary
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Skill extraction failed: {str(e)}"}), 500


@app.route('/api/calculate-ats', methods=['POST'])
def calculate_ats():
    """
    Endpoint to calculate ATS score for a resume
    """
    try:
        if 'resume_file' not in request.files:
            return jsonify({"error": "Resume file is required"}), 400
        
        resume_file = request.files['resume_file']
        
        # Save file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(temp_path)
        
        # Parse and calculate ATS
        parse_result = ResumeParser.parse_resume(temp_path)
        resume_text = parse_result['cleaned_text']
        
        ats_score = JobMatcher.calculate_ats_score(resume_text)
        
        os.remove(temp_path)
        
        return jsonify({
            "success": True,
            "ats_score": ats_score,
            "file_size": parse_result['length']
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"ATS calculation failed: {str(e)}"}), 500


@app.route('/api/history', methods=['GET'])
def get_analysis_history():
    """
    Get all previous analyses from database
    """
    try:
        analyses = ResumeAnalysis.query.order_by(ResumeAnalysis.created_at.desc()).all()
        return jsonify({
            "success": True,
            "total": len(analyses),
            "analyses": [analysis.to_dict() for analysis in analyses]
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve history: {str(e)}"}), 500


@app.route('/api/history/<int:analysis_id>', methods=['GET'])
def get_analysis_detail(analysis_id):
    """
    Get details of a specific analysis
    """
    try:
        analysis = ResumeAnalysis.query.get(analysis_id)
        if not analysis:
            return jsonify({"error": "Analysis not found"}), 404
        
        return jsonify({
            "success": True,
            "analysis": analysis.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve analysis: {str(e)}"}), 500


@app.route('/api/history/<int:analysis_id>', methods=['DELETE'])
def delete_analysis(analysis_id):
    """
    Delete a specific analysis
    """
    try:
        analysis = ResumeAnalysis.query.get(analysis_id)
        if not analysis:
            return jsonify({"error": "Analysis not found"}), 404
        
        db.session.delete(analysis)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Analysis deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete analysis: {str(e)}"}), 500


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """
    Get overall statistics from all analyses
    """
    try:
        total_analyses = ResumeAnalysis.query.count()
        avg_match_score = db.session.query(db.func.avg(ResumeAnalysis.job_match_score)).scalar() or 0
        avg_ats_score = db.session.query(db.func.avg(ResumeAnalysis.ats_score)).scalar() or 0
        
        return jsonify({
            "success": True,
            "stats": {
                "total_analyses": total_analyses,
                "average_job_match_score": round(avg_match_score, 2),
                "average_ats_score": round(avg_ats_score, 2)
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve statistics: {str(e)}"}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
