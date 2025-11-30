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
    <div className="min-h-screen bg-[#1E2233] transition-colors duration-300 relative overflow-hidden">
      {/* Ambient gradient background */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-[600px] h-[600px] bg-primary/10 rounded-full blur-[120px] animate-pulse-slow" />
        <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-secondary/8 rounded-full blur-[100px] animate-pulse-slow" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-accent/6 rounded-full blur-[90px] animate-pulse-slow" style={{ animationDelay: '2s' }} />
      </div>
      
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
