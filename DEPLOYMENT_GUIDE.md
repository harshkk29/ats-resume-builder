# 🚀 GitHub Deployment Guide

## Step-by-Step Instructions to Deploy on GitHub

### 1️⃣ Initialize Git Repository

```bash
cd "/Users/harshvardhankhot/INTERNSHIP AI bot/ATS_Modified_Final"
git init
```

### 2️⃣ Add All Files

```bash
git add .
```

### 3️⃣ Create Initial Commit

```bash
git commit -m "Initial commit: AI-Powered ATS Resume Builder with all features"
```

### 4️⃣ Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the **"+"** icon in the top right
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name:** `ats-resume-builder` (or your preferred name)
   - **Description:** "AI-Powered ATS Resume Builder with live preview, scoring, and templates"
   - **Visibility:** Public or Private (your choice)
   - **DO NOT** initialize with README (we already have one)
5. Click **"Create repository"**

### 5️⃣ Connect Local Repository to GitHub

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/ats-resume-builder.git
git branch -M main
git push -u origin main
```

### 6️⃣ Verify Upload

Go to your GitHub repository URL:
```
https://github.com/YOUR_USERNAME/ats-resume-builder
```

You should see all your files!

---

## 🌐 Deploy to Streamlit Cloud (FREE!)

### Prerequisites
- GitHub repository (completed above)
- Groq API key

### Steps

1. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Sign in with GitHub

2. **Deploy New App**
   - Click **"New app"**
   - Select your repository: `YOUR_USERNAME/ats-resume-builder`
   - Main file path: `AST.py`
   - Click **"Advanced settings"**

3. **Add Secrets**
   In the Secrets section, add:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   ```

4. **Deploy!**
   - Click **"Deploy!"**
   - Wait 2-3 minutes for deployment
   - Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

---

## 📝 Update Your Repository Later

When you make changes:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Description of your changes"

# Push to GitHub
git push origin main
```

Streamlit Cloud will automatically redeploy when you push!

---

## 🔐 Security Notes

### ✅ DO:
- Keep your `.env` file local (it's in `.gitignore`)
- Use Streamlit Cloud Secrets for API keys
- Never commit API keys to GitHub

### ❌ DON'T:
- Don't remove `.env` from `.gitignore`
- Don't hardcode API keys in code
- Don't share your `.env` file

---

## 🎯 Quick Commands Reference

```bash
# Initialize repository
git init

# Add all files
git add .

# Commit
git commit -m "Your message"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git push -u origin main

# Check status
git status

# View commit history
git log --oneline

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

## 🆘 Troubleshooting

### Problem: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### Problem: Authentication failed
Use Personal Access Token instead of password:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

### Problem: Large files error
```bash
# Remove large files from tracking
git rm --cached large_file.pdf
echo "*.pdf" >> .gitignore
git commit -m "Remove large files"
```

---

## 📊 Repository Features to Enable

After pushing to GitHub:

1. **Add Topics** (for discoverability)
   - streamlit
   - ai
   - resume-builder
   - ats
   - groq
   - python

2. **Enable Issues** (for bug reports)

3. **Add Description** (shown on repo page)

4. **Create Releases** (version your app)

---

## 🎉 You're Done!

Your project is now:
- ✅ On GitHub
- ✅ Version controlled
- ✅ Ready to deploy to Streamlit Cloud
- ✅ Shareable with others

**Share your app URL with the world!** 🌍
