import { NavLink } from 'react-router-dom'
import { Home, Music, Sparkles, History, Info } from 'lucide-react'

const navItems = [
  { to: '/dashboard', icon: Home, label: 'Dashboard' },
  { to: '/spotify-recommendations', icon: Music, label: 'Spotify' },
  { to: '/ai-generator', icon: Sparkles, label: 'AI Generator' },
  { to: '/history', icon: History, label: 'History' },
  { to: '/about', icon: Info, label: 'About' },
]

const Sidebar = () => {
  return (
    <aside className="hidden md:flex fixed left-0 top-16 bottom-0 w-64 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg border-r border-gray-200 dark:border-gray-800 flex-col">
      <nav className="flex-1 p-4 space-y-2" aria-label="Main navigation">
        {navItems.map((item) => {
          const Icon = item.icon

          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 group relative ${
                  isActive
                    ? 'bg-gradient-to-r from-primary/10 to-secondary/10 text-primary dark:text-primary-light shadow-glow'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  {isActive && (
                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-gradient-to-b from-primary to-secondary rounded-r-full" />
                  )}
                  <Icon className="w-5 h-5 group-hover:scale-110 transition-transform" />
                  <span className="font-medium">{item.label}</span>
                </>
              )}
            </NavLink>
          )
        })}
      </nav>
    </aside>
  )
}

export default Sidebar
