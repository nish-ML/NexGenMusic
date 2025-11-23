import { createContext, useContext, useState, useRef, useEffect } from 'react'

const AudioContext = createContext()

export const useAudio = () => {
  const context = useContext(AudioContext)
  if (!context) {
    throw new Error('useAudio must be used within AudioProvider')
  }
  return context
}

export const AudioProvider = ({ children }) => {
  const audioRef = useRef(new Audio())
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [currentTrack, setCurrentTrack] = useState(null)

  useEffect(() => {
    const audio = audioRef.current

    const handleTimeUpdate = () => setCurrentTime(audio.currentTime)
    const handleLoadedMetadata = () => setDuration(audio.duration)
    const handleEnded = () => setIsPlaying(false)

    audio.addEventListener('timeupdate', handleTimeUpdate)
    audio.addEventListener('loadedmetadata', handleLoadedMetadata)
    audio.addEventListener('ended', handleEnded)

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate)
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata)
      audio.removeEventListener('ended', handleEnded)
    }
  }, [])

  const loadTrack = async (audioBlob, metadata) => {
    const audio = audioRef.current
    const url = URL.createObjectURL(audioBlob)
    
    audio.src = url
    audio.load()
    
    return new Promise((resolve) => {
      audio.addEventListener('loadedmetadata', () => {
        setCurrentTrack({ ...metadata, url, blob: audioBlob })
        setDuration(audio.duration)
        resolve(audio.duration)
      }, { once: true })
    })
  }

  const play = () => {
    audioRef.current.play()
    setIsPlaying(true)
  }

  const pause = () => {
    audioRef.current.pause()
    setIsPlaying(false)
  }

  const togglePlay = () => {
    if (isPlaying) {
      pause()
    } else {
      play()
    }
  }

  const seek = (time) => {
    audioRef.current.currentTime = time
    setCurrentTime(time)
  }

  const reset = () => {
    audioRef.current.pause()
    audioRef.current.currentTime = 0
    setIsPlaying(false)
    setCurrentTime(0)
    setDuration(0)
    if (currentTrack?.url) {
      URL.revokeObjectURL(currentTrack.url)
    }
    setCurrentTrack(null)
  }

  return (
    <AudioContext.Provider value={{
      isPlaying,
      currentTime,
      duration,
      currentTrack,
      loadTrack,
      play,
      pause,
      togglePlay,
      seek,
      reset
    }}>
      {children}
    </AudioContext.Provider>
  )
}
