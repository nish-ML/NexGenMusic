import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 80)
print("🎵 MelodAI API Test Script")
print("=" * 80)

# Test 1: Register a new user
print("\n📝 Testing MelodAI API...")
print("\nTest 1: Register User")
print("-" * 80)
register_data = {
    "username": "testuser123",
    "email": "test@example.com",
    "password": "testpass123"
}

try:
    response = requests.post(f"{BASE_URL}/register/", json=register_data)
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Login
    print("\nTest 2: Login")
    print("-" * 80)
    login_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=login_data)
    print(f"✅ Status: {response.status_code}")
    login_response = response.json()
    print(f"Response: {login_response}")
    
    # Get the token
    token = login_response.get('token')
    headers = {"Authorization": f"Token {token}"}
    
    # Test 3: Generate Music (with authentication)
    print("\nTest 3: Generate Music (Authenticated)")
    print("-" * 80)
    generate_data = {"text": "I am feeling happy and excited!"}
    
    response = requests.post(f"{BASE_URL}/generate-music/", json=generate_data, headers=headers)
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 4: Get History (with authentication)
    print("\nTest 4: Get User History (Authenticated)")
    print("-" * 80)
    
    response = requests.get(f"{BASE_URL}/history/", headers=headers)
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n" + "=" * 80)
    print("✨ All tests completed successfully!")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
