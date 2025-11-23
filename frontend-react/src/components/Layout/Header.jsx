import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Sun, Moon, Bell, User, LogOut, Settings, Sparkles } from 'lucide-react'
import { useTheme } from '../../contexts/ThemeContext'
import { useSettings } from '../../contexts/SettingsContext'
import Button from '../UI/Button'
import ProfileModal from '../Profile/ProfileModal'

const Header = () => {
  const { theme, toggleTheme } = useTheme()
  const { settings, toggleParticles } = useSettings()
  const navigate = useNavigate()
  const [showProfileMenu, setShowProfileMenu] = useState(false)
  const [showProfileModal, setShowProfileModal] = useState(false)

  const handleLogout = async () => {
    // Placeholder for logout API call
    // await fetch(import.meta.env.VITE_AUTH_API_URL + '/logout', { method: 'POST' })
    localStorage.removeItem('auth-token')
    navigate('/dashboard-old')
  }

  const OLD_DASHBOARD_URL = import.meta.env.VITE_OLD_DASHBOARD_URL || '/dashboard-old'

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-50 h-16 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg border-b border-gray-200 dark:border-gray-800">
        <div className="h-full px-4 md:px-6 flex items-center justify-between">
          {/* Logo */}
          <button
            onClick={() => window.location.href = OLD_DASHBOARD_URL}
            className="flex items-center space-x-2 group"
            aria-label="Go to home dashboard"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg group-hover:shadow-glow transition-all duration-300">
              <span className="text-white font-bold text-xl">N</span>
            </div>
            <span className="hidden md:block text-xl font-bold text-gradient">NexGenMusic</span>
          </button>

          {/* Right Section */}
          <div className="flex items-center space-x-2 md:space-x-4">
            {/* Particle Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleParticles}
              aria-label={`${settings.particlesEnabled ? 'Disable' : 'Enable'} particle effects`}
              className={`relative ${settings.particlesEnabled ? 'text-primary' : ''}`}
              title="Toggle particle effects"
            >
              <Sparkles className="w-5 h-5" />
            </Button>

            {/* Theme Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
              className="relative"
            >
              {theme === 'dark' ? (
                <Sun className="w-5 h-5" />
              ) : (
                <Moon className="w-5 h-5" />
              )}
            </Button>

            {/* Notifications */}
            <Button
              variant="ghost"
              size="icon"
              aria-label="Notifications"
              className="relative"
            >
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-accent rounded-full"></span>
            </Button>

            {/* Profile Dropdown */}
            <div className="relative">
              <button
                onClick={() => setShowProfileMenu(!showProfileMenu)}
                className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center hover:shadow-glow transition-all duration-300"
                aria-label="User profile menu"
                aria-expanded={showProfileMenu}
              >
                <User className="w-5 h-5 text-white" />
              </button>

              {showProfileMenu && (
                <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-xl shadow-card-hover border border-gray-200 dark:border-gray-700 overflow-hidden">
                  <button
                    onClick={() => {
                      setShowProfileModal(true)
                      setShowProfileMenu(false)
                    }}
                    className="w-full px-4 py-3 text-left hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center space-x-2 transition-colors"
                  >
                    <Settings className="w-4 h-4" />
                    <span>Edit Profile</span>
                  </button>
                  <button
                    onClick={handleLogout}
                    className="w-full px-4 py-3 text-left hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center space-x-2 text-danger transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Logout</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <ProfileModal isOpen={showProfileModal} onClose={() => setShowProfileModal(false)} />
    </>
  )
}

export default Header
