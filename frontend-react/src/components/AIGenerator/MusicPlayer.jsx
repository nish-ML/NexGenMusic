import { Play, Pause } from 'lucide-react'
import { useAudio } from '../../contexts/AudioContext'
import Waveform from './Waveform'

const MusicPlayer = ({ mood }) => {
  const { isPlaying, currentTime, duration, currentTrack, togglePlay, seek } = useAudio()

  const formatTime = (seconds) => {
    if (!seconds || isNaN(seconds)) return '0:00'
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const handleSeek = (e) => {
    const rect = e.currentTarget.getBoundingClientRect()
    const x = e.clientX - rect.left
    const percentage = x / rect.width
    const newTime = percentage * duration
    seek(newTime)
  }

  const moodColors = {
    happy: 'from-yellow-400 to-orange-400',
    sad: 'from-blue-400 to-indigo-400',
    chill: 'from-purple-400 to-pink-400',
    energetic: 'from-orange-400 to-red-400',
    romantic: 'from-rose-400 to-pink-400',
    focus: 'from-teal-400 to-cyan-400',
  }

  return (
    <div className="space-y-6">
      {/* Circular Player */}
      <div className="relative flex justify-center">
        <div className={`
          w-48 h-48 rounded-full bg-gradient-to-br ${moodColors[mood]}
          flex items-center justify-center
          ${isPlaying ? 'animate-pulse-slow shadow-glow-lg' : 'shadow-glow'}
          transition-all duration-300
        `}>
          <button
            onClick={togglePlay}
            className="w-20 h-20 rounded-full bg-white dark:bg-gray-900 flex items-center justify-center hover:scale-110 transition-transform shadow-xl"
            aria-label={isPlaying ? 'Pause' : 'Play'}
          >
            {isPlaying ? (
              <Pause className="w-10 h-10 text-gray-900 dark:text-white" fill="currentColor" />
            ) : (
              <Play className="w-10 h-10 text-gray-900 dark:text-white ml-1" fill="currentColor" />
            )}
          </button>
        </div>
      </div>

      {/* Track Info */}
      <div className="text-center">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-1">
          {currentTrack?.title || 'Untitled Track'}
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          {currentTrack?.mood && `${currentTrack.mood.charAt(0).toUpperCase() + currentTrack.mood.slice(1)} • `}
          {currentTrack?.tempo && `${currentTrack.tempo} BPM • `}
          {currentTrack?.genre && currentTrack.genre.charAt(0).toUpperCase() + currentTrack.genre.slice(1)}
        </p>
      </div>

      {/* Waveform */}
      <Waveform isPlaying={isPlaying} mood={mood} />

      {/* Seek Bar */}
      <div className="space-y-2">
        <div
          onClick={handleSeek}
          className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full cursor-pointer overflow-hidden"
          role="slider"
          aria-label="Seek"
          aria-valuemin={0}
          aria-valuemax={duration}
          aria-valuenow={currentTime}
        >
          <div
            className={`h-full bg-gradient-to-r ${moodColors[mood]} transition-all duration-100`}
            style={{ width: `${duration ? (currentTime / duration) * 100 : 0}%` }}
          />
        </div>
        <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400">
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </div>
      </div>
    </div>
  )
}

export default MusicPlayer
