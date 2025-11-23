import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    raise Exception("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env")

auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = Spotify(auth_manager=auth_manager, requests_timeout=10, retries=3)

def get_song_by_mood_genre_language(mood, genre, language=None):
    """
    Search Spotify for track that matches mood+genre+language.
    Returns (external_url, song_name, artist_name) or (None, None, None)
    """
    # Build query
    q_parts = []
    if mood:
        q_parts.append(mood)
    if genre:
        q_parts.append(genre)
    if language:
        q_parts.append(language)
    query = " ".join(q_parts).strip()

    # Use Spotify search
    results = sp.search(q=query, limit=5, type='track')
    items = results.get('tracks', {}).get('items', [])
    if not items:
        return None, None, None

    # Try to pick a track that has preview_url or just first available
    track = None
    for it in items:
        # prefer tracks with preview_url (short sample) or popularity
        track = it
        break

    if not track:
        return None, None, None

    external_url = track.get('external_urls', {}).get('spotify')
    song_name = track.get('name')
    artist_name = ", ".join([a['name'] for a in track.get('artists', [])]) if track.get('artists') else None
    return external_url, song_name, artist_name

def get_playlist_by_mood_genre_language(mood, genre, language=None, limit=10):
    """
    Generate a playlist of tracks matching mood+genre+language.
    Returns list of track dictionaries with details
    """
    # Build search query
    q_parts = []
    if mood:
        q_parts.append(mood)
    if genre:
        q_parts.append(genre)
    if language:
        q_parts.append(language)
    query = " ".join(q_parts).strip()

    # Search for tracks
    results = sp.search(q=query, limit=limit, type='track')
    items = results.get('tracks', {}).get('items', [])
    
    if not items:
        return []

    # Build playlist with track details
    playlist = []
    for track in items:
        track_data = {
            'spotify_url': track.get('external_urls', {}).get('spotify'),
            'track_id': track.get('id'),
            'song_name': track.get('name'),
            'artist_name': ", ".join([a['name'] for a in track.get('artists', [])]) if track.get('artists') else 'Unknown',
            'album_name': track.get('album', {}).get('name'),
            'album_image': track.get('album', {}).get('images', [{}])[0].get('url') if track.get('album', {}).get('images') else None,
            'preview_url': track.get('preview_url'),
            'duration_ms': track.get('duration_ms'),
            'popularity': track.get('popularity', 0)
        }
        playlist.append(track_data)
    
    # Sort by popularity
    playlist.sort(key=lambda x: x['popularity'], reverse=True)
    
    return playlist

def get_recommendations_by_mood(mood, genre=None, limit=10):
    """
    Get Spotify recommendations based on mood and genre using audio features
    """
    # Map moods to audio features
    mood_features = {
        'happy': {'valence': 0.8, 'energy': 0.7, 'danceability': 0.7},
        'sad': {'valence': 0.2, 'energy': 0.3, 'acousticness': 0.6},
        'energetic': {'energy': 0.9, 'danceability': 0.8, 'tempo': 140},
        'calm': {'valence': 0.5, 'energy': 0.3, 'acousticness': 0.7},
        'romantic': {'valence': 0.6, 'energy': 0.4, 'acousticness': 0.5},
        'angry': {'energy': 0.9, 'valence': 0.3, 'loudness': -5},
        'anxious': {'energy': 0.6, 'valence': 0.3},
        'nostalgic': {'valence': 0.5, 'acousticness': 0.6}
    }
    
    # Get seed tracks based on mood and genre
    search_query = f"{mood} {genre}" if genre else mood
    seed_results = sp.search(q=search_query, limit=5, type='track')
    seed_tracks = [track['id'] for track in seed_results.get('tracks', {}).get('items', [])[:5]]
    
    if not seed_tracks:
        return []
    
    # Get audio features for the mood
    target_features = mood_features.get(mood.lower(), {})
    
    try:
        # Get recommendations
        recommendations = sp.recommendations(
            seed_tracks=seed_tracks[:5],
            limit=limit,
            **{f'target_{k}': v for k, v in target_features.items()}
        )
        
        # Format recommendations
        playlist = []
        for track in recommendations.get('tracks', []):
            track_data = {
                'spotify_url': track.get('external_urls', {}).get('spotify'),
                'track_id': track.get('id'),
                'song_name': track.get('name'),
                'artist_name': ", ".join([a['name'] for a in track.get('artists', [])]) if track.get('artists') else 'Unknown',
                'album_name': track.get('album', {}).get('name'),
                'album_image': track.get('album', {}).get('images', [{}])[0].get('url') if track.get('album', {}).get('images') else None,
                'preview_url': track.get('preview_url'),
                'duration_ms': track.get('duration_ms'),
                'popularity': track.get('popularity', 0)
            }
            playlist.append(track_data)
        
        return playlist
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        # Fallback to regular search
        return get_playlist_by_mood_genre_language(mood, genre, None, limit)
