"""
ATS Scorer Module - FIXED VERSION
Calculates and formats ATS scores dynamically based on actual resume content
"""

from typing import Dict, List
import re

class ATSScorer:
    """Calculate and format ATS scores with accurate, dynamic scoring"""
    
    @staticmethod
    def calculate_dynamic_score(resume_data: Dict, job_description: str = "") -> int:
        """
        Calculate actual ATS score based on resume content
        
        Args:
            resume_data: Resume data dictionary
            job_description: Optional job description
            
        Returns:
            Integer score from 0-100
        """
        score = 0
        
        # Content Quality (30 points)
        if resume_data.get('professional_summary'):
            summary = resume_data['professional_summary']
            if len(summary.split()) >= 20 and len(summary.split()) <= 100:
                score += 15
            else:
                score += 8
        
        # Has quantifiable achievements
        exp_text = str(resume_data.get('experience', ''))
        numbers = re.findall(r'\d+%|\d+\+|\$\d+|\d+x', exp_text)
        score += min(15, len(numbers) * 3)
        
        # Skills (20 points)
        skills = resume_data.get('skills', [])
        if isinstance(skills, dict):
            skill_count = len(skills.get('technical', [])) + len(skills.get('soft', []))
        elif isinstance(skills, list):
            skill_count = len(skills)
        else:
            skill_count = 0
        
        score += min(20, skill_count * 2)
        
        # Experience (20 points)
        experience = resume_data.get('experience', [])
        if isinstance(experience, list):
            score += min(20, len(experience) * 7)
        
        # Education (10 points)
        education = resume_data.get('education', [])
        if isinstance(education, list) and len(education) > 0:
            score += 10
        
        # Contact Info (10 points)
        contact_score = 0
        if resume_data.get('name'):
            contact_score += 3
        if resume_data.get('email'):
            contact_score += 4
        if resume_data.get('phone'):
            contact_score += 3
        score += contact_score
        
        # Keywords (10 points)
        if job_description:
            jd_words = set(job_description.lower().split())
            resume_text = str(resume_data).lower()
            matches = sum(1 for word in jd_words if word in resume_text)
            score += min(10, matches // 5)
        else:
            score += 5  # Base score if no JD
        
        return min(100, score)
    
    @staticmethod
    def format_score_display(score_data: Dict) -> Dict:
        """
        Format ATS score data for display with actual calculated score
        
        Args:
            score_data: Raw score data from AI
            
        Returns:
            Formatted score data
        """
        try:
            overall_score = score_data.get('overall_score', 0)
            
            # Ensure score is within valid range
            overall_score = max(0, min(100, overall_score))
            
            # Determine score category
            if overall_score >= 80:
                category = "Excellent"
                color = "#27ae60"
                message = "Your resume is highly optimized for ATS systems!"
            elif overall_score >= 60:
                category = "Good"
                color = "#f39c12"
                message = "Your resume is well-optimized with room for improvement."
            elif overall_score >= 40:
                category = "Fair"
                color = "#e67e22"
                message = "Your resume needs significant improvements for ATS optimization."
            else:
                category = "Poor"
                color = "#e74c3c"
                message = "Your resume requires major revisions to pass ATS screening."
            
            return {
                'score': overall_score,
                'category': category,
                'color': color,
                'message': message,
                'category_scores': score_data.get('category_scores', {}),
                'breakdown': score_data.get('breakdown', {}),
                'strengths': score_data.get('strengths', []),
                'improvements': score_data.get('improvements', {}),
                'missing_keywords': score_data.get('missing_keywords', []),
                'summary': score_data.get('summary', ''),
                'last_updated': score_data.get('last_updated', '')
            }
        except Exception as e:
            print(f"Error formatting score: {e}")
            return {
                'score': 0,
                'category': 'Error',
                'color': '#95a5a6',
                'message': 'Unable to calculate ATS score',
                'breakdown': {},
                'strengths': [],
                'improvements': {},
                'missing_keywords': [],
                'summary': 'Error occurred during scoring',
                'last_updated': ''
            }
    
    @staticmethod
    def validate_resume_data(resume_data: Dict) -> tuple:
        """
        Validate resume data completeness
        
        Args:
            resume_data: Resume data dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ['name', 'email', 'phone', 'target_role']
        
        for field in required_fields:
            if not resume_data.get(field):
                return False, f"Missing required field: {field}"
        
        # Check if at least one of skills, experience, or education is present
        if not any([
            resume_data.get('skills'),
            resume_data.get('experience'),
            resume_data.get('education')
        ]):
            return False, "Resume must include at least skills, experience, or education"
        
        return True, ""
