import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://127.0.0.1:8000/api/google-callback/")

def get_google_auth_url():
    """Generate Google authorization URL"""
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'consent',
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

def get_google_token(code):
    """Exchange authorization code for access token"""
    token_url = "https://oauth2.googleapis.com/token"
    
    data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    
    response = requests.post(token_url, data=data)
    return response.json()

def get_google_user_info(access_token):
    """Get Google user information"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
    return response.json()
