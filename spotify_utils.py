import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ----------------------
# Fetch Spotify tracks based on mood, song type, and language
# ----------------------
def get_spotify_tracks(mood, song_type, language, limit=5):
    client_id = "4b08a255a9564e9bb3144ffcd1d79a4f"
    client_secret = "e3e7c02b7dc84646aba960e9a3baf210"

    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        ))

        # Build query string like "Telugu Happy Romantic songs"
        query = f"{language} {mood} {song_type} songs"
        print(f"🔍 Spotify Query: {query}")

        results = sp.search(q=query, type='track', limit=limit)
        tracks = []

        for item in results['tracks']['items']:
            track_info = {
                "name": item['name'],
                "artist": item['artists'][0]['name'],
                "url": item['external_urls']['spotify'],
                "id": item['id']  # Useful for embedding Spotify player
            }
            tracks.append(track_info)

        return tracks

    except Exception as e:
        print(f"⚠️ Spotify API Error: {e}")
        return []
