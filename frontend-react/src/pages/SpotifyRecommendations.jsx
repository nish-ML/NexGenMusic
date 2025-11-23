import { useState, useEffect } from 'react'
import { Search, Play, ExternalLink } from 'lucide-react'
import Card from '../components/UI/Card'
import Input from '../components/UI/Input'
import LoadingSkeleton from '../components/UI/LoadingSkeleton'
import { motion } from 'framer-motion'

const SPOTIFY_API_URL = import.meta.env.VITE_SPOTIFY_PROXY_URL

const SpotifyRecommendations = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [songs, setSongs] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [page, setPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)

  useEffect(() => {
    fetchRecommendations()
  }, [])

  const fetchRecommendations = async (query = '', pageNum = 1) => {
    setLoading(true)
    setError(null)
    
    try {
      // Placeholder API call - replace with actual endpoint
      const response = await fetch(`${SPOTIFY_API_URL}/recommendations?q=${query}&page=${pageNum}`)
      
      if (!response.ok) throw new Error('Failed to fetch recommendations')
      
      const data = await response.json()
      
      if (pageNum === 1) {
        setSongs(data.tracks || [])
      } else {
        setSongs(prev => [...prev, ...(data.tracks || [])])
      }
      
      setHasMore(data.hasMore || false)
    } catch (err) {
      setError(err.message)
      // Mock data for demo
      setSongs([
        {
          id: '1',
          title: 'Midnight Dreams',
          artist: 'Luna Wave',
          album: 'Nocturnal',
          albumArt: 'https://via.placeholder.com/300',
          spotifyUrl: 'https://open.spotify.com/track/example1'
        },
        {
          id: '2',
          title: 'Electric Pulse',
          artist: 'Neon Riders',
          album: 'Synthwave',
          albumArt: 'https://via.placeholder.com/300',
          spotifyUrl: 'https://open.spotify.com/track/example2'
        },
        {
          id: '3',
          title: 'Ocean Breeze',
          artist: 'Coastal Vibes',
          album: 'Summer Days',
          albumArt: 'https://via.placeholder.com/300',
          spotifyUrl: 'https://open.spotify.com/track/example3'
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    setPage(1)
    fetchRecommendations(searchQuery, 1)
  }

  const loadMore = () => {
    const nextPage = page + 1
    setPage(nextPage)
    fetchRecommendations(searchQuery, nextPage)
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gradient mb-2">Spotify Recommendations</h1>
        <p className="text-gray-600 dark:text-gray-400">Discover your next favorite track</p>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="mb-8">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for songs, artists, or albums..."
            className="pl-12"
          />
        </div>
      </form>

      {/* Error State */}
      {error && (
        <div className="mb-6 p-4 bg-red-100 dark:bg-red-900/20 border border-red-300 dark:border-red-800 rounded-xl text-red-700 dark:text-red-400">
          {error}
        </div>
      )}

      {/* Loading Skeletons */}
      {loading && page === 1 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <LoadingSkeleton count={6} className="h-80" />
        </div>
      )}

      {/* Songs Grid */}
      {!loading || page > 1 ? (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {songs.map((song, index) => (
              <motion.div
                key={song.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <Card hoverTilt className="group overflow-hidden">
                  {/* Album Art */}
                  <div className="relative mb-4 overflow-hidden rounded-xl">
                    <img
                      src={song.albumArt}
                      alt={`${song.album} cover`}
                      className="w-full aspect-square object-cover group-hover:scale-110 transition-transform duration-300"
                    />
                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                      <Play className="w-12 h-12 text-white" />
                    </div>
                    <div className="absolute top-2 right-2 w-2 h-2 bg-green-500 rounded-full shadow-glow"></div>
                  </div>

                  {/* Song Info */}
                  <h3 className="font-bold text-lg text-gray-900 dark:text-white mb-1 truncate">
                    {song.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm mb-1 truncate">
                    {song.artist}
                  </p>
                  <p className="text-gray-500 dark:text-gray-500 text-xs mb-4 truncate">
                    {song.album}
                  </p>

                  {/* Play Button */}
                  <a
                    href={song.spotifyUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-center space-x-2 w-full py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:shadow-glow transition-all duration-200"
                  >
                    <ExternalLink className="w-4 h-4" />
                    <span className="font-medium">Play on Spotify</span>
                  </a>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Load More */}
          {hasMore && songs.length > 0 && (
            <div className="mt-8 flex justify-center">
              <button
                onClick={loadMore}
                disabled={loading}
                className="px-8 py-3 bg-gradient-to-r from-primary to-secondary text-white rounded-xl font-medium hover:shadow-glow transition-all duration-200 disabled:opacity-50"
              >
                {loading ? 'Loading...' : 'Load More'}
              </button>
            </div>
          )}

          {/* Empty State */}
          {songs.length === 0 && !loading && (
            <div className="text-center py-12">
              <p className="text-gray-500 dark:text-gray-400 text-lg">
                No recommendations found. Try a different search!
              </p>
            </div>
          )}
        </>
      ) : null}
    </div>
  )
}

export default SpotifyRecommendations
