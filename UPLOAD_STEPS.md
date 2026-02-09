# 🚀 UPLOAD TO GITHUB - SIMPLE STEPS

## Follow These Steps Exactly:

### **Step 1: Create Repository on GitHub** (2 minutes)

1. **Open your browser** and go to:
   ```
   https://github.com/new
   ```

2. **Log in** to your GitHub account if needed

3. **Fill in the form:**
   - Repository name: `ats-resume-builder`
   - Description: `AI-Powered ATS Resume Builder with live preview, scoring, and templates`
   - Choose: **Public** (or Private if you prefer)
   
4. **⚠️ IMPORTANT - Leave these UNCHECKED:**
   - ❌ Add a README file
   - ❌ Add .gitignore  
   - ❌ Choose a license
   
   (We already have these files!)

5. **Click the green "Create repository" button**

---

### **Step 2: Upload Your Code** (1 minute)

After creating the repository, you'll see a page with instructions.

**Option A: Use the automated script** (Easiest!)

Open Terminal and run:
```bash
cd "/Users/harshvardhankhot/INTERNSHIP AI bot/ATS_Modified_Final"
./upload_to_github.sh
```

Then enter your GitHub username when asked.

---

**Option B: Manual commands**

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
cd "/Users/harshvardhankhot/INTERNSHIP AI bot/ATS_Modified_Final"
git remote add origin https://github.com/YOUR_USERNAME/ats-resume-builder.git
git branch -M main
git push -u origin main
```

When asked for credentials:
- **Username:** Your GitHub username
- **Password:** Use a Personal Access Token (not your password)
  - Get token at: https://github.com/settings/tokens
  - Click "Generate new token (classic)"
  - Select `repo` scope
  - Copy and use as password

---

### **Step 3: Verify Upload** (30 seconds)

Go to:
```
https://github.com/YOUR_USERNAME/ats-resume-builder
```

You should see all your files! ✅

---

## 🎉 Done! What's Next?

### Deploy to Streamlit Cloud (FREE!)

1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select: `YOUR_USERNAME/ats-resume-builder`
5. Main file: `AST.py`
6. Click "Advanced settings" → "Secrets"
7. Add:
   ```toml
   GROQ_API_KEY = "your_actual_api_key_here"
   ```
8. Click "Deploy!"
9. Wait 2-3 minutes
10. Your app is LIVE! 🚀

---

## 🆘 Troubleshooting

### "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/ats-resume-builder.git
git push -u origin main
```

### "Authentication failed"
- Don't use your password
- Use a Personal Access Token instead
- Get it from: https://github.com/settings/tokens

### "Permission denied"
- Make sure you're logged into the correct GitHub account
- Check that you created the repository successfully

---

## 📞 Need Help?

1. Make sure you created the repository on GitHub first
2. Make sure you're in the correct directory
3. Make sure you replaced YOUR_USERNAME with your actual username
4. Check that you're using a Personal Access Token, not password

---

## ✅ Quick Checklist

- [ ] Created repository on GitHub
- [ ] Repository name is `ats-resume-builder`
- [ ] Did NOT check "Add README" or other options
- [ ] Ran the upload commands
- [ ] Entered GitHub username and token
- [ ] Verified files are on GitHub
- [ ] Ready to deploy to Streamlit Cloud!

---

**You're almost there! Just follow the steps above.** 🚀
