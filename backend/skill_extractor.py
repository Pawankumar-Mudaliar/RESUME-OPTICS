"""
Skill Extractor Module
Extracts technical skills from resume text
"""

import re


class SkillExtractor:
    """
    This class identifies technical skills from resume text
    """
    
    # Comprehensive list of technical skills
    TECH_SKILLS = {
        'programming_languages': [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go',
            'rust', 'php', 'ruby', 'swift', 'kotlin', 'scala', 'r', 'matlab',
            'sql', 'html', 'css', 'bash', 'shell'
        ],
        'web_frameworks': [
            'react', 'vue', 'angular', 'flask', 'django', 'fastapi', 'express',
            'spring', 'springboot', 'nodejs', 'nextjs', 'svelte', 'nuxt'
        ],
        'databases': [
            'postgresql', 'mysql', 'mongodb', 'redis', 'cassandra', 'sqlite',
            'oracle', 'elasticsearch', 'dynamodb', 'firestore', 'neo4j'
        ],
        'cloud_platforms': [
            'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean'
        ],
        'devops_tools': [
            'docker', 'kubernetes', 'jenkins', 'gitlab', 'github', 'terraform',
            'ansible', 'ci/cd', 'git', 'docker', 'prometheus', 'grafana'
        ],
        'ai_ml': [
            'machine learning', 'tensorflow', 'pytorch', 'scikit-learn',
            'nlp', 'deep learning', 'spacy', 'keras', 'huggingface', 'openai',
            'gemini', 'llm', 'bert', 'gpt'
        ],
        'other_tools': [
            'git', 'linux', 'windows', 'macos', 'agile', 'scrum', 'jira',
            'confluence', 'slack', 'rest api', 'graphql', 'postman'
        ]
    }
    
    @staticmethod
    def extract_skills(resume_text):
        """
        Extract skills from resume text
        
        Args:
            resume_text: Cleaned resume text
            
        Returns:
            Dictionary with found skills by category
        """
        resume_lower = resume_text.lower()
        found_skills = {
            'programming_languages': [],
            'web_frameworks': [],
            'databases': [],
            'cloud_platforms': [],
            'devops_tools': [],
            'ai_ml': [],
            'other_tools': []
        }
        
        # Search for each skill in the resume
        for category, skills in SkillExtractor.TECH_SKILLS.items():
            for skill in skills:
                # Use word boundaries to find exact matches
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, resume_lower, re.IGNORECASE):
                    if skill not in found_skills[category]:
                        found_skills[category].append(skill)
        
        return found_skills
    
    @staticmethod
    def get_all_skills_flat(found_skills):
        """
        Flatten all found skills into a single list
        
        Args:
            found_skills: Dictionary from extract_skills()
            
        Returns:
            Flat list of all skills
        """
        all_skills = []
        for category in found_skills.values():
            all_skills.extend(category)
        return sorted(list(set(all_skills)))
    
    @staticmethod
    def skill_summary(found_skills):
        """
        Create a summary of extracted skills
        
        Args:
            found_skills: Dictionary from extract_skills()
            
        Returns:
            Summary with counts
        """
        total_skills = sum(len(skills) for skills in found_skills.values())
        
        return {
            'total_skills_found': total_skills,
            'by_category': {cat: len(skills) for cat, skills in found_skills.items()},
            'skills': found_skills
        }
