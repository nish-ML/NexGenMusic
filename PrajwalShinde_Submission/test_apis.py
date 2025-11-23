import requests

# Step 1: Login to get token
print("1. Logging in...")
login_response = requests.post(
    "http://127.0.0.1:8000/api/auth/login/",
    json={"username": "user1", "password": "Password123"}
)
token = login_response.json()['token']
print(f"✓ Got token: {token[:30]}...")

# Step 2: Generate music with token
print("\n2. Generating music...")
headers = {"Authorization": f"Token {token}"}
music_response = requests.post(
    "http://127.0.0.1:8000/api/generate-music/",
    json={"text": "I am feeling happy and excited"},
    headers=headers
)
print(f"✓ Status: {music_response.status_code}")
print(f"✓ Response: {music_response.json()}")

# Step 3: Get history
print("\n3. Getting history...")
history_response = requests.get(
    "http://127.0.0.1:8000/api/history/",
    headers=headers
)
print(f"✓ Status: {history_response.status_code}")
print(f"✓ History: {history_response.json()}")
