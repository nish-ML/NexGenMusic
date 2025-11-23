import { Outlet } from 'react-router-dom'
import { motion } from 'framer-motion'
import Sidebar from './Sidebar'
import Header from './Header'
import MobileNav from './MobileNav'
import ParticleBackground from '../UI/ParticleBackground'
import { useSettings } from '../../contexts/SettingsContext'

const Layout = () => {
  const { settings } = useSettings()

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300 relative overflow-hidden">
      <ParticleBackground enabled={settings.particlesEnabled} />
      <div className="relative z-10">
        <Header />
        <div className="flex">
          <Sidebar />
          <main className="flex-1 p-4 md:p-6 lg:p-8 ml-0 md:ml-64 mb-16 md:mb-0">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Outlet />
            </motion.div>
          </main>
        </div>
        <MobileNav />
      </div>
    </div>
  )
}

export default Layout
