import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Music, Sparkles, History, TrendingUp, Clock, Headphones } from 'lucide-react'
import Card from '../components/UI/Card'
import Button from '../components/UI/Button'
import LoadingSkeleton from '../components/UI/LoadingSkeleton'
import { getHistory } from '../utils/historyStorage'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalGenerated: 0,
    recentGenerations: [],
    favoriteGenre: 'Unknown',
    totalListeningTime: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Load user stats from history
    const history = getHistory()
    const totalGenerated = history.length
    const recentGenerations = history.slice(0, 3)
    
    // Calculate favorite genre (mock for now)
    const genres = history.map(item => item.genre || 'Unknown')
    const genreCounts = genres.reduce((acc, genre) => {
      acc[genre] = (acc[genre] || 0) + 1
      return acc
    }, {})
    const favoriteGenre = Object.keys(genreCounts).length > 0 
      ? Object.keys(genreCounts).reduce((a, b) => genreCounts[a] > genreCounts[b] ? a : b)
      : 'Unknown'

    setStats({
      totalGenerated,
      recentGenerations,
      favoriteGenre,
      totalListeningTime: totalGenerated * 2.5 // Mock: ~2.5 min per track
    })
    
    setLoading(false)
  }, [])

  const quickActions = [
    {
      title: 'AI Music Generator',
      description: 'Create music from your mood',
      icon: Sparkles,
      link: '/ai-generator',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      title: 'Spotify Recommendations',
      description: 'Get personalized suggestions',
      icon: Music,
      link: '/spotify-recommendations',
      gradient: 'from-green-500 to-emerald-500'
    },
    {
      title: 'Generation History',
      description: 'View your past creations',
      icon: History,
      link: '/history',
      gradient: 'from-blue-500 to-cyan-500'
    }
  ]

  const statCards = [
    {
      label: 'Total Generated',
      value: stats.totalGenerated,
      icon: Music,
      color: 'text-purple-500'
    },
    {
      label: 'Favorite Genre',
      value: stats.favoriteGenre,
      icon: TrendingUp,
      color: 'text-green-500'
    },
    {
      label: 'Listening Time',
      value: `${Math.round(stats.totalListeningTime)} min`,
      icon: Clock,
      color: 'text-blue-500'
    }
  ]

  if (loading) {
    return (
      <div className="space-y-6">
        <LoadingSkeleton className="h-32" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <LoadingSkeleton className="h-40" />
          <LoadingSkeleton className="h-40" />
          <LoadingSkeleton className="h-40" />
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary via-secondary to-accent p-8 text-white">
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-2">Welcome to NexGen Music</h1>
          <p className="text-lg opacity-90">Create, discover, and enjoy AI-powered music</p>
        </div>
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/10 rounded-full blur-3xl" />
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <Card key={index} className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-900 dark:text-white">{stat.value}</p>
                </div>
                <div className={`p-3 rounded-xl bg-gray-100 dark:bg-gray-800 ${stat.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
              </div>
            </Card>
          )
        })}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action, index) => {
            const Icon = action.icon
            return (
              <Link key={index} to={action.link}>
                <Card className="p-6 hover:shadow-xl transition-all duration-300 group cursor-pointer h-full">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${action.gradient} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {action.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">
                    {action.description}
                  </p>
                </Card>
              </Link>
            )
          })}
        </div>
      </div>

      {/* Recent Generations */}
      {stats.recentGenerations.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Recent Generations</h2>
            <Link to="/history">
              <Button variant="ghost" size="sm">View All</Button>
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {stats.recentGenerations.map((item, index) => (
              <Card key={index} className="p-6">
                <div className="flex items-start space-x-4">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-primary to-secondary">
                    <Headphones className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-gray-900 dark:text-white truncate">
                      {item.mood || 'Generated Track'}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {new Date(item.timestamp).toLocaleDateString()}
                    </p>
                    {item.genre && (
                      <span className="inline-block mt-2 px-2 py-1 text-xs rounded-full bg-primary/10 text-primary">
                        {item.genre}
                      </span>
                    )}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {stats.totalGenerated === 0 && (
        <Card className="p-12 text-center">
          <div className="max-w-md mx-auto">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center mx-auto mb-4">
              <Music className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Start Creating Music
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              You haven't generated any music yet. Try our AI generator to create your first track!
            </p>
            <Link to="/ai-generator">
              <Button>Generate Your First Track</Button>
            </Link>
          </div>
        </Card>
      )}
    </div>
  )
}

export default Dashboard
