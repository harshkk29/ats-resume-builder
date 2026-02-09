# 🚀 AI-Powered ATS Resume Builder

An intelligent resume builder powered by AI that helps you create ATS-optimized resumes with real-time scoring and interactive editing.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🎯 Core Features
- **AI-Powered Resume Generation** - Generate professional resumes using Groq AI
- **Live PDF Preview** - Real-time A4-formatted resume preview
- **ATS Score Analysis** - Get detailed ATS compatibility scores with visual gauge
- **Interactive AI Agent** - Chat with AI to edit specific resume sections
- **Multiple Templates** - Choose from 4 professional templates (Professional, Modern, Creative, Minimal)
- **Smart Resume Parsing** - Upload PDF/DOCX and extract structured data
- **Version History** - Track changes with undo functionality
- **Dark Theme Support** - Fully optimized for both light and dark modes

### 📊 ATS Scoring
- Real-time ATS compatibility analysis
- Category-based scoring (Content, Format, Optimization, Best Practices)
- Detailed improvement suggestions
- Missing keywords detection
- Visual score gauge (0-100)

### 🤖 AI Agent Features
- Natural language editing commands
- Section-specific updates
- Change highlighting
- Auto-formatting suggestions
- Smart content optimization

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI/LLM:** Groq API (Llama 3.1)
- **PDF Processing:** PyPDF2, pdfplumber
- **Document Processing:** python-docx
- **Environment:** Python 3.11+

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- Groq API key ([Get one here](https://console.groq.com))

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ats-resume-builder.git
cd ats-resume-builder
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the application**
```bash
streamlit run AST.py
```

The app will open in your browser at `http://localhost:8501`

## 🎨 Usage

### Creating a Resume

1. **Upload Resume (Optional)**
   - Go to "AI Agent Resume" tab
   - Upload your existing PDF/DOCX resume
   - AI will extract and structure the data

2. **Generate with AI**
   - Fill in basic information
   - Provide job description (optional)
   - Click "Generate Resume"

3. **Edit with AI Agent**
   - Chat with the AI to make changes
   - Example: "Add Docker to skills"
   - Example: "Make the summary more concise"
   - Changes are highlighted in yellow

4. **Choose Template**
   - Select from sidebar: Professional, Modern, Creative, or Minimal
   - Template applies instantly

5. **Check ATS Score**
   - View your score (0-100)
   - Review detailed feedback
   - See missing keywords
   - Get improvement suggestions

6. **Download**
   - Download as PDF or DOCX
   - Choose your preferred template

## 📁 Project Structure

```
ATS_Modified_Final/
├── AST.py                      # Main Streamlit application
├── utils/
│   ├── __init__.py
│   ├── ai_helper.py           # AI/LLM integration
│   ├── resume_parser.py       # PDF/DOCX parsing
│   ├── resume_generator.py    # Resume generation
│   ├── ats_scorer.py          # ATS scoring logic
│   ├── resume_agent.py        # Interactive AI agent
│   └── templates.py           # Resume templates
├── test_resume_edits.py       # Test suite
├── verify_fixes.py            # Verification script
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .gitignore
└── README.md
```

## 🧪 Testing

Run the test suite to verify AI edits:
```bash
python test_resume_edits.py
```

Run verification script:
```bash
python verify_fixes.py
```

## 🎯 Key Improvements

This version includes several enhancements:

✅ **Fixed PDF Preview** - Proper HTML rendering using components  
✅ **Enhanced JSON Parsing** - Robust error handling  
✅ **Improved Data Extraction** - Better field mapping and validation  
✅ **ATS Score Gauge** - Accurate trigonometric rendering  
✅ **Template System** - 4 professional templates  
✅ **Dark Theme Support** - All text visible in dark mode  
✅ **HTML Escaping** - Prevents code injection  
✅ **Test Suite** - Validates AI functionality  

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | Yes |

## 📝 Templates

### Professional
Clean, traditional format ideal for corporate roles
- Colors: Navy blue + Blue
- Font: Arial
- Best for: Corporate, Finance, Legal

### Modern
Contemporary design with accent colors
- Colors: Black + Purple
- Font: Helvetica
- Best for: Tech, Startups, Marketing

### Creative
Bold design for creative industries
- Colors: Dark gray + Orange
- Font: Georgia + Arial
- Best for: Design, Media, Arts

### Minimal
Simple, elegant design focusing on content
- Colors: Pure black + Gray
- Font: Arial
- Best for: Academic, Research

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Groq for providing the AI API
- Streamlit for the amazing framework
- All contributors and users

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add your `GROQ_API_KEY` in Secrets
5. Deploy!

### Deploy to Heroku

```bash
# Create Procfile
echo "web: streamlit run AST.py --server.port=$PORT" > Procfile

# Deploy
heroku create your-app-name
heroku config:set GROQ_API_KEY=your_key
git push heroku main
```

## 📊 Screenshots

### Live PDF Preview
Beautiful A4-formatted resume with real-time updates

### ATS Score Analysis
Detailed scoring with visual gauge and improvement suggestions

### AI Agent Chat
Interactive editing with natural language commands

### Template Selection
Choose from 4 professional templates

---

**Made with ❤️ using Streamlit and Groq AI**
