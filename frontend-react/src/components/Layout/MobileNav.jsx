import { NavLink } from 'react-router-dom'
import { Home, Music, Sparkles, History, Info } from 'lucide-react'

const navItems = [
  { to: '/dashboard', icon: Home, label: 'Home' },
  { to: '/spotify-recommendations', icon: Music, label: 'Spotify' },
  { to: '/ai-generator', icon: Sparkles, label: 'AI Gen' },
  { to: '/history', icon: History, label: 'History' },
  { to: '/about', icon: Info, label: 'About' },
]

const MobileNav = () => {
  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white/90 dark:bg-gray-900/90 backdrop-blur-lg border-t border-gray-200 dark:border-gray-800 z-50" aria-label="Mobile navigation">
      <div className="flex justify-around items-center h-16 px-2">
        {navItems.map((item) => {
          const Icon = item.icon

          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex flex-col items-center justify-center flex-1 h-full space-y-1 transition-colors ${
                  isActive
                    ? 'text-primary dark:text-primary-light'
                    : 'text-gray-600 dark:text-gray-400 hover:text-primary dark:hover:text-primary-light'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <Icon className={`w-5 h-5 ${isActive ? 'scale-110' : ''} transition-transform`} />
                  <span className="text-xs font-medium">{item.label}</span>
                  {isActive && (
                    <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-12 h-1 bg-gradient-to-r from-primary to-secondary rounded-t-full" />
                  )}
                </>
              )}
            </NavLink>
          )
        })}
      </div>
    </nav>
  )
}

export default MobileNav
