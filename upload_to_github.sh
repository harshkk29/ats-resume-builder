#!/bin/bash

# GitHub Upload Script for ATS Resume Builder
# Run this after creating your repository on GitHub

echo "🚀 Uploading ATS Resume Builder to GitHub..."
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

# Confirm repository name
echo ""
echo "Repository name will be: ats-resume-builder"
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Navigate to project directory
cd "/Users/harshvardhankhot/INTERNSHIP AI bot/ATS_Modified_Final"

# Add remote (replace YOUR_USERNAME with actual username)
echo ""
echo "Adding GitHub remote..."
git remote add origin "https://github.com/$GITHUB_USERNAME/ats-resume-builder.git"

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Done! Your code is now on GitHub!"
echo "🌐 View at: https://github.com/$GITHUB_USERNAME/ats-resume-builder"
echo ""
echo "Next steps:"
echo "1. Go to https://share.streamlit.io to deploy"
echo "2. Connect your GitHub repository"
echo "3. Add GROQ_API_KEY to Secrets"
echo "4. Deploy!"
