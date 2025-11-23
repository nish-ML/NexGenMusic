import { createContext, useContext, useState, useEffect } from 'react'

const SettingsContext = createContext()

export const useSettings = () => {
  const context = useContext(SettingsContext)
  if (!context) {
    throw new Error('useSettings must be used within SettingsProvider')
  }
  return context
}

export const SettingsProvider = ({ children }) => {
  const [settings, setSettings] = useState(() => {
    const saved = localStorage.getItem('nexgen-settings')
    return saved ? JSON.parse(saved) : {
      particlesEnabled: false, // Default off for performance
      reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      notifications: true,
    }
  })

  useEffect(() => {
    localStorage.setItem('nexgen-settings', JSON.stringify(settings))
  }, [settings])

  const updateSetting = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }))
  }

  const toggleParticles = () => {
    updateSetting('particlesEnabled', !settings.particlesEnabled)
  }

  return (
    <SettingsContext.Provider value={{ settings, updateSetting, toggleParticles }}>
      {children}
    </SettingsContext.Provider>
  )
}
