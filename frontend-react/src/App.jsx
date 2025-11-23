import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './contexts/ThemeContext'
import { AudioProvider } from './contexts/AudioContext'
import { SettingsProvider } from './contexts/SettingsContext'
import Layout from './components/Layout/Layout'
import Dashboard from './pages/Dashboard'
import SpotifyRecommendations from './pages/SpotifyRecommendations'
import AIGenerator from './pages/AIGenerator'
import History from './pages/History'
import Profile from './pages/Profile'
import About from './pages/About'

function App() {
  return (
    <ThemeProvider>
      <SettingsProvider>
        <AudioProvider>
          <Router>
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route element={<Layout />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/spotify-recommendations" element={<SpotifyRecommendations />} />
                <Route path="/ai-generator" element={<AIGenerator />} />
                <Route path="/history" element={<History />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/about" element={<About />} />
              </Route>
            </Routes>
          </Router>
        </AudioProvider>
      </SettingsProvider>
    </ThemeProvider>
  )
}

export default App
