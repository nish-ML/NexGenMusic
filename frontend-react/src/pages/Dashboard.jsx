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
      link: '/ai-generator'
    },
    {
      title: 'Spotify Recommendations',
      description: 'Get personalized suggestions',
      icon: Music,
      link: '/spotify-recommendations'
    },
    {
      title: 'Generation History',
      description: 'View your past creations',
      icon: History,
      link: '/history'
    }
  ]

  const statCards = [
    {
      label: 'Total Projects',
      value: 24,
      icon: Music,
      color: 'text-green-500',
      trend: 'Increased from last month',
      trendPositive: true
    },
    {
      label: 'Ended Projects',
      value: 10,
      icon: TrendingUp,
      color: 'text-green-500',
      trend: 'Increased from last month',
      trendPositive: true
    },
    {
      label: 'Running Projects',
      value: 12,
      icon: Clock,
      color: 'text-green-500',
      trend: 'Increased from last month',
      trendPositive: true
    },
    {
      label: 'Pending Projects',
      value: 2,
      icon: Clock,
      color: 'text-green-500',
      trend: 'On Discuss',
      trendPositive: null
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
    <div className="min-h-screen bg-gradient-to-br from-neutral-50 to-neutral-100">
      {/* Enhanced Header */}
      <div className="bg-white/80 backdrop-blur-xl border-b border-neutral-200 px-10 py-8 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-50/50 to-blue-50/30 -z-10"></div>
        <div className="flex items-center justify-between relative z-10">
          <div className="animate-fade-in">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-emerald-600 to-emerald-700 bg-clip-text text-transparent mb-2">
              Dashboard
            </h1>
            <p className="text-lg text-neutral-600">Plan, prioritize, and accomplish your music tasks with ease.</p>
          </div>
          <div className="flex items-center gap-3 animate-fade-in" style={{animationDelay: '0.2s'}}>
            <Button className="bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800 text-white px-6 py-3 rounded-2xl font-semibold shadow-lg hover:shadow-emerald-500/25 transition-all duration-300 hover:-translate-y-1 relative overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <svg className="w-4 h-4 mr-2 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"></path>
              </svg>
              <span className="relative z-10">Add Project</span>
            </Button>
            <Button variant="outline" className="px-6 py-3 rounded-2xl font-semibold border-neutral-300 bg-white/50 backdrop-blur-sm hover:bg-white/80 hover:border-emerald-300 transition-all duration-300 hover:-translate-y-0.5">
              Import Data
            </Button>
          </div>
        </div>
      </div>

      {/* Enhanced Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 px-10">
        {statCards.map((stat, index) => {
          const isPrimary = index === 0 // First card is primary (green)
          return (
            <Card 
              key={index} 
              className={`p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 hover:scale-105 rounded-3xl relative overflow-hidden group animate-bounce-in ${
                isPrimary 
                  ? 'bg-gradient-to-br from-emerald-600 to-emerald-700 text-white shadow-emerald-500/25' 
                  : 'bg-white/80 backdrop-blur-xl border border-neutral-200 hover:border-emerald-300'
              }`}
              style={{animationDelay: `${index * 0.1}s`}}
            >
              {/* Decorative background element */}
              <div className={`absolute top-0 right-0 w-24 h-24 rounded-full opacity-20 transition-opacity duration-300 group-hover:opacity-40 ${
                isPrimary 
                  ? 'bg-gradient-radial from-white/30 to-transparent' 
                  : 'bg-gradient-radial from-emerald-200 to-transparent'
              }`}></div>
              
              <div className="flex items-start justify-between mb-4 relative z-10">
                <div className="flex-1">
                  <p className={`text-sm font-medium mb-2 uppercase tracking-wide ${
                    isPrimary ? 'text-emerald-100' : 'text-neutral-600'
                  }`}>{stat.label}</p>
                  <p className={`text-4xl font-bold ${
                    isPrimary ? 'text-white' : 'text-neutral-900'
                  }`}>{stat.value}</p>
                </div>
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300 group-hover:scale-110 ${
                  isPrimary ? 'bg-white/20' : 'bg-emerald-50'
                }`}>
                  <svg className={`w-6 h-6 ${
                    isPrimary ? 'text-white' : 'text-emerald-600'
                  }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                  </svg>
                </div>
              </div>
              <div className={`flex items-center gap-2 text-sm font-medium relative z-10 ${
                stat.trendPositive === true ? (isPrimary ? 'text-emerald-100' : 'text-emerald-600') : 
                stat.trendPositive === false ? 'text-red-600' : 
                (isPrimary ? 'text-emerald-100' : 'text-neutral-600')
              }`}>
                {stat.trendPositive === true && (
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                  </svg>
                )}
                {stat.trend}
              </div>
            </Card>
          )
        })}
      </div>

      {/* Enhanced Quick Actions */}
      <div className="mb-8 px-10">
        <h2 className="text-2xl font-semibold text-neutral-900 mb-6 relative animate-fade-in" style={{animationDelay: '0.5s'}}>
          Quick Actions
          <div className="absolute bottom-0 left-0 w-16 h-1 bg-gradient-to-r from-emerald-600 to-emerald-700 rounded-full"></div>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action, index) => {
            const Icon = action.icon
            return (
              <Link key={index} to={action.link}>
                <Card 
                  className="p-6 hover:shadow-2xl hover:border-emerald-400 transition-all duration-300 hover:-translate-y-2 cursor-pointer h-full rounded-3xl border border-neutral-200 bg-white/80 backdrop-blur-xl relative overflow-hidden group animate-fade-in"
                  style={{animationDelay: `${0.6 + index * 0.1}s`}}
                >
                  {/* Hover background effect */}
                  <div className="absolute inset-0 bg-gradient-to-br from-emerald-50/50 to-blue-50/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  
                  <div className="flex items-start gap-4 relative z-10">
                    <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-600 to-emerald-700 flex items-center justify-center flex-shrink-0 shadow-lg shadow-emerald-500/25 group-hover:scale-110 transition-transform duration-300">
                      <Icon className="w-7 h-7 text-white" />
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-neutral-900 mb-2 group-hover:text-emerald-700 transition-colors duration-300">
                        {action.title}
                      </h3>
                      <p className="text-neutral-600 text-sm leading-relaxed">
                        {action.description}
                      </p>
                    </div>
                  </div>
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

      {/* Enhanced Empty State */}
      {stats.totalGenerated === 0 && (
        <div className="px-10">
          <h2 className="text-2xl font-semibold text-neutral-900 mb-6 relative animate-fade-in" style={{animationDelay: '0.9s'}}>
            Recent Generations
            <div className="absolute bottom-0 left-0 w-16 h-1 bg-gradient-to-r from-emerald-600 to-emerald-700 rounded-full"></div>
          </h2>
          <Card className="p-12 text-center bg-white/80 backdrop-blur-xl border border-neutral-200 rounded-3xl animate-fade-in" style={{animationDelay: '1.0s'}}>
            <div className="max-w-md mx-auto">
              <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-emerald-100 to-emerald-200 flex items-center justify-center mx-auto mb-6 shadow-lg">
                <Music className="w-10 h-10 text-emerald-600" />
              </div>
              <h3 className="text-2xl font-semibold text-neutral-900 mb-3">
                Start Creating Music
              </h3>
              <p className="text-neutral-600 mb-8 text-lg leading-relaxed">
                You haven't generated any music yet. Try our AI generator to create your first track and begin your musical journey!
              </p>
              <Link to="/ai-generator">
                <Button className="bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800 text-white px-8 py-4 rounded-2xl font-semibold shadow-lg hover:shadow-emerald-500/25 transition-all duration-300 hover:-translate-y-1 text-lg">
                  Generate Your First Track
                </Button>
              </Link>
            </div>
          </Card>
        </div>
      )}
    </div>
  )
}

export default Dashboard
