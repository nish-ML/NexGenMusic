// Mock data for testing without backend

export const mockSpotifyTracks = [
  {
    id: '1',
    title: 'Midnight Dreams',
    artist: 'Luna Wave',
    album: 'Nocturnal',
    albumArt: 'https://via.placeholder.com/300/4f46e5/ffffff?text=Midnight+Dreams',
    spotifyUrl: 'https://open.spotify.com/track/example1'
  },
  {
    id: '2',
    title: 'Electric Pulse',
    artist: 'Neon Riders',
    album: 'Synthwave',
    albumArt: 'https://via.placeholder.com/300/8b5cf6/ffffff?text=Electric+Pulse',
    spotifyUrl: 'https://open.spotify.com/track/example2'
  },
  {
    id: '3',
    title: 'Ocean Breeze',
    artist: 'Coastal Vibes',
    album: 'Summer Days',
    albumArt: 'https://via.placeholder.com/300/14b8a6/ffffff?text=Ocean+Breeze',
    spotifyUrl: 'https://open.spotify.com/track/example3'
  },
  {
    id: '4',
    title: 'Urban Nights',
    artist: 'City Lights',
    album: 'Metropolitan',
    albumArt: 'https://via.placeholder.com/300/f97316/ffffff?text=Urban+Nights',
    spotifyUrl: 'https://open.spotify.com/track/example4'
  },
  {
    id: '5',
    title: 'Starlight Symphony',
    artist: 'Cosmic Orchestra',
    album: 'Celestial',
    albumArt: 'https://via.placeholder.com/300/ec4899/ffffff?text=Starlight',
    spotifyUrl: 'https://open.spotify.com/track/example5'
  },
  {
    id: '6',
    title: 'Desert Wind',
    artist: 'Sahara Sounds',
    album: 'Dunes',
    albumArt: 'https://via.placeholder.com/300/fbbf24/ffffff?text=Desert+Wind',
    spotifyUrl: 'https://open.spotify.com/track/example6'
  },
]

export const mockGeneratedTrack = {
  title: 'AI Generated Track',
  mood: 'happy',
  tempo: 120,
  genre: 'electronic',
  duration: 30,
  timestamp: new Date().toISOString(),
}
