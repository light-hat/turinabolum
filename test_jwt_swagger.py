#!/usr/bin/env python3
"""
Test script to verify JWT authentication integration with Swagger.
This script tests the authentication endpoints and verifies they work properly.
"""

import requests
import json
import sys
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"
SWAGGER_URL = f"{BASE_URL}/api/docs/"

def test_swagger_access():
    """Test that Swagger UI is accessible."""
    print("Testing Swagger UI access...")
    try:
        response = requests.get(SWAGGER_URL)
        if response.status_code == 200:
            print("✅ Swagger UI is accessible")
            return True
        else:
            print(f"❌ Swagger UI returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to access Swagger UI: {e}")
        return False

def test_auth_endpoints():
    """Test authentication endpoints."""
    print("\nTesting authentication endpoints...")
    
    # Test JWT create endpoint
    print("Testing JWT create endpoint...")
    auth_data = {
        "username": "admin",  # You may need to create this user first
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/jwt/create/",
            json=auth_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "access" in data:
                print("✅ JWT create endpoint works")
                access_token = data["access"]
                return access_token
            else:
                print(f"❌ JWT create failed: {data}")
                return None
        else:
            print(f"❌ JWT create returned status {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to test JWT create: {e}")
        return None

def test_protected_endpoint(access_token):
    """Test a protected endpoint with JWT token."""
    print("\nTesting protected endpoint with JWT...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test incidents endpoint (should be protected)
        response = requests.get(f"{API_BASE}/incidents/", headers=headers)
        
        if response.status_code == 200:
            print("✅ Protected endpoint accessible with JWT")
            return True
        elif response.status_code == 401:
            print("❌ Protected endpoint returned 401 (unauthorized)")
            return False
        else:
            print(f"❌ Protected endpoint returned status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to test protected endpoint: {e}")
        return False

def test_swagger_auth_integration():
    """Test that Swagger UI shows authentication options."""
    print("\nTesting Swagger authentication integration...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/schema/")
        if response.status_code == 200:
            schema = response.json()
            
            # Check if security definitions are present
            if "components" in schema and "securitySchemes" in schema["components"]:
                security_schemes = schema["components"]["securitySchemes"]
                if "Bearer" in security_schemes:
                    print("✅ JWT Bearer authentication is defined in OpenAPI schema")
                    return True
                else:
                    print("❌ JWT Bearer authentication not found in schema")
                    return False
            else:
                print("❌ Security schemes not found in OpenAPI schema")
                return False
        else:
            print(f"❌ Failed to get OpenAPI schema: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to test schema: {e}")
        return False

def main():
    """Main test function."""
    print("🔍 Testing JWT Authentication Integration with Swagger")
    print("=" * 60)
    
    # Test 1: Swagger UI access
    if not test_swagger_access():
        print("\n❌ Swagger UI test failed. Make sure the server is running.")
        sys.exit(1)
    
    # Test 2: OpenAPI schema with security definitions
    if not test_swagger_auth_integration():
        print("\n❌ OpenAPI schema test failed.")
        sys.exit(1)
    
    # Test 3: Authentication endpoints
    access_token = test_auth_endpoints()
    if not access_token:
        print("\n⚠️  Authentication test failed. You may need to create a user first.")
        print("   Try: python manage.py createsuperuser")
        return
    
    # Test 4: Protected endpoints
    if not test_protected_endpoint(access_token):
        print("\n❌ Protected endpoint test failed.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! JWT authentication is properly integrated with Swagger.")
    print(f"\n📖 You can now test the API at: {SWAGGER_URL}")
    print("   - Click 'Authorize' button in Swagger UI")
    print("   - Enter your JWT token in the format: Bearer <your_token>")
    print("   - Test protected endpoints directly from the UI")

if __name__ == "__main__":
    main()
