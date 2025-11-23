import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

def get_spotify_client():
    """Initialize and return Spotify client using client credentials."""
    client_credentials_manager = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_tracks(query, limit=10, market=None):
    """Search for tracks on Spotify based on a query."""
    sp = get_spotify_client()
    search_params = {'q': query, 'type': 'track', 'limit': limit}
    if market:
        search_params['market'] = market
    results = sp.search(**search_params)
    tracks = []
    for item in results['tracks']['items']:
        # Get artist names properly
        artists = [artist['name'] for artist in item['artists']]
        tracks.append({
            'id': item['id'],
            'name': item['name'],
            'artists': artists,  # Keep as list for proper display
            'album': item['album']['name'],
            'preview_url': item['preview_url'],
            'external_url': item['external_urls']['spotify'],
            'image_url': item['album']['images'][0]['url'] if item['album']['images'] else None
        })
    return tracks

def get_recommendations(seed_genres=None, seed_artists=None, seed_tracks=None, limit=10, market=None, **kwargs):
    """Get track recommendations from Spotify based on seeds."""
    sp = get_spotify_client()
    try:
        # Filter out None values and ensure we have valid seeds
        valid_seeds = {}
        if seed_genres and len(seed_genres) > 0:
            # Ensure seed_genres is a list
            if isinstance(seed_genres, str):
                seed_genres = [seed_genres]
            valid_seeds['seed_genres'] = seed_genres
        if seed_artists and len(seed_artists) > 0:
            valid_seeds['seed_artists'] = seed_artists
        if seed_tracks and len(seed_tracks) > 0:
            valid_seeds['seed_tracks'] = seed_tracks

        if not valid_seeds:
            # If no valid seeds, use popular tracks as fallback
            return search_tracks('popular', limit, market=market)

        # Add market parameter if provided
        if market:
            kwargs['market'] = market

        recommendations = sp.recommendations(
            limit=limit,
            **valid_seeds,
            **kwargs
        )
        tracks = []
        for track in recommendations['tracks']:
            tracks.append({
                'id': track['id'],
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'preview_url': track['preview_url'],
                'external_url': track['external_urls']['spotify'],
                'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
            })
        return tracks
    except Exception as e:
        # Fallback: return some popular tracks if recommendations fail
        print(f"Error getting recommendations: {e}")
        return search_tracks('popular', limit, market=market)

def get_genres():
    """Get available genres for recommendations."""
    sp = get_spotify_client()
    try:
        genres = sp.recommendation_genre_seeds()
        return genres['genres']
    except Exception as e:
        # Fallback to common genres if API fails - include Indian genres
        return ['pop', 'rock', 'hip-hop', 'jazz', 'classical', 'electronic', 'country', 'r-b', 'indie', 'ambient', 'bollywood', 'indian classical', 'indian indie', 'indian rock']
