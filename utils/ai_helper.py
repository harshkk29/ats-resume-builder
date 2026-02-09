"""
AI Helper Module - IMPROVED VERSION
Groq API Integration with accurate, dynamic ATS scoring
"""

from groq import Groq
from typing import Dict, List, Optional
import json
import re
from datetime import datetime

class AIHelper:
    def __init__(self, api_key: str):
        """Initialize Groq client with API key"""
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
    
    def extract_resume_info(self, resume_text: str, target_role: str) -> Dict:
        """Extract structured information from resume text with improved parsing"""
        prompt = f"""
You are an expert resume parser. Extract the following information from the resume text and return it as a JSON object.

Resume Text:
{resume_text}

Target Role: {target_role}

Extract and return ONLY a valid JSON object with these fields:
{{
    "name": "Full name",
    "email": "Email address",
    "phone": "Phone number",
    "target_role": "{target_role}",
    "professional_summary": "Professional summary or objective (2-4 sentences)",
    "skills": ["skill1", "skill2", "skill3", ...],
    "education": [
        {{
            "degree": "Degree name",
            "institution": "University/College name",
            "year": "Graduation year",
            "gpa": "GPA if mentioned"
        }}
    ],
    "experience": [
        {{
            "title": "Job title",
            "company": "Company name",
            "duration": "Duration (e.g., Jan 2020 - Dec 2022)",
            "responsibilities": ["responsibility1", "responsibility2", ...]
        }}
    ],
    "projects": [
        {{
            "name": "Project name",
            "description": "Brief description",
            "technologies": ["tech1", "tech2", ...],
            "achievements": ["achievement1", "achievement2", ...]
        }}
    ],
    "certifications": ["cert1", "cert2", ...],
    "languages": ["language1", "language2", ...]
}}

IMPORTANT:
1. Extract ALL information present in the resume
2. If a field is not found, use an empty string "" or empty array []
3. For skills, extract ALL technical and soft skills mentioned
4. For experience, extract ALL bullet points under responsibilities
5. Return ONLY valid JSON, no explanatory text

Return ONLY the JSON object, no additional text.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,  # Lower temperature for more accurate extraction
                max_tokens=2500
            )
            
            result = response.choices[0].message.content.strip()
            result = self._extract_json(result)
            
            # Clean up JSON before parsing
            result = result.replace('\n', ' ').replace('\r', '')
            result = re.sub(r',\s*}', '}', result)  # Remove trailing commas
            result = re.sub(r',\s*]', ']', result)
            
            parsed_data = json.loads(result.strip())
            
            # Validate and clean the extracted data
            parsed_data = self._validate_resume_data(parsed_data, target_role)
            
            print(f"Successfully extracted resume info")
            return parsed_data
            
        except json.JSONDecodeError as je:
            print(f"JSON parse error in extraction: {je}")
            print(f"Problematic JSON: {result[:500]}...")
            return self._create_minimal_resume(target_role)
        except Exception as e:
            print(f"Error extracting resume info: {e}")
            return self._create_minimal_resume(target_role)
    
    def _validate_resume_data(self, data: Dict, target_role: str) -> Dict:
        """Validate and ensure all required fields exist"""
        validated = {
            "name": data.get("name", ""),
            "email": data.get("email", ""),
            "phone": data.get("phone", ""),
            "target_role": data.get("target_role", target_role),
            "professional_summary": data.get("professional_summary", data.get("summary", "")),
            "skills": data.get("skills", []),
            "experience": data.get("experience", []),
            "education": data.get("education", []),
            "projects": data.get("projects", []),
            "certifications": data.get("certifications", []),
            "languages": data.get("languages", [])
        }
        return validated
    
    def _create_minimal_resume(self, target_role: str) -> Dict:
        """Create minimal resume structure when extraction fails"""
        return {
            "name": "",
            "email": "",
            "phone": "",
            "target_role": target_role,
            "professional_summary": "",
            "skills": [],
            "experience": [],
            "education": [],
            "projects": [],
            "certifications": [],
            "languages": []
        }
    
    def generate_resume_content(self, user_data: Dict, job_description: Optional[str] = None) -> Dict:
        """Generate optimized resume content based on user data and job description"""
        jd_context = f"\n\nJob Description:\n{job_description}" if job_description else ""
        
        prompt = f"""
You are an expert resume writer specializing in ATS-optimized resumes. Create a professional, ATS-friendly resume based on the following information.

User Information:
{json.dumps(user_data, indent=2)}

Target Role: {user_data.get('target_role', 'Not specified')}
{jd_context}

Generate a complete resume with the following sections. Return ONLY a valid JSON object:

{{
    "professional_summary": "A compelling 3-4 line professional summary tailored to the target role",
    "skills": {{
        "technical": ["skill1", "skill2", ...],
        "soft": ["skill1", "skill2", ...]
    }},
    "experience": [
        {{
            "title": "Job title",
            "company": "Company name",
            "duration": "Duration",
            "achievements": [
                "Achievement 1 with quantifiable results",
                "Achievement 2 with quantifiable results",
                "Achievement 3 with quantifiable results"
            ]
        }}
    ],
    "education": [
        {{
            "degree": "Degree name",
            "institution": "Institution name",
            "year": "Year",
            "gpa": "GPA if available",
            "relevant_coursework": ["course1", "course2", ...]
        }}
    ],
    "projects": [
        {{
            "name": "Project name",
            "description": "Detailed description with impact",
            "technologies": ["tech1", "tech2", ...],
            "achievements": ["achievement1", "achievement2"]
        }}
    ],
    "certifications": ["cert1", "cert2", ...],
    "keywords": ["keyword1", "keyword2", ...]
}}

Guidelines:
1. Use action verbs and quantifiable achievements
2. Include relevant keywords from the job description
3. Keep language professional and concise
4. Optimize for ATS parsing
5. Ensure all content is relevant to the target role

Return ONLY the JSON object, no additional text.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=2500
            )
            
            result = response.choices[0].message.content.strip()
            result = self._extract_json(result)
            parsed_data = json.loads(result.strip())
            print(f"Successfully generated resume content")
            return parsed_data
            
        except Exception as e:
            print(f"Error generating resume content: {e}")
            return {}
    
    def calculate_ats_score(self, resume_data: Dict, job_description: Optional[str] = None) -> Dict:
        """
        Calculate ACCURATE, DYNAMIC ATS score based on actual resume content
        Uses hybrid approach: AI analysis + rule-based scoring
        """
        # First, calculate base score using rules
        base_score = self._calculate_base_score(resume_data, job_description)
        
        # Then get AI analysis for detailed feedback
        jd_context = f"\n\nJob Description:\n{job_description}" if job_description else ""
        
        prompt = f"""
You are an ATS (Applicant Tracking System) expert. Analyze this resume and provide detailed feedback.

Resume Data:
{json.dumps(resume_data, indent=2)}

Target Role: {resume_data.get('target_role', 'Not specified')}
{jd_context}

The base ATS score is {base_score}/100 based on content analysis.

Provide detailed categorized feedback in 5 categories. Return ONLY a valid JSON object:
{{
    "category_scores": {{
        "content": <score 0-100 based on summary quality, achievements, metrics>,
        "format": <score 0-100 based on ATS-friendly structure>,
        "optimization": <score 0-100 based on keywords and JD alignment>,
        "best_practices": <score 0-100 based on action verbs, professional language>,
        "application_ready": <score 0-100 based on completeness, polish>
    }},
    "breakdown": {{
        "keyword_match": {{"score": <number>, "max": 30}},
        "skills_alignment": {{"score": <number>, "max": 25}},
        "experience_relevance": {{"score": <number>, "max": 20}},
        "formatting": {{"score": <number>, "max": 15}},
        "completeness": {{"score": <number>, "max": 10}}
    }},
    "strengths": [
        "Specific strength 1",
        "Specific strength 2",
        "Specific strength 3"
    ],
    "improvements": {{
        "content": [
            {{"severity": "error|warning|info", "message": "Issue title", "detail": "Detailed explanation", "section": "section_name"}}
        ],
        "format": [...],
        "optimization": [...],
        "best_practices": [...],
        "application_ready": [...]
    }},
    "missing_keywords": ["keyword1", "keyword2", ...],
    "summary": "A brief 2-3 sentence summary of the overall ATS evaluation"
}}

Be specific and actionable in improvements. Severity: "error" (critical), "warning" (important), "info" (suggestion).

Return ONLY the JSON object.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1800
            )
            
            result = response.choices[0].message.content.strip()
            result = self._extract_json(result)
            parsed_data = json.loads(result.strip())
            
            # Use the calculated base score, not AI's guess
            parsed_data['overall_score'] = base_score
            parsed_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"Successfully calculated ATS score: {base_score}")
            return parsed_data
            
        except Exception as e:
            print(f"Error calculating ATS score: {e}")
            # Return base score with minimal feedback on error
            return {
                "overall_score": base_score,
                "category_scores": {
                    "content": base_score,
                    "format": base_score,
                    "optimization": base_score // 2 if not job_description else base_score,
                    "best_practices": base_score,
                    "application_ready": base_score
                },
                "breakdown": {},
                "strengths": ["Resume structure is present"],
                "improvements": {
                    "content": [],
                    "format": [],
                    "optimization": [],
                    "best_practices": [],
                    "application_ready": []
                },
                "missing_keywords": [],
                "summary": f"Resume scored {base_score}/100. Further analysis unavailable.",
                "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def _calculate_base_score(self, resume_data: Dict, job_description: str = "") -> int:
        """
        Calculate accurate base ATS score using rule-based analysis
        This ensures the score is always based on actual content
        """
        score = 0
        
        # 1. Contact Information (10 points)
        if resume_data.get('name'):
            score += 3
        if resume_data.get('email') and '@' in str(resume_data.get('email', '')):
            score += 4
        if resume_data.get('phone'):
            score += 3
        
        # 2. Professional Summary (15 points)
        summary = resume_data.get('professional_summary', '')
        if summary:
            word_count = len(str(summary).split())
            if 20 <= word_count <= 100:
                score += 15  # Perfect length
            elif 10 <= word_count < 20 or 100 < word_count <= 150:
                score += 10  # Acceptable
            else:
                score += 5  # Too short or too long
        
        # 3. Skills (20 points)
        skills = resume_data.get('skills', [])
        skill_count = 0
        
        if isinstance(skills, dict):
            skill_count = len(skills.get('technical', [])) + len(skills.get('soft', []))
        elif isinstance(skills, list):
            skill_count = len(skills)
        
        if skill_count >= 10:
            score += 20
        elif skill_count >= 5:
            score += 15
        elif skill_count >= 3:
            score += 10
        elif skill_count > 0:
            score += 5
        
        # 4. Experience with Quantifiable Achievements (25 points)
        experience = resume_data.get('experience', [])
        if isinstance(experience, list) and len(experience) > 0:
            # Base points for having experience
            score += min(10, len(experience) * 3)
            
            # Check for quantifiable achievements
            exp_text = json.dumps(experience)
            metrics = re.findall(r'\d+%|\d+\+|\$\d+|\d+x|\d+k|\d+ [a-z]+', exp_text.lower())
            
            if len(metrics) >= 5:
                score += 15  # Excellent use of metrics
            elif len(metrics) >= 3:
                score += 10  # Good use of metrics
            elif len(metrics) >= 1:
                score += 5   # Some metrics
        
        # 5. Education (10 points)
        education = resume_data.get('education', [])
        if isinstance(education, list) and len(education) > 0:
            score += 10
        
        # 6. Projects (10 points)
        projects = resume_data.get('projects', [])
        if isinstance(projects, list):
            if len(projects) >= 3:
                score += 10
            elif len(projects) >= 1:
                score += 5
        
        # 7. Keywords & Job Description Match (10 points)
        if job_description:
            resume_text = json.dumps(resume_data).lower()
            jd_words = set(job_description.lower().split())
            
            # Count keyword matches
            matches = sum(1 for word in jd_words if len(word) > 3 and word in resume_text)
            
            if matches >= 20:
                score += 10
            elif matches >= 10:
                score += 7
            elif matches >= 5:
                score += 4
        else:
            score += 5  # Base score without JD
        
        # Ensure score is within 0-100
        return max(0, min(100, score))
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text that might have markdown formatting"""
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        # Try to find JSON object or array in the text
        json_match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
        if json_match:
            text = json_match.group(0)
        
        return text
