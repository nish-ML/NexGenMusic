import { useState, useEffect } from 'react'
import { Sparkles, Download, RotateCcw, Save, AlertCircle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import Card from '../components/UI/Card'
import Button from '../components/UI/Button'
import MoodSelector from '../components/AIGenerator/MoodSelector'
import MusicPlayer from '../components/AIGenerator/MusicPlayer'
import { useAudio } from '../contexts/AudioContext'
import { saveToHistory } from '../utils/historyStorage'
import { useKeyboardShortcuts } from '../hooks/useKeyboardShortcuts'

const AI_GENERATOR_URL = import.meta.env.VITE_AI_GENERATOR_URL

const AIGenerator = () => {
  const [selectedMood, setSelectedMood] = useState('happy')
  const [tempo, setTempo] = useState(120)
  const [genre, setGenre] = useState('electronic')
  const [duration, setDuration] = useState(30)
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState(null)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)
  
  const { loadTrack, currentTrack, reset, togglePlay } = useAudio()

  // Keyboard shortcuts
  useKeyboardShortcuts({
    'g': () => !generating && handleGenerate(),
    ' ': () => currentTrack && togglePlay(),
  })

  const handleGenerate = async () => {
    setGenerating(true)
    setError(null)
    setSaveSuccess(false)
    reset()

    try {
      const response = await fetch(AI_GENERATOR_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          mood: selectedMood,
          tempo,
          genre,
          duration,
        }),
      })

      const contentType = response.headers.get('content-type')
      
      if (!response.ok) {
        // Try to parse error as JSON, fallback to text
        let errorMessage = 'Generation failed'
        try {
          const errorData = await response.json()
          errorMessage = errorData.message || errorData.error || errorMessage
        } catch {
          errorMessage = await response.text() || errorMessage
        }
        throw new Error(errorMessage)
      }

      // Handle binary audio response
      if (contentType && contentType.startsWith('audio/')) {
        const audioBlob = await response.blob()
        
        const metadata = {
          title: `${selectedMood.charAt(0).toUpperCase() + selectedMood.slice(1)} Track`,
          mood: selectedMood,
          tempo,
          genre,
          duration,
          timestamp: new Date().toISOString(),
        }

        await loadTrack(audioBlob, metadata)
      } else {
        throw new Error('Invalid response format - expected audio file')
      }
    } catch (err) {
      setError(err.message)
      console.error('Generation error:', err)
    } finally {
      setGenerating(false)
    }
  }

  const handleDownload = () => {
    if (!currentTrack?.blob) return

    const url = URL.createObjectURL(currentTrack.blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `nexgenmusic_${selectedMood}_${Date.now()}.mp3`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handleSave = () => {
    if (!currentTrack) return
    saveToHistory(currentTrack)
    setSaveSuccess(true)
    setTimeout(() => setSaveSuccess(false), 3000)
  }

  // Update page background gradient based on mood
  useEffect(() => {
    const root = document.documentElement
    const moodGradients = {
      happy: 'linear-gradient(135deg, rgba(251, 191, 36, 0.05) 0%, rgba(249, 115, 22, 0.05) 100%)',
      sad: 'linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(99, 102, 241, 0.05) 100%)',
      chill: 'linear-gradient(135deg, rgba(167, 139, 250, 0.05) 0%, rgba(236, 72, 153, 0.05) 100%)',
      energetic: 'linear-gradient(135deg, rgba(249, 115, 22, 0.05) 0%, rgba(239, 68, 68, 0.05) 100%)',
      romantic: 'linear-gradient(135deg, rgba(244, 63, 94, 0.05) 0%, rgba(236, 72, 153, 0.05) 100%)',
      focus: 'linear-gradient(135deg, rgba(20, 184, 166, 0.05) 0%, rgba(6, 182, 212, 0.05) 100%)',
    }
    root.style.setProperty('--mood-gradient', moodGradients[selectedMood])
  }, [selectedMood])

  const moodColors = {
    happy: 'from-yellow-400 to-orange-400',
    sad: 'from-blue-400 to-indigo-400',
    chill: 'from-purple-400 to-pink-400',
    energetic: 'from-orange-400 to-red-400',
    romantic: 'from-rose-400 to-pink-400',
    focus: 'from-teal-400 to-cyan-400',
  }

  return (
    <motion.div 
      className="max-w-6xl mx-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gradient mb-2">AI Mood Generator</h1>
        <p className="text-gray-600 dark:text-gray-400">Create music that matches your vibe</p>
        <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
          Press <kbd className="px-2 py-1 bg-gray-200 dark:bg-gray-700 rounded">G</kbd> to generate, 
          <kbd className="px-2 py-1 bg-gray-200 dark:bg-gray-700 rounded ml-1">Space</kbd> to play/pause
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <Card className="h-fit">
          <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
            Configure Your Track
          </h2>

          {/* Mood Selector */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Select Mood
            </label>
            <MoodSelector selected={selectedMood} onChange={setSelectedMood} />
          </div>

          {/* Tempo Slider */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Tempo: {tempo} BPM
            </label>
            <input
              type="range"
              min="60"
              max="180"
              value={tempo}
              onChange={(e) => setTempo(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-primary"
            />
            <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
              <span>Slow</span>
              <span>Fast</span>
            </div>
          </div>

          {/* Genre Dropdown */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Genre
            </label>
            <select
              value={genre}
              onChange={(e) => setGenre(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border-2 border-gray-300 dark:border-gray-600 focus:border-primary focus:outline-none transition-all"
            >
              <option value="electronic">Electronic</option>
              <option value="ambient">Ambient</option>
              <option value="classical">Classical</option>
              <option value="jazz">Jazz</option>
              <option value="rock">Rock</option>
              <option value="pop">Pop</option>
            </select>
          </div>

          {/* Advanced Options */}
          <button
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-primary hover:text-primary-dark font-medium mb-4 transition-colors"
          >
            {showAdvanced ? '− Hide' : '+ Show'} Advanced Options
          </button>

          {showAdvanced && (
            <div className="mb-6 p-4 bg-gray-50 dark:bg-gray-900/50 rounded-xl">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                Duration: {duration}s
              </label>
              <input
                type="range"
                min="15"
                max="120"
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
                className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-primary"
              />
            </div>
          )}

          {/* Generate Button */}
          <Button
            onClick={handleGenerate}
            loading={generating}
            disabled={generating}
            className={`w-full py-4 text-lg animate-pulse-slow bg-gradient-to-r ${moodColors[selectedMood]}`}
          >
            <Sparkles className="w-5 h-5 inline mr-2" />
            {generating ? 'Generating...' : 'Generate Music'}
          </Button>

          {/* Microcopy */}
          <p className="mt-4 text-sm text-gray-500 dark:text-gray-400 text-center">
            {selectedMood === 'energetic' && '⚡ Feeling energetic? Try a 140 BPM synth mix!'}
            {selectedMood === 'chill' && '🌙 Perfect for late-night vibes'}
            {selectedMood === 'happy' && '☀️ Brighten your day with upbeat melodies'}
            {selectedMood === 'sad' && '🌧️ Let the music embrace your emotions'}
            {selectedMood === 'romantic' && '💕 Set the mood with gentle harmonies'}
            {selectedMood === 'focus' && '🎯 Enhance your concentration'}
          </p>

          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mt-4 p-3 bg-red-100 dark:bg-red-900/20 border border-red-300 dark:border-red-800 rounded-xl text-red-700 dark:text-red-400 text-sm flex items-start gap-2"
              >
                <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
                <span>{error}</span>
              </motion.div>
            )}
          </AnimatePresence>
        </Card>

        {/* Result Section */}
        <Card className={`h-fit bg-gradient-to-br ${moodColors[selectedMood]} bg-opacity-10`}>
          <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
            Your Generated Track
          </h2>

          {currentTrack ? (
            <>
              <MusicPlayer mood={selectedMood} />

              {/* Action Buttons */}
              <div className="grid grid-cols-3 gap-3 mt-6">
                <Button onClick={handleDownload} variant="secondary" className="flex-col h-20">
                  <Download className="w-5 h-5 mb-1" />
                  <span className="text-xs">Download</span>
                </Button>
                <Button onClick={handleGenerate} variant="secondary" className="flex-col h-20" disabled={generating}>
                  <RotateCcw className="w-5 h-5 mb-1" />
                  <span className="text-xs">Regenerate</span>
                </Button>
                <Button onClick={handleSave} variant="secondary" className="flex-col h-20">
                  <Save className="w-5 h-5 mb-1" />
                  <span className="text-xs">{saveSuccess ? 'Saved!' : 'Save'}</span>
                </Button>
              </div>
              
              <AnimatePresence>
                {saveSuccess && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className="mt-4 p-3 bg-green-100 dark:bg-green-900/20 border border-green-300 dark:border-green-800 rounded-xl text-green-700 dark:text-green-400 text-sm text-center"
                  >
                    ✓ Track saved to history!
                  </motion.div>
                )}
              </AnimatePresence>
            </>
          ) : (
            <div className="text-center py-12">
              <Sparkles className="w-16 h-16 mx-auto mb-4 text-gray-400 dark:text-gray-600 animate-pulse" />
              <p className="text-gray-500 dark:text-gray-400">
                {generating ? 'Creating your masterpiece...' : 'Generate a track to see it here'}
              </p>
            </div>
          )}
        </Card>
      </div>
    </motion.div>
  )
}

export default AIGenerator
