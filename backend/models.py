"""
Database Models
Defines the structure of the database tables
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class ResumeAnalysis(db.Model):
    """
    Stores resume analysis results
    """
    __tablename__ = 'resume_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    job_type = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    
    # Analysis Results
    job_match_score = db.Column(db.Float, nullable=False)
    ats_score = db.Column(db.Float, nullable=False)
    resume_strength = db.Column(db.String(50), nullable=False)
    
    # Skills Data (stored as JSON)
    skills_found = db.Column(db.Text, nullable=False)  # JSON
    missing_skills = db.Column(db.Text, nullable=False)  # JSON
    
    # Metadata
    recommendation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ResumeAnalysis {self.id}: {self.filename}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'filename': self.filename,
            'job_type': self.job_type,
            'job_match_score': self.job_match_score,
            'ats_score': self.ats_score,
            'resume_strength': self.resume_strength,
            'skills_found': json.loads(self.skills_found),
            'missing_skills': json.loads(self.missing_skills),
            'recommendation': self.recommendation,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class User(db.Model):
    """
    Stores user information (optional for future authentication)
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # User metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to analyses
    analyses = db.relationship('ResumeAnalysis', backref='user', lazy=True, foreign_keys='ResumeAnalysis.user_id')
    
    def __repr__(self):
        return f'<User {self.username}>'


# Add user_id to ResumeAnalysis (optional for future)
ResumeAnalysis.user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
