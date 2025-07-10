#!/usr/bin/env python3
"""
Test script to verify the review submission works
"""

import requests
import json

def test_form_submission():
    """Test form submission to the Flask app"""
    try:
        # Test data
        form_data = {
            'school_name': 'Test School from Script',
            'reviewer_name': 'Test User',
            'rating': '4',
            'comment': 'This is a test review submitted via script to check if form submission works.'
        }
        
        # Submit the form
        response = requests.post('http://localhost:5000/addreview', data=form_data)
        
        if response.status_code == 200:
            print("✅ Form submission successful!")
            print(f"Response status: {response.status_code}")
            
            # Check if we got redirected to reviews page
            if 'reviews' in response.url:
                print("✅ Redirected to reviews page successfully")
            else:
                print("⚠️  Form processed but no redirect")
                
        else:
            print(f"❌ Form submission failed with status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error testing form submission: {e}")

def test_api_endpoint():
    """Test the API endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/reviews')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API endpoint working - {len(data['reviews'])} reviews found")
        else:
            print(f"❌ API endpoint failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing API endpoint: {e}")

if __name__ == "__main__":
    print("🧪 Testing Flask App Form Submission")
    print("=" * 40)
    
    print("\n1. Testing API endpoint...")
    test_api_endpoint()
    
    print("\n2. Testing form submission...")
    test_form_submission()
    
    print("\n3. Testing API endpoint again...")
    test_api_endpoint()
