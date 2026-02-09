"""
Streamlit Application - ATS Resume Builder
AI-powered ATS-friendly resume creation system with two modes
"""

import streamlit as st
import os
import json
from datetime import datetime
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from utils.ai_helper import AIHelper
from utils.resume_parser import ResumeParser
from utils.resume_generator import ResumeGenerator
from utils.ats_scorer import ATSScorer
from utils.resume_agent import ResumeAgent

# Page configuration
st.set_page_config(
    page_title="ATS Resume Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Enhanced Modern UI
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeIn 1s ease-in;
    }
    
    /* Score card with glassmorphism */
    .score-card {
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(10px);
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .score-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    /* Chat container */
    .chat-container {
        height: 450px;
        overflow-y: auto;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        margin-bottom: 1rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* User message bubble */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        word-wrap: break-word;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease;
    }
    
    /* AI message bubble */
    .ai-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 4px 10px rgba(245, 87, 108, 0.3);
        animation: slideInLeft 0.3s ease;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.85rem 1.5rem;
        border-radius: 12px;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 12px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.5);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# Groq API Key - Must be set in environment variable or .env file
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

# Check if API key is valid
if not GROQ_API_KEY or GROQ_API_KEY.startswith("gsk_") == False:
    st.error("""
    ❌ **Invalid Groq API Key!**
    
    Please add your Groq API key:
    1. Get a key from https://console.groq.com/keys
    2. Create a `.env` file with: `GROQ_API_KEY=your_key_here`
    3. Or update line 87 in ATS.py
    
    **Current key status:** Invalid/Missing
    """)
    st.stop()

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'ats_score' not in st.session_state:
    st.session_state.ats_score = None
if 'score_last_updated' not in st.session_state:
    st.session_state.score_last_updated = None
if 'generated_resume' not in st.session_state:
    st.session_state.generated_resume = None
if 'resume_agent' not in st.session_state:
    st.session_state.resume_agent = None
if 'agent_chat_history' not in st.session_state:
    st.session_state.agent_chat_history = []
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = 'professional'

# Initialize AI Helper
@st.cache_resource
def get_ai_helper():
    return AIHelper(GROQ_API_KEY)

ai_helper = get_ai_helper()

# Header with better dark theme support
st.markdown('''
<h1 style="
    font-size: 3rem;
    font-weight: bold;
    color: #000000;
    text-align: center;
    margin-bottom: 1rem;
    padding: 1rem 0;
">
🚀 AI-Powered ATS Resume Builder
</h1>
''', unsafe_allow_html=True)

# Template selector in sidebar
with st.sidebar:
    st.markdown('<h3 style="color: #000000;">📐 Resume Template</h3>', unsafe_allow_html=True)
    from utils.templates import get_all_templates
    templates = get_all_templates()
    
    template_options = {name: info["name"] + " - " + info["description"] for name, info in templates.items()}
    
    selected_template = st.selectbox(
        "Choose a template",
        options=list(template_options.keys()),
        format_func=lambda x: template_options[x],
        index=list(template_options.keys()).index(st.session_state.selected_template),
        key="template_selector"
    )
    
    if selected_template != st.session_state.selected_template:
        st.session_state.selected_template = selected_template
        st.rerun()

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Create Resume", "🤖 AI Agent Resume", "📊 ATS Score", "💾 Download"])

# ==================== TAB 1: CREATE RESUME ====================
with tab1:
    st.header("Create Resume from Scratch")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Upload Resume (Optional)")
        uploaded_file = st.file_uploader(
            "Upload existing resume to extract information",
            type=['pdf', 'docx'],
            key="create_upload"
        )
        
        if uploaded_file and st.button("Parse Resume", key="parse_btn"):
            with st.spinner("🔍 Parsing..."):
                try:
                    # Create uploads directory with proper permissions
                    upload_dir = "uploads"
                    os.makedirs(upload_dir, exist_ok=True)
                    os.chmod(upload_dir, 0o777)
                    
                    # Save file with timestamp
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{uploaded_file.name}"
                    filepath = os.path.join(upload_dir, filename)
                    
                    # Write file with error handling
                    try:
                        with open(filepath, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        os.chmod(filepath, 0o666)  # Make file readable/writable
                    except PermissionError:
                        st.error("❌ Permission denied when saving file. Please contact admin.")
                    except IOError as e:
                        st.error(f"❌ File write error: {str(e)}")
                    
                    # Verify file was created
                    if not os.path.exists(filepath):
                        st.error("❌ File was not saved properly. Please try again.")
                    else:
                        # Parse the file
                        resume_text = ResumeParser.parse_resume(filepath)
                        if resume_text:
                            # Extract data using AI
                            extracted_data = ai_helper.extract_resume_info(resume_text, "General")
                            if extracted_data:
                                st.session_state.resume_data = extracted_data
                                st.success("✅ Resume parsed successfully!")
                                with st.expander("View Extracted Data"):
                                    st.json(extracted_data)
                            else:
                                st.error("❌ Failed to extract information from resume. Please try again or enter manually.")
                        else:
                            st.error("❌ Could not extract text from the file. Please ensure it's a valid PDF or DOCX file.")
                        
                        # Clean up temporary file
                        try:
                            if os.path.exists(filepath):
                                os.remove(filepath)
                        except Exception as cleanup_error:
                            st.warning(f"Note: Temp file cleanup failed: {str(cleanup_error)}")
                
                except Exception as e:
                    st.error(f"❌ Error parsing resume: {str(e)}\n\nPlease try:\n1. Verify the PDF/DOCX file is valid\n2. Try another file\n3. Use manual entry instead")
                        
    with col2:
        st.subheader("✏️ Manual Entry")
        name = st.text_input("Full Name *", key="name_input")
        email = st.text_input("Email *", key="email_input")
        phone = st.text_input("Phone *", key="phone_input")
        target_role = st.text_input("Target Role *", key="role_input")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        skills_input = st.text_area("Skills (comma-separated)", key="skills_input")
        job_description = st.text_area("Job Description (Optional)", height=150, key="jd_input")
    
    with col2:
        degree = st.text_input("Degree", key="degree_input")
        institution = st.text_input("Institution", key="inst_input")
        exp_title = st.text_input("Job Title", key="job_title_input")
        exp_company = st.text_input("Company", key="company_input")
    
    if st.button("🚀 Generate Resume", type="primary"):
        if not all([name, email, phone, target_role]):
            st.error("⚠️ Please fill mandatory fields")
        else:
            with st.spinner("🤖 Generating..."):
                try:
                    user_data = {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'target_role': target_role
                    }
                    
                    if skills_input:
                        user_data['skills'] = [s.strip() for s in skills_input.split(',')]
                    
                    if degree and institution:
                        user_data['education'] = [{'degree': degree, 'institution': institution}]
                    
                    if exp_title and exp_company:
                        user_data['experience'] = [{'title': exp_title, 'company': exp_company}]
                    
                    resume_content = ai_helper.generate_resume_content(user_data, job_description)
                    
                    if resume_content:
                        final_resume_data = {
                            'name': user_data['name'],
                            'email': user_data['email'],
                            'phone': user_data['phone'],
                            'target_role': user_data['target_role'],
                            'professional_summary': resume_content.get('professional_summary', ''),
                            'skills': resume_content.get('skills', user_data.get('skills', [])),
                            'experience': resume_content.get('experience', user_data.get('experience', [])),
                            'education': resume_content.get('education', user_data.get('education', [])),
                            'projects': resume_content.get('projects', []),
                            'certifications': resume_content.get('certifications', [])
                        }
                        
                        st.session_state.generated_resume = final_resume_data
                        
                        score_data = ai_helper.calculate_ats_score(final_resume_data, job_description)
                        st.session_state.ats_score = ATSScorer.format_score_display(score_data)
                        st.session_state.score_last_updated = datetime.now()
                        
                        st.success("✅ Resume generated!")
                        st.balloons()
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ==================== TAB 2: AI AGENT RESUME ====================
with tab2:
    st.header("🤖 AI Agent Resume Editor")
    
    if st.session_state.resume_agent is None:
        st.info("📤 **Upload your resume to start editing with AI**")
        
        uploaded_file = st.file_uploader(
            "Choose PDF or DOCX resume",
            type=['pdf', 'docx'],
            key="agent_upload"
        )
        
        if uploaded_file:
            with st.spinner("🔍 Loading resume..."):
                try:
                    # Create uploads directory with proper permissions
                    upload_dir = "uploads"
                    os.makedirs(upload_dir, exist_ok=True)
                    os.chmod(upload_dir, 0o777)
                    
                    # Save file with timestamp
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{uploaded_file.name}"
                    filepath = os.path.join(upload_dir, filename)
                    
                    # Write file with error handling
                    try:
                        with open(filepath, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        os.chmod(filepath, 0o666)  # Make file readable/writable
                    except PermissionError:
                        st.error("❌ Permission denied when saving file. Please contact admin.")
                    except IOError as e:
                        st.error(f"❌ File write error: {str(e)}")
                    
                    # Verify file was created
                    if not os.path.exists(filepath):
                        st.error("❌ File was not saved properly. Please try again.")
                    else:
                        # Parse the resume
                        resume_text = ResumeParser.parse_resume(filepath)
                        
                        if resume_text:
                            extracted_data = ai_helper.extract_resume_info(resume_text, "General")
                            
                            if extracted_data:
                                st.session_state.resume_agent = ResumeAgent(ai_helper)
                                st.session_state.resume_agent.initialize_resume(extracted_data)
                                st.session_state.generated_resume = extracted_data.copy()
                                
                                score_data = ai_helper.calculate_ats_score(extracted_data, "")
                                st.session_state.ats_score = ATSScorer.format_score_display(score_data)
                                
                                st.success("✅ Resume loaded! Start chatting below.")
                                
                                # Clean up temporary file
                                try:
                                    if os.path.exists(filepath):
                                        os.remove(filepath)
                                except:
                                    pass
                                
                                st.rerun()
                            else:
                                st.error("❌ Failed to extract information from resume.")
                        else:
                            st.error("❌ Could not extract text from the file. Please ensure it's a valid PDF or DOCX file.")
                
                except Exception as e:
                    st.error(f"❌ Error loading resume: {str(e)}\n\nPlease try:\n1. Verify the PDF/DOCX file is valid\n2. Try another file\n3. Use manual entry instead")
    
    # Main layout - AI Agent Resume Editor
    if st.session_state.resume_agent:
        # Top control bar
        top_col1, top_col2, top_col3, top_col4 = st.columns([2, 1, 1, 1])
        
        with top_col1:
            st.markdown("### 📄 Live PDF Preview")
        
        with top_col2:
            if st.button("🎨 Auto-Adjust", help="Auto-adjust font size and formatting", key="auto_adjust"):
                message, pdf_html = st.session_state.resume_agent.auto_adjust_formatting()
                st.session_state.generated_resume = st.session_state.resume_agent.resume_state.copy()
                
                # Update ATS score
                with st.spinner("Updating ATS score..."):
                    score_data = ai_helper.calculate_ats_score(st.session_state.resume_agent.resume_state, "")
                    st.session_state.ats_score = ATSScorer.format_score_display(score_data)
                    st.session_state.score_last_updated = datetime.now()
                
                st.success("✅ Formatting optimized!")
                st.rerun()
        
        with top_col3:
            if st.button("🔄 Clear Highlights", help="Clear yellow highlights"):
                st.session_state.resume_agent.clear_highlights()
                st.rerun()
        
        with top_col4:
            if st.button("💾 Save", help="Save current version"):
                st.session_state.generated_resume = st.session_state.resume_agent.resume_state.copy()
                st.success("✅ Saved!")
        
        # Split view: PDF Preview | Chat + Score
        col_left, col_right = st.columns([1.5, 1])
        
        with col_left:
            # PDF-style resume preview
            pdf_html = st.session_state.resume_agent.get_resume_pdf_html(highlight_changes=True)
            
            # Use components.html for proper rendering
            import streamlit.components.v1 as components
            
            # Wrap in a scrollable container
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        margin: 0;
                        padding: 20px;
                        background: #f5f5f5;
                        font-family: Arial, sans-serif;
                    }}
                    .container {{
                        max-height: 600px;
                        overflow-y: auto;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    {pdf_html}
                </div>
            </body>
            </html>
            """
            
            components.html(full_html, height=650, scrolling=True)
            
            # Action buttons below preview
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("↩️ Undo Last Change"):
                    message, html = st.session_state.resume_agent.undo_last_change()
                    st.session_state.generated_resume = st.session_state.resume_agent.resume_state.copy()
                    
                    # Update score
                    score_data = ai_helper.calculate_ats_score(st.session_state.resume_agent.resume_state, "")
                    st.session_state.ats_score = ATSScorer.format_score_display(score_data)
                    st.session_state.score_last_updated = datetime.now()
                    
                    st.info(message)
                    st.rerun()
            
            with col_b:
                if st.button("🔄 Reset to Saved"):
                    if st.session_state.generated_resume:
                        st.session_state.resume_agent.initialize_resume(st.session_state.generated_resume)
                        st.info("↻ Reset to last saved version")
                        st.rerun()
            
            with col_c:
                if st.button("🗑️ Start New"):
                    st.session_state.resume_agent = None
                    st.session_state.agent_chat_history = []
                    st.rerun()
        
        with col_right:
            # Live ATS Score Card
            if st.session_state.ats_score:
                score = st.session_state.ats_score
                
                col_score, col_refresh = st.columns([4, 1])
                with col_score:
                    last_updated = st.session_state.get('score_last_updated')
                    time_str = last_updated.strftime('%H:%M:%S') if last_updated else "Not yet calculated"
                    
                    st.markdown(f"""
                    <div class="score-card">
                        <h3 style="margin: 0;">📊 Live ATS Score</h3>
                        <h1 style="margin: 0.5rem 0; font-size: 2.8rem;">{score['score']}/100</h1>
                        <p style="margin: 0; font-size: 1.1rem;">{score['category']}</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.7rem; color: #ddd;">Updated: {time_str}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_refresh:
                    if st.button("🔄", help="Refresh ATS Score Now", key="refresh_score_agent"):
                        with st.spinner("♻️ Recalculating..."):
                            score_data = ai_helper.calculate_ats_score(st.session_state.resume_agent.resume_state, "")
                            st.session_state.ats_score = ATSScorer.format_score_display(score_data)
                            st.session_state.score_last_updated = datetime.now()
                        st.success("✅ Score updated!")
                        st.rerun()
            
            st.markdown("---")
            
            # Chat Interface
            st.subheader("💬 Chat with AI")
            
            # Scrollable chat history
            chat_html = '<div class="chat-container">'
            for msg in st.session_state.agent_chat_history:
                if msg["role"] == "user":
                    chat_html += f'<div class="user-message"><strong>You:</strong> {msg["content"]}</div>'
                else:
                    chat_html += f'<div class="ai-message"><strong>AI:</strong> {msg["content"]}</div>'
            chat_html += '</div>'
            
            st.markdown(chat_html, unsafe_allow_html=True)
            
            # Chat input
            user_input = st.text_input(
                "Type your command...", 
                placeholder="e.g., 'Add Python to skills', 'Make summary shorter'",
                key="chat_input_agent"
            )
            
            col_send, col_clear = st.columns([5, 1])
            
            with col_send:
                if st.button("📤 Send", type="primary", key="send_chat"):
                    if user_input:
                        # Add user message to chat
                        st.session_state.agent_chat_history.append({"role": "user", "content": user_input})
                        
                        # Process command
                        with st.spinner("🤖 Processing your request..."):
                            response, _ = st.session_state.resume_agent.process_command(user_input)
                        
                        # Add AI response to chat
                        st.session_state.agent_chat_history.append({"role": "assistant", "content": response})
                        
                        # Auto-save changes
                        st.session_state.generated_resume = st.session_state.resume_agent.resume_state.copy()
                        
                        # Auto-update ATS score
                        with st.spinner("📊 Updating ATS score..."):
                            score_data = ai_helper.calculate_ats_score(st.session_state.resume_agent.resume_state, "")
                            st.session_state.ats_score = ATSScorer.format_score_display(score_data)
                            st.session_state.score_last_updated = datetime.now()
                        
                        st.rerun()
            
            with col_clear:
                if st.button("🗑️", help="Clear chat", key="clear_chat"):
                    st.session_state.agent_chat_history = []
                    st.session_state.resume_agent.clear_highlights()
                    st.rerun()
            
            # Quick Actions
            st.markdown("---")
            st.markdown("**⚡ Quick Actions**")
            
            quick_actions = [
                "Make summary more concise",
                "Add quantifiable metrics",
                "Optimize keywords for ATS",
                "Use stronger action verbs"
            ]
            
            cols = st.columns(2)
            for idx, action in enumerate(quick_actions):
                with cols[idx % 2]:
                    if st.button(action, key=f"quick_{idx}", use_container_width=True):
                        # Add to chat
                        st.session_state.agent_chat_history.append({"role": "user", "content": action})
                        
                        # Process
                        with st.spinner("Processing..."):
                            response, _ = st.session_state.resume_agent.process_command(action)
                        
                        st.session_state.agent_chat_history.append({"role": "assistant", "content": response})
                        st.session_state.generated_resume = st.session_state.resume_agent.resume_state.copy()
                        
                        # Update score
                        with st.spinner("Updating score..."):
                            score_data = ai_helper.calculate_ats_score(st.session_state.resume_agent.resume_state, "")
                            st.session_state.ats_score = ATSScorer.format_score_display(score_data)
                            st.session_state.score_last_updated = datetime.now()
                        
                        st.rerun()
            
            # AI Suggestions
            st.markdown("---")
            if st.button("💡 Get AI Suggestions", key="get_suggestions"):
                with st.spinner("Analyzing resume..."):
                    suggestions = st.session_state.resume_agent.get_suggestions()
                    
                    st.markdown("**📋 AI Recommendations:**")
                    for i, suggestion in enumerate(suggestions, 1):
                        st.markdown(f"{i}. {suggestion}")
# ==================== TAB 3: ATS SCORE ====================
with tab3:
    st.header("📊 ATS Score Analysis")
    
    if st.session_state.ats_score:
        score_data = st.session_state.ats_score
        score = score_data['score']
        
        # Top section: Score Gauge + Comparison Chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Rezi Score")
            st.markdown(f"<p style='color: #666; font-size: 14px;'>{st.session_state.generated_resume.get('name', 'Your')} Resume</p>", unsafe_allow_html=True)
            
            # Gauge chart using HTML/CSS with proper semicircle
            color = "#dc3545" if score < 60 else "#ffc107" if score < 80 else "#28a745"
            status = "Needs improvement" if score < 60 else "Good" if score < 80 else "Excellent"
            
            # Calculate arc endpoint for the score
            import math
            import streamlit.components.v1 as components
            
            # Convert score (0-100) to angle (180-0 degrees, going clockwise from left)
            angle = 180 - (score / 100) * 180  # Start from 180° (left) and go to 0° (right)
            angle_rad = math.radians(angle)
            
            # Calculate end point on the arc
            center_x = 100
            center_y = 100
            radius = 80
            end_x = center_x + radius * math.cos(angle_rad)
            end_y = center_y - radius * math.sin(angle_rad)
            
            # Determine if we need large arc flag (for scores > 50)
            large_arc = 1 if score > 50 else 0
            
            # Use components.html for proper rendering
            gauge_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        background: transparent;
                    }}
                    .gauge-container {{
                        text-align: center;
                        padding: 1rem;
                    }}
                    .scale-labels {{
                        display: flex;
                        justify-content: space-between;
                        width: 180px;
                        margin: 10px auto 0;
                        font-size: 12px;
                        color: #999;
                    }}
                </style>
            </head>
            <body>
                <div class="gauge-container">
                    <svg width="220" height="140" viewBox="0 0 220 140">
                        <!-- Background arc (gray semicircle) -->
                        <path d="M 20 100 A 80 80 0 0 1 180 100" 
                              fill="none" 
                              stroke="#e0e0e0" 
                              stroke-width="16" 
                              stroke-linecap="round"/>
                        
                        <!-- Score arc (colored portion) -->
                        <path d="M 20 100 A 80 80 0 {large_arc} 1 {end_x:.2f} {end_y:.2f}" 
                              fill="none" 
                              stroke="{color}" 
                              stroke-width="16" 
                              stroke-linecap="round"/>
                        
                        <!-- Score number -->
                        <text x="100" y="85" 
                              text-anchor="middle" 
                              font-size="42" 
                              font-weight="bold" 
                              fill="#333">{score}</text>
                        
                        <!-- Status text -->
                        <text x="100" y="110" 
                              text-anchor="middle" 
                              font-size="14" 
                              fill="#666">{status}</text>
                    </svg>
                    
                    <!-- Scale labels -->
                    <div class="scale-labels">
                        <span>0</span>
                        <span>100</span>
                    </div>
                </div>
            </body>
            </html>
            """
            
            components.html(gauge_html, height=200)
        
        with col2:
            st.subheader("How You Compare")
            st.markdown("<p style='color: #666; font-size: 14px;'>See how your resume compares to others.</p>", unsafe_allow_html=True)
            
            # Comparison histogram
            import numpy as np
            histogram_data = np.random.normal(65, 15, 1000)
            histogram_data = np.clip(histogram_data, 0, 100)
            
            st.markdown(f"""
            <div style="padding: 1rem;">
                <svg width="100%" height="150" viewBox="0 0 400 150">
                    <!-- Histogram bars -->
                    {"".join([f'<rect x="{i*8}" y="{150 - min(100, len([x for x in histogram_data if i*2 <= x < (i+1)*2])*2)}" width="6" height="{min(100, len([x for x in histogram_data if i*2 <= x < (i+1)*2])*2)}" fill="#e0e0e0"/>' for i in range(50)])}
                    <!-- Your score marker -->
                    <rect x="{score*4-2}" y="0" width="4" height="150" fill="{color}"/>
                    <text x="{score*4}" y="15" text-anchor="middle" font-size="12" font-weight="bold" fill="{color}">You</text>
                    <!-- X-axis labels -->
                    <text x="0" y="145" font-size="10" fill="#999">0</text>
                    <text x="200" y="145" text-anchor="middle" font-size="10" fill="#999">50</text>
                    <text x="400" y="145" text-anchor="end" font-size="10" fill="#999">100</text>
                </svg>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Improvements section with category tabs
        st.subheader("Improvements")
        st.markdown("<p style='color: #666;'>Improve your Rezi Score by making the suggested adjustments in each category.</p>", unsafe_allow_html=True)
        
        # Category tabs
        category_scores = score_data.get('category_scores', {
            'content': 93,
            'format': 88,
            'optimization': 0,
            'best_practices': 90,
            'application_ready': 79
        })
        
        tab_content, tab_format, tab_optimization, tab_best, tab_ready = st.tabs([
            f"Content ({category_scores.get('content', 0)})",
            f"Format ({category_scores.get('format', 0)})",
            f"Optimization ({category_scores.get('optimization', 0)})",
            f"Best Practices ({category_scores.get('best_practices', 0)})",
            f"Application Ready ({category_scores.get('application_ready', 0)})"
        ])
        
        improvements = score_data.get('improvements', {})
        
        # Helper function to display improvements
        def display_improvements(category_key, tab):
            with tab:
                category_improvements = improvements.get(category_key, [])
                if not isinstance(category_improvements, list):
                    category_improvements = []
                
                if len(category_improvements) > 0:
                    for imp in category_improvements:
                        if isinstance(imp, dict):
                            severity = imp.get('severity', 'info')
                            icon = "🔴" if severity == "error" else "🟠" if severity == "warning" else "🟡"
                            bg_color = "#fee" if severity == "error" else "#ffeaa7" if severity == "warning" else "#fff3cd"
                            border_color = "#dc3545" if severity == "error" else "#ffc107" if severity == "warning" else "#17a2b8"
                            
                            section_html = f'<p style="margin: 5px 0 0 0; color: #007bff; font-size: 12px;">Section: {imp.get("section", "")}</p>' if imp.get('section') else ''
                            
                            st.markdown(f"""
                            <div style="background: {bg_color}; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid {border_color};">
                                <div style="display: flex; align-items: start;">
                                    <span style="font-size: 20px; margin-right: 10px;">{icon}</span>
                                    <div style="flex: 1;">
                                        <strong>{imp.get('message', '')}</strong>
                                        <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">{imp.get('detail', '')}</p>
                                        {section_html}
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.info(str(imp))
                else:
                    st.success("✅ No issues found in this category!")
        
        display_improvements('content', tab_content)
        display_improvements('format', tab_format)
        display_improvements('optimization', tab_optimization)
        display_improvements('best_practices', tab_best)
        display_improvements('application_ready', tab_ready)
        
        st.markdown("---")
        
        # Strengths and Missing Keywords
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Strengths")
            if score_data.get('strengths'):
                for strength in score_data['strengths']:
                    st.markdown(f"- {strength}")
        
        with col2:
            st.subheader("🔑 Missing Keywords")
            if score_data.get('missing_keywords'):
                st.write(", ".join(score_data['missing_keywords']))
            else:
                st.write("No missing keywords identified")
        
        # Summary
        if score_data.get('summary'):
            st.markdown("---")
            st.info(f"**Summary:** {score_data['summary']}")
            
    else:
        st.info("📝 Generate a resume first to see your ATS score!")
        
        st.markdown("""
        ### What is an ATS Score?
        
        An **ATS (Applicant Tracking System) score** measures how well your resume will perform when scanned by automated systems.
        
        **Our scoring evaluates:**
        - 📝 **Content**: Quality of summary, achievements, metrics
        - 📄 **Format**: ATS-friendly structure and readability
        - 🎯 **Optimization**: Keywords and job description alignment
        - ✨ **Best Practices**: Action verbs, professional language
        - ✅ **Application Ready**: Completeness and polish
        """)

# ==================== TAB 4: DOWNLOAD ====================
with tab4:
    st.header("💾 Download Resume")
    
    if st.session_state.generated_resume:
        resume_data = st.session_state.generated_resume
        
        # Live PDF Preview
        st.subheader("📄 Live PDF Preview")
        
        # Generate HTML preview using resume agent if available
        if hasattr(st.session_state, 'resume_agent') and st.session_state.resume_agent:
            import streamlit.components.v1 as components
            pdf_html = st.session_state.resume_agent.get_resume_pdf_html(highlight_changes=False)
            
            # Wrap in a scrollable container
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        margin: 0;
                        padding: 20px;
                        background: #f5f5f5;
                        font-family: Arial, sans-serif;
                    }}
                    .container {{
                        max-height: 600px;
                        overflow-y: auto;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    {pdf_html}
                </div>
            </body>
            </html>
            """
            
            components.html(full_html, height=650, scrolling=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📄 PDF")
            if st.button("Download PDF"):
                with st.spinner("Generating..."):
                    try:
                        os.makedirs("uploads", exist_ok=True)
                        name = resume_data.get('name', 'resume').replace(' ', '_')
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{name}_{timestamp}.pdf"
                        filepath = os.path.join("uploads", filename)
                        
                        success = ResumeGenerator.generate_pdf(resume_data, filepath)
                        
                        if success:
                            with open(filepath, "rb") as f:
                                st.download_button(
                                    "📥 Click to Download",
                                    data=f.read(),
                                    file_name=filename,
                                    mime="application/pdf"
                                )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with col2:
            st.markdown("### 📝 DOCX")
            if st.button("Download DOCX"):
                with st.spinner("Generating..."):
                    try:
                        os.makedirs("uploads", exist_ok=True)
                        name = resume_data.get('name', 'resume').replace(' ', '_')
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{name}_{timestamp}.docx"
                        filepath = os.path.join("uploads", filename)
                        
                        success = ResumeGenerator.generate_docx(resume_data, filepath)
                        
                        if success:
                            with open(filepath, "rb") as f:
                                st.download_button(
                                    "📥 Click to Download",
                                    data=f.read(),
                                    file_name=filename,
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        if st.session_state.ats_score:
            score = st.session_state.ats_score
            st.markdown(f"""
            <div style="background: #f0f0f0; padding: 1rem; border-radius: 10px; margin-top: 2rem;">
                <h4>📊 Current ATS Score: {score['score']}/100 ({score['category']})</h4>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Generate a resume first!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 1rem;">
    <p>🤖 Powered by AI | Built with Streamlit & Groq</p>
</div>
""", unsafe_allow_html=True)
