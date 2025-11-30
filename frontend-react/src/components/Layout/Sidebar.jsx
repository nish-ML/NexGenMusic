import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  CheckSquare, 
  Calendar, 
  BarChart3, 
  Users, 
  Settings, 
  HelpCircle, 
  LogOut,
  Music
} from 'lucide-react'

const Sidebar = () => {
  const location = useLocation()

  const menuItems = [
    {
      title: 'Dashboard',
      icon: LayoutDashboard,
      path: '/dashboard',
      section: 'menu'
    },
    {
      title: 'Tasks',
      icon: CheckSquare,
      path: '/ai-generator',
      badge: '23',
      section: 'menu'
    },
    {
      title: 'Calendar',
      icon: Calendar,
      path: '/calendar',
      section: 'menu'
    },
    {
      title: 'Analytics',
      icon: BarChart3,
      path: '/analytics',
      section: 'menu'
    },
    {
      title: 'Team',
      icon: Users,
      path: '/team',
      section: 'menu'
    },
    {
      title: 'Settings',
      icon: Settings,
      path: '/settings',
      section: 'general'
    },
    {
      title: 'Help',
      icon: HelpCircle,
      path: '/help',
      section: 'general'
    },
    {
      title: 'Logout',
      icon: LogOut,
      path: '/logout',
      section: 'general'
    }
  ]

  const menuSections = menuItems.reduce((acc, item) => {
    if (!acc[item.section]) {
      acc[item.section] = []
    }
    acc[item.section].push(item)
    return acc
  }, {})

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/')
  }

  return (
    <div className="w-70 bg-gray-50 border-r border-gray-200 h-screen fixed left-0 top-0 overflow-y-auto z-50">
      {/* Logo */}
      <div className="p-6 border-b border-gray-200">
        <Link to="/" className="flex items-center gap-3 text-xl font-bold text-gray-900">
          <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center font-semibold text-white">
            ♪
          </div>
          NexGen Music
        </Link>
      </div>

      {/* Navigation */}
      <nav className="p-4">
        {/* Menu Section */}
        <div className="mb-6">
          <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3 px-3">
            Menu
          </h3>
          <div className="space-y-1">
            {menuSections.menu?.map((item) => {
              const Icon = item.icon
              const active = isActive(item.path)
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-medium transition-all duration-200 relative ${
                    active
                      ? 'bg-emerald-600 text-white font-semibold'
                      : 'text-gray-600 hover:bg-emerald-50 hover:text-emerald-600'
                  }`}
                >
                  <Icon className="w-5 h-5 flex-shrink-0 stroke-1.5" />
                  <span className="flex-1">{item.title}</span>
                  {item.badge && (
                    <span className="bg-emerald-600 text-white text-xs px-2 py-1 rounded-xl font-semibold min-w-5 text-center">
                      {item.badge}
                    </span>
                  )}
                </Link>
              )
            })}
          </div>
        </div>

        {/* General Section */}
        <div>
          <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3 px-3">
            General
          </h3>
          <div className="space-y-1">
            {menuSections.general?.map((item) => {
              const Icon = item.icon
              const active = isActive(item.path)
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-medium transition-all duration-200 ${
                    active
                      ? 'bg-emerald-600 text-white font-semibold'
                      : 'text-gray-600 hover:bg-emerald-50 hover:text-emerald-600'
                  }`}
                >
                  <Icon className="w-5 h-5 flex-shrink-0 stroke-1.5" />
                  <span>{item.title}</span>
                </Link>
              )
            })}
          </div>
        </div>
      </nav>
    </div>
  )
}

export default Sidebar