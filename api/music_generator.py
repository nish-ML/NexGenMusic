"""
AI-Powered Music Generation System
Combines mood prediction with intelligent music selection
"""

import random
from .spotify_client import sp, get_playlist_by_mood_genre_language, get_recommendations_by_mood
from .ml_mood_predictor import get_mood_recommendations

class MusicGenerator:
    """
    Intelligent music generation based on mood and sentiment analysis
    """
    
    def __init__(self):
        self.spotify_client = sp
        
    def generate_playlist(self, mood, genre=None, language=None, intensity=0.5, limit=10):
        """
        Generate a curated playlist based on mood, genre, and emotion intensity
        
        Args:
            mood: Detected mood (happy, sad, energetic, etc.)
            genre: Optional genre preference
            language: Optional language preference
            intensity: Emotion intensity (0-1)
            limit: Number of tracks to return
            
        Returns:
            list: Curated playlist with track details
        """
        # Get mood-based recommendations
        mood_rec = get_mood_recommendations(mood, intensity)
        
        # Use provided genre or get recommended genres
        if not genre:
            genre = random.choice(mood_rec['genres'])
        
        # Get audio features for the mood
        audio_features = mood_rec['audio_features']
        
        # Try multiple strategies to get the best playlist
        playlist = []
        
        # Strategy 1: Use Spotify recommendations with audio features
        try:
            playlist = self._get_recommendations_with_features(
                mood, genre, audio_features, limit
            )
        except Exception as e:
            print(f"Recommendation strategy failed: {e}")
        
        # Strategy 2: Fallback to search-based playlist
        if not playlist or len(playlist) < limit:
            try:
                search_playlist = get_playlist_by_mood_genre_language(
                    mood, genre, language, limit
                )
                playlist.extend(search_playlist)
            except Exception as e:
                print(f"Search strategy failed: {e}")
        
        # Strategy 3: Get tracks from mood-specific playlists
        if not playlist or len(playlist) < limit:
            try:
                playlist_tracks = self._get_from_mood_playlists(mood, genre, limit)
                playlist.extend(playlist_tracks)
            except Exception as e:
                print(f"Playlist strategy failed: {e}")
        
        # Remove duplicates and limit
        playlist = self._deduplicate_playlist(playlist)[:limit]
        
        # Enhance playlist with audio analysis
        playlist = self._enhance_playlist_metadata(playlist, mood, intensity)
        
        return playlist
    
    def _get_recommendations_with_features(self, mood, genre, audio_features, limit):
        """
        Get recommendations using Spotify's recommendation API with audio features
        """
        # Search for seed tracks
        search_query = f"{mood} {genre}"
        seed_results = self.spotify_client.search(q=search_query, limit=5, type='track')
        seed_tracks = [track['id'] for track in seed_results.get('tracks', {}).get('items', [])[:5]]
        
        if not seed_tracks:
            return []
        
        # Get recommendations with audio features
        recommendations = self.spotify_client.recommendations(
            seed_tracks=seed_tracks[:5],
            limit=limit,
            **{f'target_{k}': v for k, v in audio_features.items()}
        )
        
        # Format tracks
        playlist = []
        for track in recommendations.get('tracks', []):
            track_data = self._format_track(track)
            playlist.append(track_data)
        
        return playlist
    
    def _get_from_mood_playlists(self, mood, genre, limit):
        """
        Get tracks from Spotify's curated mood playlists
        """
        # Search for mood-based playlists
        playlist_query = f"{mood} {genre} playlist"
        playlist_results = self.spotify_client.search(q=playlist_query, limit=3, type='playlist')
        
        tracks = []
        for playlist in playlist_results.get('playlists', {}).get('items', []):
            if len(tracks) >= limit:
                break
            
            try:
                # Get playlist tracks
                playlist_id = playlist['id']
                playlist_tracks = self.spotify_client.playlist_tracks(playlist_id, limit=limit)
                
                for item in playlist_tracks.get('items', []):
                    if len(tracks) >= limit:
                        break
                    
                    track = item.get('track')
                    if track:
                        track_data = self._format_track(track)
                        tracks.append(track_data)
            except Exception as e:
                print(f"Error getting playlist tracks: {e}")
                continue
        
        return tracks
    
    def _format_track(self, track):
        """
        Format track data into standardized structure
        """
        return {
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
    
    def _deduplicate_playlist(self, playlist):
        """
        Remove duplicate tracks from playlist
        """
        seen_ids = set()
        unique_playlist = []
        
        for track in playlist:
            track_id = track.get('track_id')
            if track_id and track_id not in seen_ids:
                seen_ids.add(track_id)
                unique_playlist.append(track)
        
        return unique_playlist
    
    def _enhance_playlist_metadata(self, playlist, mood, intensity):
        """
        Add mood-based metadata to playlist tracks
        """
        for track in playlist:
            track['mood'] = mood
            track['intensity'] = intensity
            track['match_score'] = self._calculate_match_score(track, mood, intensity)
        
        # Sort by match score
        playlist.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        
        return playlist
    
    def _calculate_match_score(self, track, mood, intensity):
        """
        Calculate how well a track matches the mood and intensity
        """
        # Base score from popularity
        score = track.get('popularity', 50) / 100.0
        
        # Adjust based on intensity
        score += intensity * 0.3
        
        # Bonus for having preview URL
        if track.get('preview_url'):
            score += 0.1
        
        # Bonus for having album image
        if track.get('album_image'):
            score += 0.05
        
        return min(score, 1.0)
    
    def get_single_track(self, mood, genre=None, language=None, intensity=0.5):
        """
        Get a single track (for backward compatibility)
        """
        playlist = self.generate_playlist(mood, genre, language, intensity, limit=1)
        
        if playlist:
            track = playlist[0]
            return track['spotify_url'], track['song_name'], track['artist_name']
        
        return None, None, None
    
    def generate_mood_mix(self, primary_mood, secondary_mood=None, limit=15):
        """
        Generate a mixed playlist with primary and secondary moods
        """
        primary_limit = limit * 2 // 3 if secondary_mood else limit
        secondary_limit = limit - primary_limit
        
        # Get primary mood tracks
        playlist = self.generate_playlist(primary_mood, limit=primary_limit)
        
        # Add secondary mood tracks if specified
        if secondary_mood:
            secondary_playlist = self.generate_playlist(secondary_mood, limit=secondary_limit)
            playlist.extend(secondary_playlist)
        
        # Shuffle for variety
        random.shuffle(playlist)
        
        return playlist[:limit]
    
    def generate_dynamic_playlist(self, text_analysis):
        """
        Generate playlist based on comprehensive text analysis
        
        Args:
            text_analysis: Dict with mood, sentiment_score, confidence, emotions
            
        Returns:
            list: Curated playlist
        """
        mood = text_analysis.get('mood', 'calm')
        confidence = text_analysis.get('confidence', 0.5)
        sentiment_score = text_analysis.get('sentiment_score', 0.0)
        
        # Determine intensity from confidence and sentiment
        intensity = (confidence + abs(sentiment_score)) / 2
        
        # Get mood recommendations
        mood_rec = get_mood_recommendations(mood, intensity)
        
        # Select genre based on mood
        genre = random.choice(mood_rec['genres'])
        
        # Generate playlist
        playlist = self.generate_playlist(mood, genre, None, intensity, limit=10)
        
        # Add analysis metadata
        for track in playlist:
            track['generated_from'] = {
                'mood': mood,
                'sentiment_score': sentiment_score,
                'confidence': confidence,
                'intensity': intensity
            }
        
        return playlist

# Global music generator instance
_music_generator = None

def get_music_generator():
    """
    Get or create music generator instance (singleton)
    """
    global _music_generator
    if _music_generator is None:
        _music_generator = MusicGenerator()
    return _music_generator
