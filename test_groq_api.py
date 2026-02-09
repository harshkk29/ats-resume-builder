#!/usr/bin/env python3
"""
Test Groq API Key Validity
Run this to verify your API key works before using the ATS app
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("=" * 70)
print("🔍 Testing Groq API Key")
print("=" * 70)
print("")

# Get API key
api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    print("❌ ERROR: No GROQ_API_KEY found!")
    print("")
    print("📝 How to fix:")
    print("   1. Create a .env file in this folder")
    print("   2. Add: GROQ_API_KEY=gsk_your_key_here")
    print("   3. Get key from: https://console.groq.com/keys")
    sys.exit(1)

print(f"✓ API Key Found: {api_key[:15]}...{api_key[-5:]}")
print("")

# Test the API
print("Testing API connection...")
try:
    from groq import Groq
    
    client = Groq(api_key=api_key)
    
    print("  Sending test request...")
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": "Say 'SUCCESS' exactly once, nothing else."
            }
        ],
        max_tokens=5,
        temperature=0.1
    )
    
    result = response.choices[0].message.content.strip()
    
    print("")
    print("=" * 70)
    print("✅ SUCCESS! Your API Key Works!")
    print("=" * 70)
    print(f"API Response: {result}")
    print("")
    print("✨ You can now run the ATS app without 403 errors!")
    print("")
    print("Start the app with:")
    print("   streamlit run ATS.py")
    
except Exception as e:
    error_msg = str(e)
    
    print("")
    print("=" * 70)
    print("❌ API Test Failed")
    print("=" * 70)
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {error_msg}")
    print("")
    
    if "403" in error_msg or "Forbidden" in error_msg:
        print("🔴 Issue: Invalid or Expired API Key")
        print("")
        print("Solutions:")
        print("  1. Get a new key: https://console.groq.com/keys")
        print("  2. Check your key doesn't have extra spaces/quotes")
        print("  3. Verify the key starts with 'gsk_'")
        print("  4. Check your Groq account is active")
    
    elif "401" in error_msg or "Unauthorized" in error_msg:
        print("🔴 Issue: Authentication Failed")
        print("  Solution: Verify your API key is correct (starts with gsk_)")
    
    elif "429" in error_msg or "rate" in error_msg.lower():
        print("⚠️  Issue: Rate Limit Exceeded")
        print("  Solution: Wait a few minutes before trying again")
    
    elif "timeout" in error_msg.lower() or "connection" in error_msg.lower():
        print("⚠️  Issue: Network Connection Problem")
        print("  Solution: Check your internet connection")
    
    elif "ModuleNotFoundError" in error_msg:
        print("🔴 Issue: Missing 'groq' module")
        print("  Solution: pip install groq")
    
    else:
        print(f"❓ Unknown error. Try these steps:")
        print("  1. Verify .env file exists")
        print("  2. Check API key format (should start with gsk_)")
        print("  3. Try a different API key")
        print("  4. Check internet connection")
    
    sys.exit(1)
