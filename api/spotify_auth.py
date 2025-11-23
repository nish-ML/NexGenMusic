import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8000/api/spotify-callback/")

def get_spotify_auth_url():
    """Generate Spotify authorization URL"""
    params = {
        'client_id': SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'scope': 'user-read-email user-read-private',
    }
    return f"https://accounts.spotify.com/authorize?{urlencode(params)}"

def get_spotify_token(code):
    """Exchange authorization code for access token"""
    token_url = "https://accounts.spotify.com/api/token"
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }
    
    response = requests.post(token_url, data=data)
    return response.json()

def get_spotify_user_info(access_token):
    """Get Spotify user information"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    return response.json()
