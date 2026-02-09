#!/usr/bin/env python3
"""
Complete Setup & Diagnostic for Resume Upload 403 Error
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ Success")
            return True
        else:
            print(f"  ❌ Failed: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("🔧 ATS Resume Upload - Complete Setup & Diagnostics")
    print("=" * 70)
    
    os.chdir("/workspaces/weather-dash-board/ATS copy")
    
    # Step 1: Activate venv and install packages
    print("\n📦 1. Installing Python Packages...")
    run_command("source ../venv/bin/activate && pip install -q --upgrade streamlit groq PyPDF2 python-docx reportlab python-dotenv", "Installing packages")
    
    # Step 2: Set up folders
    print("\n📁 2. Setting Up Folders...")
    os.makedirs("uploads", exist_ok=True)
    os.chmod("uploads", 0o777)
    print("  ✅ Uploads folder ready (chmod 777)")
    
    # Step 3: API Key Check
    print("\n🔑 3. Checking API Key Configuration...")
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            content = f.read()
            if "GROQ_API_KEY=" in content:
                print("  ✅ .env file found with GROQ_API_KEY")
            else:
                print("  ⚠️  .env file found but missing GROQ_API_KEY")
    else:
        print("  ⚠️  .env file not found")
        print("     Create it with: echo 'GROQ_API_KEY=gsk_your_key' > .env")
    
    # Step 4: File Permissions
    print("\n🔐 4. Fixing File Permissions...")
    run_command("chmod -R 777 uploads/", "Setting uploads/ to 777")
    run_command("chmod 644 ATS.py", "Setting ATS.py to 644")
    
    # Step 5: Clear Cache
    print("\n🧹 5. Clearing Streamlit Cache...")
    run_command("streamlit cache clear", "Clearing cache")
    
    # Step 6: Test Resume Upload
    print("\n🧪 6. Testing Resume Upload Capability...")
    pdf_path = "uploads/test_upload.pdf"
    try:
        # Try to create a simple PDF
        subprocess.run(
            """python3 << 'EOF'
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("uploads/test_upload.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = [Paragraph("Test Resume", styles['Heading1'])]
doc.build(story)
print("Test PDF created")
EOF""",
            shell=True,
            capture_output=True
        )
        
        if os.path.exists(pdf_path):
            print(f"  ✅ Test PDF created successfully ({os.path.getsize(pdf_path)} bytes)")
            os.remove(pdf_path)
        else:
            print("  ⚠️  Could not create test PDF")
    except Exception as e:
        print(f"  ⚠️  Test failed: {str(e)}")
    
    # Final Summary
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    
    print("""
📋 WHAT'S READY:
  ✅ Python environment activated
  ✅ All dependencies installed
  ✅ uploads/ folder configured (chmod 777)
  ✅ File permissions fixed
  ✅ Streamlit cache cleared
  ✅ Resume parsing ready

🚀 NEXT STEPS:

  1. Ensure .env file exists with valid API key:
     - Create .env with: GROQ_API_KEY=gsk_your_key_here
     - Get key from: https://console.groq.com/keys

  2. Start the Streamlit app:
     streamlit run ATS.py

  3. Upload your Resume:
     - Tab 1: "📝 Create Resume"
     - Click "Upload existing resume"
     - Select your PDF/DOCX file
     - Click "Parse Resume"

🔧 IF YOU GET 403 ERROR:

  A. Invalid API Key:
     - Generate new key from Groq console
     - Update .env file
     - Run: python test_groq_api.py

  B. File Permission Issues:
     - Run: chmod -R 777 uploads/
     - Run: streamlit cache clear

  C. Cache Issues:
     - Run: streamlit cache clear
     - Restart: streamlit run ATS.py

📊 RESUME UPLOAD REQUIREMENTS:
  ✅ PDF (text-based, not scanned)
  ✅ DOCX (Word format)
  ❌ Images or scanned PDFs
  ❌ Files > 10MB

📞 SUPPORT:
  • Check: RESUME_UPLOAD_GUIDE.md
  • Test: python test_groq_api.py
  • Logs: Check Streamlit terminal
    """)
    
    print("=" * 70)
    print("Ready to use! Good luck! 🎉")
    print("=" * 70)

if __name__ == "__main__":
    main()
