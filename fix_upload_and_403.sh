#!/bin/bash

echo "=========================================="
echo "🔧 Complete Resume Upload Fix"
echo "=========================================="
echo ""

cd "/workspaces/weather-dash-board/ATS copy"

# Activate venv
echo "1️⃣ Activating Python environment..."
source "../venv/bin/activate"

echo ""
echo "2️⃣ Installing dependencies..."
pip install --quiet --upgrade streamlit groq PyPDF2 python-docx reportlab python-dotenv

echo ""
echo "3️⃣ Setting up uploads folder..."
mkdir -p uploads
chmod -R 777 uploads/

echo ""
echo "4️⃣ Creating sample resume for testing..."
python3 << 'EOF'
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors

pdf_path = "uploads/Sample_Resume.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
story = []
styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#003366'), alignment=1)
heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#003366'), font='Helvetica-Bold')

story.append(Paragraph("JOHN SMITH", title_style))
story.append(Spacer(1, 0.1))
story.append(Paragraph("New York, NY | (555) 123-4567 | john@email.com", styles['Normal']))
story.append(Spacer(1, 0.2))

story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
story.append(Paragraph("Experienced Software Engineer with 5+ years in full-stack development.", styles['Normal']))
story.append(Spacer(1, 0.15))

story.append(Paragraph("TECHNICAL SKILLS", heading_style))
story.append(Paragraph("Languages: Python, JavaScript, TypeScript", styles['Normal']))
story.append(Paragraph("Frameworks: Django, React, FastAPI, Node.js", styles['Normal']))
story.append(Spacer(1, 0.15))

story.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))
story.append(Paragraph("Senior Software Engineer | TechCorp Inc. | 2021 - Present", styles['Normal']))
story.append(Paragraph("• Led microservices architecture development", styles['Normal']))
story.append(Spacer(1, 0.1))

story.append(Paragraph("Software Engineer | StartupXYZ | 2019 - 2020", styles['Normal']))
story.append(Paragraph("• Developed RESTful APIs using FastAPI and Python", styles['Normal']))
story.append(Spacer(1, 0.15))

story.append(Paragraph("EDUCATION", heading_style))
story.append(Paragraph("BS in Computer Science | State University | 2019", styles['Normal']))

doc.build(story)
print("✅ Sample Resume created: uploads/Sample_Resume.pdf")
EOF

echo ""
echo "5️⃣ Clearing Streamlit cache..."
streamlit cache clear

echo ""
echo "6️⃣ Setting file permissions..."
chmod 777 ATS.py
chmod -R 777 uploads/
chmod -R 755 . 2>/dev/null || true

echo ""
echo "=========================================="
echo "✅ All Fixed!"
echo "=========================================="
echo ""
echo "📝 To Upload & Test Your Resume:"
echo ""
echo "  1. Start the app:"
echo "     streamlit run ATS.py"
echo ""
echo "  2. Go to Tab 1: '📝 Create Resume'"
echo ""
echo "  3. Click 'Upload existing resume to extract information'"
echo ""
echo "  4. Upload Sample_Resume.pdf from uploads/ folder"
echo ""
echo "  5. Click 'Parse Resume' button"
echo ""
echo "=========================================="
echo ""
echo "🔑 If you get 403 error:"
echo "   • Check .env file has valid GROQ_API_KEY"
echo "   • Verify API key starts with 'gsk_'"
echo "   • Make sure uploads/ folder has 777 permissions"
echo "   • Try: streamlit cache clear"
echo ""
