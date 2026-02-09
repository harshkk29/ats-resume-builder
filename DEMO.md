# 🎥 Demo Guide - ATS Resume Builder

## Quick Start Demo

### Option 1: Using the Run Script
```bash
cd "/Users/harshvardhankhot/INTERNSHIP AI bot/ATS"
./run.sh
```

### Option 2: Direct Streamlit Command
```bash
cd "/Users/harshvardhankhot/INTERNSHIP AI bot/ATS"
streamlit run app.py
```

## Demo Walkthrough

### Scenario 1: Creating a Resume from Scratch

**Step 1: Enter Basic Information**
- Full Name: `John Doe`
- Email: `john.doe@example.com`
- Phone: `+1 234 567 8900`
- Target Job Role: `Software Engineer`

**Step 2: Add Job Description (Optional but Recommended)**
```
We are seeking a talented Software Engineer with experience in Python, 
JavaScript, and cloud technologies. The ideal candidate will have strong 
problem-solving skills and experience with modern web frameworks like 
React and Node.js. Experience with AWS or Google Cloud is a plus.
```

**Step 3: Fill Additional Information**
- **Skills**: `Python, JavaScript, React, Node.js, AWS, Docker, Git, SQL`
- **Education**:
  - Degree: `Bachelor of Science in Computer Science`
  - Institution: `Stanford University`
  - Year: `2023`
  - GPA: `3.8/4.0`
- **Experience**:
  - Title: `Software Engineer Intern`
  - Company: `Tech Corp`
  - Duration: `Jun 2022 - Aug 2022`
  - Responsibilities:
    ```
    Developed RESTful APIs using Python and Flask
    Improved application performance by 40% through code optimization
    Collaborated with cross-functional teams on agile projects
    ```
- **Projects**:
  - Name: `E-commerce Platform`
  - Description: `Built a full-stack e-commerce platform with user authentication, payment integration, and admin dashboard`
  - Technologies: `React, Node.js, MongoDB, Stripe API`
- **Certifications**:
  ```
  AWS Certified Solutions Architect
  Google Cloud Professional Developer
  ```

**Step 4: Generate Resume**
- Click "🚀 Generate ATS-Optimized Resume"
- Wait for AI processing (10-20 seconds)
- Review the generated content

**Step 5: Check ATS Score**
- Navigate to "📊 ATS Score" tab
- Review overall score (aim for 70+)
- Check breakdown by category
- Review strengths and improvement suggestions

**Step 6: Download Resume**
- Navigate to "💾 Download" tab
- Download PDF for applications
- Download DOCX for future edits

---

### Scenario 2: Uploading Existing Resume

**Step 1: Prepare Your Resume**
- Ensure your resume is in PDF or DOCX format
- File should be under 16MB

**Step 2: Upload and Parse**
- Enter mandatory fields (Name, Email, Phone, Target Role)
- Click "Upload Existing Resume"
- Select your resume file
- Wait for AI to parse and extract information

**Step 3: Review Extracted Data**
- Click "View Extracted Information" to see what was parsed
- The system will automatically populate fields

**Step 4: Add Job Description**
- Paste the job description you're targeting
- This helps optimize keywords and content

**Step 5: Generate Optimized Version**
- Click "Generate ATS-Optimized Resume"
- AI will enhance your existing content
- Review improvements and ATS score

---

## Expected Results

### ATS Score Interpretation

**Score 80-100 (Excellent)**
- ✅ Highly optimized for ATS systems
- ✅ Strong keyword match
- ✅ Well-structured content
- ✅ Ready to submit

**Score 60-79 (Good)**
- ✅ Good foundation
- ⚠️ Some improvements needed
- 💡 Add more relevant keywords
- 💡 Quantify achievements

**Score 40-59 (Fair)**
- ⚠️ Needs significant work
- 💡 Missing key sections
- 💡 Weak keyword match
- 💡 Add more details

**Score 0-39 (Poor)**
- ❌ Major revisions needed
- 💡 Incomplete information
- 💡 Poor formatting
- 💡 Missing critical sections

---

## AI Prompts Explanation

### 1. Resume Parsing Prompt
**Purpose**: Extract structured information from uploaded resume

**Key Elements**:
- Identifies name, contact info, skills
- Parses education history
- Extracts work experience with achievements
- Identifies projects and certifications

**Temperature**: 0.3 (Low for accuracy)

### 2. Content Generation Prompt
**Purpose**: Create optimized resume content

**Key Elements**:
- Generates compelling professional summary
- Optimizes skills for target role
- Rewrites achievements with action verbs
- Adds quantifiable metrics
- Incorporates job description keywords

**Temperature**: 0.5 (Moderate for creativity)

### 3. ATS Scoring Prompt
**Purpose**: Evaluate resume against ATS criteria

**Key Elements**:
- Keyword match analysis (30%)
- Skills alignment check (25%)
- Experience relevance (20%)
- Formatting assessment (15%)
- Completeness check (10%)

**Temperature**: 0.3 (Low for consistency)

---

## ATS Logic Breakdown

### Keyword Match (30 points)
- Extracts keywords from job description
- Compares with resume content
- Checks for industry-standard terms
- Evaluates keyword density

### Skills Alignment (25 points)
- Matches technical skills with requirements
- Evaluates soft skills presence
- Checks for role-specific competencies
- Assesses skill depth vs breadth

### Experience Relevance (20 points)
- Evaluates job titles alignment
- Checks experience duration
- Assesses achievement quality
- Reviews responsibility relevance

### Formatting & Structure (15 points)
- Checks for standard sections
- Evaluates heading hierarchy
- Assesses readability
- Reviews ATS-friendly formatting

### Completeness (10 points)
- Verifies all required sections
- Checks information depth
- Evaluates content balance
- Assesses overall presentation

---

## Video Walkthrough Script

### Introduction (30 seconds)
"Welcome to the AI-Powered ATS Resume Builder. This system helps students create professional, ATS-optimized resumes using advanced AI technology."

### Feature Overview (1 minute)
"The system has three main features:
1. Smart resume creation with AI-powered content generation
2. Comprehensive ATS scoring with detailed feedback
3. Professional PDF and DOCX downloads"

### Live Demo (3 minutes)
1. Enter student information
2. Upload existing resume (optional)
3. Add job description
4. Generate optimized resume
5. Review ATS score
6. Download final resume

### Results & Benefits (1 minute)
"The system provides:
- Professional summaries tailored to target roles
- Optimized keywords for ATS systems
- Quantifiable achievements
- Detailed scoring with improvement suggestions
- Ready-to-use professional resumes"

### Conclusion (30 seconds)
"This AI-powered system makes it easy for students to create ATS-friendly resumes that stand out to both automated systems and human recruiters."

---

## GitHub Repository Structure

```
ATS-Resume-Builder/
├── README.md                   # Project overview
├── DEMO.md                     # This file
├── requirements.txt            # Dependencies
├── .gitignore                 # Git ignore rules
├── run.sh                     # Quick start script
├── app.py                     # Main Streamlit app
├── utils/
│   ├── __init__.py
│   ├── ai_helper.py           # Groq AI integration
│   ├── resume_parser.py       # PDF/DOCX parsing
│   ├── resume_generator.py    # Resume generation
│   └── ats_scorer.py          # Scoring logic
└── uploads/
    └── .gitkeep
```

---

## Troubleshooting

### Issue: Application won't start
**Solution**: 
```bash
pip install -r requirements.txt --upgrade
streamlit run app.py
```

### Issue: Resume parsing fails
**Solution**: 
- Ensure file is PDF or DOCX
- Check file size (under 16MB)
- Try a different file

### Issue: Low ATS score
**Solution**:
- Add job description for better optimization
- Include more relevant keywords
- Add quantifiable achievements
- Ensure all sections are complete

### Issue: AI generation slow
**Solution**:
- Normal processing time: 10-20 seconds
- Check internet connection
- Groq API may be experiencing high traffic

---

## Next Steps After Demo

1. **Test with Real Resumes**: Upload your actual resume
2. **Try Different Roles**: Test with various job descriptions
3. **Compare Scores**: See how different content affects ATS score
4. **Iterate**: Use improvement suggestions to enhance resume
5. **Download**: Get both PDF and DOCX versions

---

## Contact & Support

For questions or issues, refer to the README.md file or check the code comments for detailed explanations.

**Built with ❤️ using Streamlit, Groq AI, and Python**
