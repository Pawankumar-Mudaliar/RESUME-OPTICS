"""
Test script to analyze your resume using the Flask API
"""

import requests
import json

# API endpoint
BASE_URL = "http://localhost:5000"

# Your resume file path
RESUME_PATH = r"C:\Users\Pawankumar\OneDrive\Desktop\interview\RESUME.pdf"

# Sample job description
JOB_DESCRIPTION = """
We are seeking a Full Stack Developer with experience in Python, JavaScript, React, and Flask.
The ideal candidate should have knowledge of machine learning, NLP, and cloud platforms like AWS.
Strong skills in REST APIs, database management, and version control (Git) are required.
Experience with Docker, CI/CD, and agile development is a plus.
"""

print("=" * 60)
print("🧠 AI Resume Analyzer - Testing Backend")
print("=" * 60)

# Test 1: Health Check
print("\n1️⃣ Testing Health Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Extract Skills Only
print("\n2️⃣ Testing Skill Extraction...")
try:
    with open(RESUME_PATH, 'rb') as file:
        files = {'resume_file': file}
        response = requests.post(f"{BASE_URL}/api/extract-skills", files=files)
    
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Skills Found: {data['skills']['total_skills_found']}")
        print("\nSkills by Category:")
        for category, skills in data['skills']['skills'].items():
            if skills:
                print(f"  • {category}: {', '.join(skills)}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Calculate ATS Score
print("\n3️⃣ Testing ATS Score Calculation...")
try:
    with open(RESUME_PATH, 'rb') as file:
        files = {'resume_file': file}
        response = requests.post(f"{BASE_URL}/api/calculate-ats", files=files)
    
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"\n📈 ATS Score: {data['ats_score']}/100")
        print(f"📄 Resume Length: {data['file_size']} characters")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Full Resume Analysis
print("\n4️⃣ Testing Full Resume Analysis...")
try:
    with open(RESUME_PATH, 'rb') as file:
        files = {'resume_file': file}
        data = {'job_description': JOB_DESCRIPTION}
        response = requests.post(f"{BASE_URL}/api/analyze", files=files, data=data)
    
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        analysis = result['analysis']
        
        print("\n" + "=" * 60)
        print("📊 ANALYSIS REPORT")
        print("=" * 60)
        print(f"🎯 Job Match Score: {analysis['job_match_score']}%")
        print(f"📈 ATS Score: {analysis['ats_score']}%")
        print(f"💪 Resume Strength: {analysis['resume_strength']}")
        print(f"✅ Skills Found: {analysis['skills_found']['total']}")
        print(f"❌ Missing Skills: {analysis['missing_skills']['count']}")
        
        if analysis['missing_skills']['list']:
            print(f"\n🔍 Top Missing Skills:")
            for skill in analysis['missing_skills']['list'][:5]:
                print(f"   • {skill}")
        
        print(f"\n💡 Recommendation:")
        print(f"   {analysis['recommendation']}")
        print("=" * 60)
except Exception as e:
    print(f"❌ Error: {e}")

print("\n✨ Testing Complete!")
