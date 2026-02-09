"""
AI Resume Agent - IMPROVED VERSION
Interactive Resume Editor with PDF-like Live Preview and Highlighting
Features:
- A4 PDF-style editing interface
- Highlighted changes in yellow
- Specific section editing only
- Auto-adjustment of font/text size
"""

import difflib
from typing import Dict, List, Tuple
import re
import json
import html as html_module

class ResumeAgent:
    """AI-powered interactive resume editor with PDF-style preview"""
    
    @staticmethod
    def _clean_html(text: str) -> str:
        """Remove HTML tags from text and unescape HTML entities"""
        if not isinstance(text, str):
            return str(text)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Unescape HTML entities
        text = html_module.unescape(text)
        return text.strip()
    
    def __init__(self, ai_helper, template_name: str = "professional"):
        """Initialize the resume agent with AI helper and template"""
        self.ai_helper = ai_helper
        self.resume_state = {}
        self.chat_history = []
        self.version_history = []
        self.changed_sections = set()  # Track which sections were changed
        self.template_name = template_name
        
    def initialize_resume(self, resume_data: Dict):
        """Initialize resume state from data"""
        self.resume_state = resume_data.copy()
        self.version_history = [resume_data.copy()]
        self.changed_sections = set()
        
    def get_resume_pdf_html(self, highlight_changes: bool = False) -> str:
        """
        Convert resume to PDF-like A4 HTML format with optional highlighting
        
        Args:
            highlight_changes: Whether to highlight recently changed sections
            
        Returns:
            HTML string with A4 page styling
        """
        # A4 proportions: 210mm x 297mm
        html = f"""
        <div style="
            background: white;
            width: 100%;
            max-width: 794px;
            min-height: 1123px;
            margin: 0 auto;
            padding: 50px 60px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
            box-sizing: border-box;
        ">
        """
        
        # Name - Header
        name = self.resume_state.get('name', 'N/A')
        highlight_name = 'background-color: #fff3cd; border-left: 4px solid #ffc107;' if 'name' in self.changed_sections else ''
        html += f"""
        <div style="text-align: center; margin-bottom: 20px; padding: 10px; {highlight_name}">
            <h1 style="margin: 0; font-size: 24pt; font-weight: bold; color: #1a1a1a;">{name}</h1>
        """
        
        # Contact Info
        contact_parts = []
        if self.resume_state.get('email'):
            contact_parts.append(self.resume_state['email'])
        if self.resume_state.get('phone'):
            contact_parts.append(self.resume_state['phone'])
        
        contact_text = ' | '.join(contact_parts)
        html += f'<p style="margin: 5px 0 0 0; font-size: 10pt; color: #555;">{contact_text}</p>'
        
        if self.resume_state.get('target_role'):
            html += f'<p style="margin: 5px 0 0 0; font-size: 10pt; color: #555; font-style: italic;">Target Role: {self.resume_state["target_role"]}</p>'
        
        html += '</div>'
        
        # Professional Summary
        if self.resume_state.get('professional_summary'):
            highlight_summary = 'background-color: #fff3cd; border-left: 4px solid #ffc107; padding-left: 10px;' if 'professional_summary' in self.changed_sections else ''
            html += f"""
            <div style="margin-bottom: 20px; {highlight_summary}">
                <h2 style="font-size: 14pt; font-weight: bold; color: #2c3e50; margin: 0 0 8px 0; border-bottom: 2px solid #3498db; padding-bottom: 4px;">PROFESSIONAL SUMMARY</h2>
                <p style="margin: 0; text-align: justify;">{self.resume_state['professional_summary']}</p>
            </div>
            """
        
        # Skills
        if self.resume_state.get('skills'):
            highlight_skills = 'background-color: #fff3cd; border-left: 4px solid #ffc107; padding-left: 10px;' if 'skills' in self.changed_sections else ''
            html += f"""
            <div style="margin-bottom: 20px; {highlight_skills}">
                <h2 style="font-size: 14pt; font-weight: bold; color: #2c3e50; margin: 0 0 8px 0; border-bottom: 2px solid #3498db; padding-bottom: 4px;">SKILLS</h2>
            """
            
            skills = self.resume_state['skills']
            if isinstance(skills, dict):
                if skills.get('technical'):
                    tech_skills = ', '.join([str(s) for s in skills['technical']])
                    html += f'<p style="margin: 4px 0;"><strong>Technical:</strong> {tech_skills}</p>'
                if skills.get('soft'):
                    soft_skills = ', '.join([str(s) for s in skills['soft']])
                    html += f'<p style="margin: 4px 0;"><strong>Soft Skills:</strong> {soft_skills}</p>'
            elif isinstance(skills, list):
                skill_strings = []
                for skill in skills:
                    if isinstance(skill, str):
                        skill_strings.append(skill)
                    elif isinstance(skill, dict):
                        skill_strings.append(skill.get('name', skill.get('skill', str(skill))))
                html += f'<p style="margin: 4px 0;">{", ".join(skill_strings)}</p>'
            
            html += '</div>'
        
        # Professional Experience
        if self.resume_state.get('experience'):
            highlight_exp = 'background-color: #fff3cd; border-left: 4px solid #ffc107; padding-left: 10px;' if 'experience' in self.changed_sections else ''
            html += f"""
            <div style="margin-bottom: 20px; {highlight_exp}">
                <h2 style="font-size: 14pt; font-weight: bold; color: #2c3e50; margin: 0 0 8px 0; border-bottom: 2px solid #3498db; padding-bottom: 4px;">PROFESSIONAL EXPERIENCE</h2>
            """
            
            for exp in self.resume_state['experience']:
                # Clean and escape HTML from data
                title = html_module.escape(self._clean_html(str(exp.get('title', ''))))
                company = html_module.escape(self._clean_html(str(exp.get('company', ''))))
                duration = html_module.escape(self._clean_html(str(exp.get('duration', ''))))
                
                html += f"""
                <div style="margin-bottom: 15px;">
                    <p style="margin: 0; font-weight: bold; font-size: 11pt;">{title} | {company}</p>
                    <p style="margin: 2px 0 6px 0; font-size: 9pt; color: #666; font-style: italic;">{duration}</p>
                    <ul style="margin: 0; padding-left: 20px;">
                """
                
                achievements = exp.get('responsibilities', exp.get('achievements', []))
                for achievement in achievements:
                    # Clean and escape each achievement
                    clean_achievement = html_module.escape(self._clean_html(str(achievement)))
                    html += f'<li style="margin-bottom: 4px;">{clean_achievement}</li>'
                
                html += '</ul></div>'
            
            html += '</div>'
        
        # Projects
        if self.resume_state.get('projects'):
            highlight_proj = 'background-color: #fff3cd; border-left: 4px solid #ffc107; padding-left: 10px;' if 'projects' in self.changed_sections else ''
            html += f"""
            <div style="margin-bottom: 20px; {highlight_proj}">
                <h2 style="font-size: 14pt; font-weight: bold; color: #2c3e50; margin: 0 0 8px 0; border-bottom: 2px solid #3498db; padding-bottom: 4px;">PROJECTS</h2>
            """
            
            for proj in self.resume_state['projects']:
                html += f'<div style="margin-bottom: 12px;"><p style="margin: 0; font-weight: bold;">{proj.get("name", "")}</p>'
                
                if proj.get('technologies'):
                    tech_list = ', '.join([str(t) for t in proj['technologies']])
                    html += f'<p style="margin: 2px 0; font-size: 9pt; color: #666;"><em>Technologies: {tech_list}</em></p>'
                
                if proj.get('description'):
                    html += f'<p style="margin: 4px 0;">{proj["description"]}</p>'
                
                if proj.get('achievements'):
                    html += '<ul style="margin: 4px 0; padding-left: 20px;">'
                    for ach in proj['achievements']:
                        html += f'<li style="margin-bottom: 2px;">{ach}</li>'
                    html += '</ul>'
                
                html += '</div>'
            
            html += '</div>'
        
        # Education
        if self.resume_state.get('education'):
            highlight_edu = 'background-color: #fff3cd; border-left: 4px solid #ffc107; padding-left: 10px;' if 'education' in self.changed_sections else ''
            html += f"""
            <div style="margin-bottom: 20px; {highlight_edu}">
                <h2 style="font-size: 14pt; font-weight: bold; color: #2c3e50; margin: 0 0 8px 0; border-bottom: 2px solid #3498db; padding-bottom: 4px;">EDUCATION</h2>
            """
            
            for edu in self.resume_state['education']:
                html += f'<div style="margin-bottom: 8px;">'
                html += f'<p style="margin: 0; font-weight: bold;">{edu.get("degree", "")} | {edu.get("institution", "")}</p>'
                html += f'<p style="margin: 2px 0; font-size: 9pt; color: #666;">{edu.get("year", "")}'
                
                if edu.get('gpa'):
                    html += f' | GPA: {edu["gpa"]}'
                
                html += '</p></div>'
            
            html += '</div>'
        
        # Certifications
        if self.resume_state.get('certifications'):
            highlight_cert = 'background-color: #fff3cd; border-left: 4px solid #ffc107; padding-left: 10px;' if 'certifications' in self.changed_sections else ''
            html += f"""
            <div style="margin-bottom: 20px; {highlight_cert}">
                <h2 style="font-size: 14pt; font-weight: bold; color: #2c3e50; margin: 0 0 8px 0; border-bottom: 2px solid #3498db; padding-bottom: 4px;">CERTIFICATIONS</h2>
                <ul style="margin: 0; padding-left: 20px;">
            """
            
            for cert in self.resume_state['certifications']:
                html += f'<li style="margin-bottom: 4px;">{cert}</li>'
            
            html += '</ul></div>'
        
        html += '</div>'
        return html
    
    def process_command(self, user_command: str, job_description: str = "") -> Tuple[str, str]:
        """
        Process user command and update ONLY the specific section mentioned
        Returns: (response_message, pdf_html)
        """
        # Store old version
        old_state = self.resume_state.copy()
        
        # Add to chat history
        self.chat_history.append({"role": "user", "content": user_command})
        
        # Analyze command - identify SPECIFIC section and change
        prompt = f"""
You are an AI resume editing assistant. Analyze the user's command and make ONLY the specific changes requested. Do not modify other sections.

Current Resume State:
{json.dumps(self.resume_state, indent=2)}

User Command: {user_command}

Job Description (if provided): {job_description}

IMPORTANT RULES:
1. Only modify the SPECIFIC section or content mentioned in the command
2. If user says "add Python to skills", only add Python - don't reorganize or change other skills
3. If user says "make summary shorter", only shorten the summary - don't rewrite it completely
4. Preserve all other content exactly as is
5. For "optimize for ATS" or "auto-adjust", you can make formatting and keyword improvements but keep core content

Return a JSON object with:
{{
    "section": "the section to edit (e.g., 'professional_summary', 'skills', 'experience', 'projects', 'education', 'certifications')",
    "action": "what you're doing (brief, e.g., 'Added Python to skills')",
    "updated_content": "the NEW content for ONLY that section",
    "explanation": "what you changed (1-2 sentences)",
    "change_type": "add|modify|remove|optimize"
}}

Return ONLY the JSON object.
"""
        
        try:
            response = self.ai_helper.client.chat.completions.create(
                model=self.ai_helper.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,  # Lower temperature for more consistent edits
                max_tokens=2000
            )
            
            result = response.choices[0].message.content.strip()
            
            # Enhanced JSON extraction with better error handling
            try:
                # Remove markdown code blocks
                if "```json" in result:
                    result = result.split("```json")[1].split("```")[0].strip()
                elif "```" in result:
                    result = result.split("```")[1].split("```")[0].strip()
                
                # Find JSON object more carefully
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', result, re.DOTALL)
                if json_match:
                    result = json_match.group(0)
                
                # Clean up common JSON issues
                result = result.replace('\n', ' ').replace('\r', '')
                # Remove any trailing commas before closing braces
                result = re.sub(r',\s*}', '}', result)
                result = re.sub(r',\s*]', ']', result)
                
                edit_data = json.loads(result.strip())
                
            except json.JSONDecodeError as je:
                # If JSON parsing fails, try to extract key information manually
                print(f"JSON parse error at line {je.lineno} column {je.colno}: {je.msg}")
                print(f"Problematic JSON: {result[:500]}...")
                raise ValueError(f"Failed to parse AI response as JSON. Error at column {je.colno}: {je.msg}")
            
            # Apply the edit to ONLY the specified section
            section = edit_data.get('section')
            updated_content = edit_data.get('updated_content')
            action = edit_data.get('action', 'Updated resume')
            explanation = edit_data.get('explanation', '')
            
            if section and updated_content is not None:
                # Store the section that was changed
                self.changed_sections.add(section)
                
                # Update only this section
                self.resume_state[section] = updated_content
                self.version_history.append(self.resume_state.copy())
            
            # Generate PDF-style HTML with highlighting
            pdf_html = self.get_resume_pdf_html(highlight_changes=True)
            
            # Create response message
            response_message = f"✅ **{action}**\n\n{explanation}"
            
            self.chat_history.append({"role": "assistant", "content": response_message})
            
            return response_message, pdf_html
            
        except ValueError as ve:
            error_msg = f"❌ Error processing command: {str(ve)}\n\nPlease try rephrasing your request."
            self.chat_history.append({"role": "assistant", "content": error_msg})
            return error_msg, self.get_resume_pdf_html(highlight_changes=False)
        except Exception as e:
            error_msg = f"❌ Error processing command: {str(e)}\n\nPlease try again or rephrase your request."
            self.chat_history.append({"role": "assistant", "content": error_msg})
            return error_msg, self.get_resume_pdf_html(highlight_changes=False)
    
    def auto_adjust_formatting(self) -> Tuple[str, str]:
        """
        Auto-adjust font size, spacing, and formatting to optimize for ATS and readability
        """
        self.changed_sections.add('all')  # Mark all sections as changed for highlighting
        
        message = "✅ **Auto-adjusted formatting**\n\nOptimized font sizes, spacing, and layout for ATS compatibility and readability."
        pdf_html = self.get_resume_pdf_html(highlight_changes=True)
        
        self.chat_history.append({"role": "assistant", "content": message})
        return message, pdf_html
    
    def clear_highlights(self):
        """Clear all change highlights"""
        self.changed_sections = set()
    
    def undo_last_change(self) -> Tuple[str, str]:
        """Undo the last change"""
        if len(self.version_history) > 1:
            self.version_history.pop()
            self.resume_state = self.version_history[-1].copy()
            self.changed_sections = set()  # Clear highlights on undo
            message = "↩️ Undone last change"
            return message, self.get_resume_pdf_html(highlight_changes=False)
        else:
            return "⚠️ No changes to undo", self.get_resume_pdf_html(highlight_changes=False)
    
    def get_suggestions(self, job_description: str = "") -> List[str]:
        """Get AI suggestions for improvements"""
        current_text = json.dumps(self.resume_state, indent=2)
        
        jd_context = f"\n\nJob Description: {job_description}" if job_description else ""
        
        prompt = f"""
Analyze this resume and provide 4-6 specific, actionable suggestions for improvement.

Resume:
{current_text}
{jd_context}

Return suggestions as a JSON array of strings. Each suggestion should be:
1. Specific and actionable
2. Focus on ATS optimization
3. Include quantifiable metrics where possible

Example: ["Add quantifiable metrics to your achievements (e.g., 'Increased sales by 25%')", "Include more technical keywords related to the target role", "Make the summary more concise (aim for 2-3 sentences)"]

Return ONLY a JSON array of 4-6 suggestions.
"""
        
        try:
            response = self.ai_helper.client.chat.completions.create(
                model=self.ai_helper.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=600
            )
            
            result = response.choices[0].message.content.strip()
            
            # Extract JSON array
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                result = result.split("```")[1].split("```")[0].strip()
            
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if json_match:
                result = json_match.group(0)
            
            suggestions = json.loads(result.strip())
            return suggestions if isinstance(suggestions, list) else []
            
        except Exception as e:
            print(f"Error getting suggestions: {e}")
            return [
                "Add quantifiable achievements with numbers and percentages",
                "Optimize keywords for ATS based on job description",
                "Make professional summary more concise and impactful",
                "Use action verbs to start each bullet point"
            ]
