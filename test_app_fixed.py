#!/usr/bin/env python3
"""
Test script to verify all Flask app functionality after date formatting fix
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api_endpoint():
    """Test the API endpoint"""
    print("🔍 Testing API endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/reviews")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API returned {len(data['reviews'])} reviews")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_reviews_page():
    """Test the reviews page loads without errors"""
    print("🔍 Testing reviews page...")
    try:
        response = requests.get(f"{BASE_URL}/reviews")
        if response.status_code == 200:
            if "error" not in response.text.lower() and "traceback" not in response.text.lower():
                print("✅ Reviews page loaded successfully without errors")
                return True
            else:
                print("❌ Reviews page contains error messages")
                return False
        else:
            print(f"❌ Reviews page returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Reviews page test failed: {e}")
        return False

def test_add_review_page():
    """Test the add review page loads"""
    print("🔍 Testing add review page...")
    try:
        response = requests.get(f"{BASE_URL}/addreview")
        if response.status_code == 200:
            print("✅ Add review page loaded successfully")
            return True
        else:
            print(f"❌ Add review page returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Add review page test failed: {e}")
        return False

def test_add_review_form():
    """Test submitting a new review"""
    print("🔍 Testing add review form submission...")
    try:
        data = {
            'school_name': 'Test School Auto',
            'reviewer_name': 'Automated Test',
            'rating': 5,
            'comment': 'This is an automated test review'
        }
        response = requests.post(f"{BASE_URL}/addreview", data=data, allow_redirects=False)
        if response.status_code == 302 or (response.status_code == 200 and "redirect" in response.text.lower()):
            print("✅ Review form submitted successfully")
            return True
        else:
            print(f"❌ Review form submission failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Review form test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Flask App Tests...")
    print("=" * 50)
    
    # Wait a moment for the server to be ready
    time.sleep(1)
    
    tests = [
        test_api_endpoint,
        test_reviews_page,
        test_add_review_page,
        test_add_review_form
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Flask app is working perfectly!")
    else:
        print("⚠️  Some tests failed. Please check the output above.")

if __name__ == "__main__":
    main()
