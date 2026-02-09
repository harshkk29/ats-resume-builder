#!/bin/bash

echo "=========================================="
echo "🚀 Complete ATS Setup & 403 Error Fix"
echo "=========================================="
echo ""

cd "/workspaces/weather-dash-board/ATS copy"

# Activate venv
echo "1️⃣ Activating Python environment..."
source "../venv/bin/activate"

echo ""
echo "2️⃣ Installing all dependencies..."
pip install --quiet --upgrade streamlit groq PyPDF2 python-docx reportlab python-dotenv

echo ""
echo "3️⃣ Clearing Streamlit cache..."
streamlit cache clear

echo ""
echo "4️⃣ Setting up file permissions..."
chmod -R 777 uploads/
chmod -R 755 templates/ static/ 2>/dev/null || true
chmod 644 ATS.py

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "🔐 Next Step: Configure Your API Key"
echo ""
echo "Option A: Create .env File (Recommended)"
echo "   1. Run: echo 'GROQ_API_KEY=gsk_your_key_here' > .env"
echo "   2. Get key from: https://console.groq.com/keys"
echo "   3. Replace 'gsk_your_key_here' with your actual key"
echo ""
echo "Option B: Test Your API Key First"
echo "   1. Create .env file with your API key"
echo "   2. Run: python test_groq_api.py"
echo "   3. If test passes, start the app"
echo ""
echo "Option C: Start the App"
echo "   streamlit run ATS.py"
echo ""
echo "=========================================="
echo ""
