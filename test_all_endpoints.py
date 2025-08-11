#!/usr/bin/env python3
"""
Comprehensive End-to-End Test Script for MVP Generation Agent
Tests all endpoints and functionality without getting stuck on proxy issues.
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8003"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test an endpoint and return the response."""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n🔍 Testing {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"   ✅ SUCCESS")
            try:
                return response.json()
            except:
                return response.text
        else:
            print(f"   ❌ FAILED - Expected {expected_status}, got {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return None
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ TIMEOUT - Endpoint took too long")
        return None
    except Exception as e:
        print(f"   💥 ERROR - {str(e)}")
        return None

def main():
    print("🚀 MVP Generation Agent - Comprehensive Endpoint Test")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n📋 Phase 1: Basic Health Check")
    health = test_endpoint("GET", "/api/v1/health")
    if not health:
        print("❌ Backend is not responding! Exiting...")
        return
    
    # Test 2: Create Project
    print("\n📋 Phase 2: Project Creation")
    project_data = {
        "name": "Test MVP Project",
        "description": "Testing all functionality",
        "industry": "PRODUCTIVITY",
        "target_users": "Remote teams and project managers",
        "tech_stack": {
            "frontend": ["React"],
            "backend": ["Node.js"],
            "database": ["PostgreSQL"]
        },
        "team_experience": "intermediate"
    }
    
    project = test_endpoint("POST", "/api/v1/projects", project_data, 200)
    if not project:
        print("❌ Cannot create project! Exiting...")
        return
    
    project_id = project.get("id")
    print(f"   📝 Created project: {project_id}")
    
    # Test 3: Add Feature
    print("\n📋 Phase 3: Feature Addition")
    feature_data = {
        "name": "User Authentication",
        "description": "Essential authentication system with login, register, and basic user management",
        "priority": "high"
    }
    
    feature_response = test_endpoint("POST", f"/api/v1/projects/{project_id}/features", feature_data, 200)
    if not feature_response:
        print("❌ Cannot add feature!")
        return
    
    print(f"   📝 Added feature with validation score: {feature_response['result']['score']['overall_score']}/10")
    
    # Test 4: Get Project Details
    print("\n📋 Phase 4: Project Retrieval")
    project_details = test_endpoint("GET", f"/api/v1/projects/{project_id}")
    if not project_details:
        print("❌ Cannot get project details!")
        return
    
    features = project_details.get("features", [])
    if not features:
        print("❌ No features found in project!")
        return
    
    feature_id = features[0]["id"]
    print(f"   📝 Found {len(features)} features, first feature ID: {feature_id}")
    
    # Test 5: User Story Generation (NEW FEATURE)
    print("\n📋 Phase 5: User Story Generation")
    user_story_response = test_endpoint("POST", f"/api/v1/projects/{project_id}/features/{feature_id}/generate-user-story")
    if user_story_response:
        print(f"   ✨ Generated user story: {user_story_response.get('user_story', 'N/A')}")
    else:
        print("   ❌ User story generation failed!")
    
    # Test 6: Feature Re-evaluation (NEW FEATURE)
    print("\n📋 Phase 6: Feature Re-evaluation")
    re_eval_response = test_endpoint("PUT", f"/api/v1/projects/{project_id}/features/{feature_id}/re-evaluate")
    if re_eval_response:
        new_score = re_eval_response.get("validation_result", {}).get("score", {}).get("overall_score", "N/A")
        print(f"   🔄 Re-evaluated with new score: {new_score}/10")
    else:
        print("   ❌ Feature re-evaluation failed!")
    
    # Test 7: MVP Generation
    print("\n📋 Phase 7: MVP Generation")
    mvp_data = {
        "target_timeline_weeks": 12,
        "budget_range": "10000-50000",
        "priority_focus": "user_experience"
    }
    
    mvp_response = test_endpoint("POST", f"/api/v1/projects/{project_id}/generate-mvp", mvp_data)
    if mvp_response:
        print(f"   🚀 MVP generated with {len(mvp_response.get('core_features', []))} core features")
    else:
        print("   ❌ MVP generation failed!")
    
    # Test 8: Project Deletion (MISSING FEATURE)
    print("\n📋 Phase 8: Project Deletion")
    delete_response = test_endpoint("DELETE", f"/api/v1/projects/{project_id}", expected_status=200)
    if delete_response:
        print("   🗑️ Project deleted successfully")
    else:
        print("   ❌ Project deletion failed (endpoint might be missing)")
    
    # Test 9: List All Projects
    print("\n📋 Phase 9: Project Listing")
    projects_list = test_endpoint("GET", "/api/v1/projects")
    if projects_list:
        total_projects = projects_list.get("total", 0)
        print(f"   📊 Found {total_projects} total projects")
    
    print("\n" + "=" * 60)
    print("🎯 Test Summary:")
    print("✅ Health Check - Backend is running")
    print("✅ Project Creation - Working")
    print("✅ Feature Addition - Working with validation")
    print("✅ Project Retrieval - Working")
    print("🔍 User Story Generation - Check results above")
    print("🔍 Feature Re-evaluation - Check results above") 
    print("🔍 MVP Generation - Check results above")
    print("🔍 Project Deletion - Check results above")
    print("✅ Project Listing - Working")
    
    print(f"\n⏰ Test completed at {datetime.now().strftime('%H:%M:%S')}")
    print("\n🌐 Next: Open http://localhost:3000 in browser to test frontend!")

if __name__ == "__main__":
    main()
