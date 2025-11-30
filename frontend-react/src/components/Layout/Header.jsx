import { useState } from 'react'
import { Search, Bell, Sun, Moon } from 'lucide-react'
import { useTheme } from '../../contexts/ThemeContext'

const Header = () => {
  const { theme, toggleTheme } = useTheme()
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <header className="bg-white dark:bg-slate-800 border-b border-gray-200 dark:border-slate-700 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Search */}
        <div className="flex-1 max-w-md">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search task"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-200 dark:border-slate-600 rounded-lg bg-gray-50 dark:bg-slate-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
            <kbd className="absolute right-3 top-1/2 transform -translate-y-1/2 text-xs text-gray-400 bg-gray-100 dark:bg-slate-600 px-2 py-1 rounded">
              ⌘F
            </kbd>
          </div>
        </div>

        {/* Right side controls */}
        <div className="flex items-center gap-4">
          {/* Notifications */}
          <button className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
            <Bell className="w-5 h-5" />
          </button>

          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>

          {/* Profile */}
          <div className="flex items-center gap-3">
            <div className="text-right">
              <div className="text-sm font-medium text-gray-900 dark:text-white">Totok Michael</div>
              <div className="text-xs text-gray-500 dark:text-gray-400">tmichael@gmail.com</div>
            </div>
            <img
              src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
              alt="Profile"
              className="w-10 h-10 rounded-full border-2 border-green-500"
            />
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
