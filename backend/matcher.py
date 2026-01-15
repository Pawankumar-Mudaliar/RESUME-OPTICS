"""
Job Matcher Module
Matches resume with job description using string similarity
"""

from collections import Counter
import math


class JobMatcher:
    """
    This class compares resume and job description to find match percentage
    """
    
    @staticmethod
    def calculate_match_score(resume_text, job_description):
        """
        Calculate similarity between resume and job description
        Using cosine similarity with simple word tokenization
        
        Args:
            resume_text: Cleaned resume text
            job_description: Job description text
            
        Returns:
            Match percentage (0-100)
        """
        try:
            # Convert to lowercase and split into words
            resume_words = set(resume_text.lower().split())
            job_words = set(job_description.lower().split())
            
            # Remove very short words
            resume_words = {w for w in resume_words if len(w) > 2}
            job_words = {w for w in job_words if len(w) > 2}
            
            # Calculate Jaccard similarity
            if len(job_words) == 0:
                return 0
            
            intersection = len(resume_words & job_words)
            union = len(resume_words | job_words)
            
            if union == 0:
                return 0
            
            similarity = intersection / union
            match_score = round(similarity * 100, 2)
            
            # Also check for common phrases
            phrase_bonus = JobMatcher._phrase_matching(resume_text, job_description)
            
            # Combine scores
            final_score = min(100, (match_score * 0.7) + (phrase_bonus * 0.3))
            
            return round(final_score, 2)
        except Exception as e:
            return 0
    
    @staticmethod
    def _phrase_matching(resume_text, job_description):
        """
        Bonus points for matching phrases (not just single words)
        """
        bonus = 0
        
        # Split into bigrams (2-word phrases)
        resume_bigrams = set()
        job_bigrams = set()
        
        resume_words = resume_text.lower().split()
        job_words = job_description.lower().split()
        
        for i in range(len(resume_words) - 1):
            resume_bigrams.add(f"{resume_words[i]} {resume_words[i+1]}")
        
        for i in range(len(job_words) - 1):
            job_bigrams.add(f"{job_words[i]} {job_words[i+1]}")
        
        # Count matching bigrams
        matching_bigrams = len(resume_bigrams & job_bigrams)
        
        if len(job_bigrams) > 0:
            bonus = (matching_bigrams / len(job_bigrams)) * 100
        
        return bonus
    
    @staticmethod
    def extract_keywords(text):
        """
        Extract important keywords from text
        
        Args:
            text: Input text
            
        Returns:
            List of keywords
        """
        # Split text and filter short words
        words = text.lower().split()
        keywords = [word.strip('.,!?;:') for word in words if len(word) > 3]
        return list(set(keywords))
    
    @staticmethod
    def find_missing_skills(resume_skills, job_skills):
        """
        Find skills in job description that are missing in resume
        
        Args:
            resume_skills: List of resume skills
            job_skills: List of job description skills
            
        Returns:
            List of missing skills
        """
        resume_set = set(skill.lower() for skill in resume_skills)
        job_set = set(skill.lower() for skill in job_skills)
        
        missing = list(job_set - resume_set)
        return sorted(missing)
    
    @staticmethod
    def calculate_ats_score(resume_text):
        """
        Calculate ATS (Applicant Tracking System) compatibility score
        
        This evaluates:
        - Text length (resume should be 400-1000 words)
        - Section presence (Experience, Skills, Education)
        - Formatting (proper spacing)
        
        Args:
            resume_text: Cleaned resume text
            
        Returns:
            ATS score (0-100)
        """
        score = 0
        
        # 1. Check text length (ideal: 400-1000 words)
        word_count = len(resume_text.split())
        if 400 <= word_count <= 1000:
            score += 20
        elif 200 <= word_count <= 1500:
            score += 10
        
        # 2. Check for important sections
        sections = ['experience', 'skills', 'education', 'projects', 'summary']
        found_sections = 0
        for section in sections:
            if section.lower() in resume_text.lower():
                found_sections += 1
        
        score += (found_sections / len(sections)) * 40
        
        # 3. Check for contact info (email and phone)
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        
        if len(resume_text.split('\n')) > 5:  # Good formatting
            score += 10
        
        if 'email' in resume_text.lower() or '@' in resume_text:
            score += 15
        
        if 'phone' in resume_text.lower():
            score += 15
        
        return min(round(score), 100)
    
    @staticmethod
    def generate_match_report(resume_text, job_description, resume_skills, missing_skills):
        """
        Generate complete matching report
        
        Args:
            resume_text: Cleaned resume text
            job_description: Job description text
            resume_skills: Found resume skills
            missing_skills: Missing skills
            
        Returns:
            Dictionary with comprehensive report
        """
        match_score = JobMatcher.calculate_match_score(resume_text, job_description)
        ats_score = JobMatcher.calculate_ats_score(resume_text)
        
        # Determine resume strength
        if ats_score >= 80:
            strength = "Strong"
        elif ats_score >= 60:
            strength = "Good"
        elif ats_score >= 40:
            strength = "Fair"
        else:
            strength = "Needs Improvement"
        
        return {
            'job_match_score': match_score,
            'ats_score': ats_score,
            'resume_strength': strength,
            'total_skills_found': len(resume_skills),
            'missing_skills_count': len(missing_skills),
            'missing_skills': missing_skills[:10],  # Top 10 missing skills
            'recommendation': JobMatcher._get_recommendation(match_score, ats_score)
        }
    
    @staticmethod
    def _get_recommendation(match_score, ats_score):
        """
        Generate recommendation based on scores
        """
        if match_score >= 80 and ats_score >= 80:
            return "Excellent match! Your resume aligns well with the job."
        elif match_score >= 60 and ats_score >= 60:
            return "Good match! Consider adding more relevant skills."
        elif match_score >= 40:
            return "Fair match. Add more skills from the job description."
        else:
            return "Low match. Significant skill improvements needed."

    
    @staticmethod
    def extract_keywords(text):
        """
        Extract important keywords from text
        
        Args:
            text: Input text
            
        Returns:
            List of keywords
        """
        # Split text and filter short words
        words = text.lower().split()
        keywords = [word.strip('.,!?;:') for word in words if len(word) > 3]
        return list(set(keywords))
    
    @staticmethod
    def find_missing_skills(resume_skills, job_skills):
        """
        Find skills in job description that are missing in resume
        
        Args:
            resume_skills: List of resume skills
            job_skills: List of job description skills
            
        Returns:
            List of missing skills
        """
        resume_set = set(skill.lower() for skill in resume_skills)
        job_set = set(skill.lower() for skill in job_skills)
        
        missing = list(job_set - resume_set)
        return sorted(missing)
    
    @staticmethod
    def calculate_ats_score(resume_text):
        """
        Calculate ATS (Applicant Tracking System) compatibility score
        
        This evaluates:
        - Text length (resume should be 400-1000 words)
        - Section presence (Experience, Skills, Education)
        - Formatting (proper spacing)
        
        Args:
            resume_text: Cleaned resume text
            
        Returns:
            ATS score (0-100)
        """
        score = 0
        
        # 1. Check text length (ideal: 400-1000 words)
        word_count = len(resume_text.split())
        if 400 <= word_count <= 1000:
            score += 20
        elif 200 <= word_count <= 1500:
            score += 10
        
        # 2. Check for important sections
        sections = ['experience', 'skills', 'education', 'projects', 'summary']
        found_sections = 0
        for section in sections:
            if section.lower() in resume_text.lower():
                found_sections += 1
        
        score += (found_sections / len(sections)) * 40
        
        # 3. Check for contact info (email and phone)
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        
        if len(resume_text.split('\n')) > 5:  # Good formatting
            score += 10
        
        if 'email' in resume_text.lower() or '@' in resume_text:
            score += 15
        
        if 'phone' in resume_text.lower():
            score += 15
        
        return min(round(score), 100)
    
    @staticmethod
    def generate_match_report(resume_text, job_description, resume_skills, missing_skills):
        """
        Generate complete matching report
        
        Args:
            resume_text: Cleaned resume text
            job_description: Job description text
            resume_skills: Found resume skills
            missing_skills: Missing skills
            
        Returns:
            Dictionary with comprehensive report
        """
        match_score = JobMatcher.calculate_match_score(resume_text, job_description)
        ats_score = JobMatcher.calculate_ats_score(resume_text)
        
        # Determine resume strength
        if ats_score >= 80:
            strength = "Strong"
        elif ats_score >= 60:
            strength = "Good"
        elif ats_score >= 40:
            strength = "Fair"
        else:
            strength = "Needs Improvement"
        
        return {
            'job_match_score': match_score,
            'ats_score': ats_score,
            'resume_strength': strength,
            'total_skills_found': len(resume_skills),
            'missing_skills_count': len(missing_skills),
            'missing_skills': missing_skills[:10],  # Top 10 missing skills
            'recommendation': JobMatcher._get_recommendation(match_score, ats_score)
        }
    
    @staticmethod
    def _get_recommendation(match_score, ats_score):
        """
        Generate recommendation based on scores
        """
        if match_score >= 80 and ats_score >= 80:
            return "Excellent match! Your resume aligns well with the job."
        elif match_score >= 60 and ats_score >= 60:
            return "Good match! Consider adding more relevant skills."
        elif match_score >= 40:
            return "Fair match. Add more skills from the job description."
        else:
            return "Low match. Significant skill improvements needed."
