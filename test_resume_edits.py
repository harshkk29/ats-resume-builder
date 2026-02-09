"""
Test Script for Resume Agent Edits
This script verifies that the AI agent actually makes the requested changes to the resume
"""

import json
import sys
from utils.ai_helper import AIHelper
from utils.resume_agent import ResumeAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

def test_resume_edit(command: str, initial_resume: dict):
    """
    Test a single resume edit command
    
    Args:
        command: The edit command to test
        initial_resume: The initial resume state
    
    Returns:
        Tuple of (success, before_state, after_state, message)
    """
    print(f"\n{'='*80}")
    print(f"Testing Command: {command}")
    print(f"{'='*80}")
    
    # Initialize AI helper and agent
    ai_helper = AIHelper(GROQ_API_KEY)
    agent = ResumeAgent(ai_helper)
    agent.initialize_resume(initial_resume.copy())
    
    # Store before state
    before_state = agent.resume_state.copy()
    print(f"\n📋 Before State:")
    print(json.dumps(before_state, indent=2))
    
    # Process command
    try:
        response, pdf_html = agent.process_command(command)
        after_state = agent.resume_state.copy()
        
        print(f"\n✅ Response: {response}")
        print(f"\n📋 After State:")
        print(json.dumps(after_state, indent=2))
        
        # Check if anything changed
        if before_state == after_state:
            print(f"\n⚠️  WARNING: No changes detected!")
            return False, before_state, after_state, "No changes made"
        else:
            # Find what changed
            changes = []
            for key in before_state.keys():
                if before_state.get(key) != after_state.get(key):
                    changes.append(key)
            
            print(f"\n✅ Changes detected in sections: {', '.join(changes)}")
            return True, before_state, after_state, response
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False, before_state, before_state, str(e)

def run_all_tests():
    """Run a suite of tests"""
    
    # Sample resume
    sample_resume = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1-234-567-8900",
        "target_role": "Software Engineer",
        "professional_summary": "Experienced software engineer with 5 years of experience in web development.",
        "skills": ["Python", "JavaScript", "React", "Node.js"],
        "experience": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "duration": "2020-Present",
                "responsibilities": [
                    "Developed web applications",
                    "Collaborated with team members"
                ]
            }
        ],
        "education": [
            {
                "degree": "BS Computer Science",
                "institution": "University of Tech",
                "year": "2019"
            }
        ],
        "projects": [],
        "certifications": []
    }
    
    # Test cases
    test_cases = [
        "Add Docker to skills",
        "Make the professional summary shorter",
        "Add a certification: AWS Certified Developer",
        "Change phone number to +1-555-123-4567",
        "Add quantifiable metrics to the first experience"
    ]
    
    results = []
    
    print("\n" + "="*80)
    print("RESUME EDIT VALIDATION TEST SUITE")
    print("="*80)
    
    for i, command in enumerate(test_cases, 1):
        print(f"\n\nTest {i}/{len(test_cases)}")
        success, before, after, message = test_resume_edit(command, sample_resume)
        results.append({
            "test_number": i,
            "command": command,
            "success": success,
            "message": message
        })
    
    # Summary
    print("\n\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{status} - Test {result['test_number']}: {result['command']}")
    
    print(f"\n{'='*80}")
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"{'='*80}\n")
    
    return results

if __name__ == "__main__":
    run_all_tests()
