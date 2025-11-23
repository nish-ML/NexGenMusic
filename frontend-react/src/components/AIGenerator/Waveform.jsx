import { useEffect, useRef } from 'react'

const Waveform = ({ isPlaying, mood }) => {
  const canvasRef = useRef(null)
  const animationRef = useRef(null)

  const moodColors = {
    happy: ['#fbbf24', '#f97316'],
    sad: ['#3b82f6', '#6366f1'],
    chill: ['#a78bfa', '#ec4899'],
    energetic: ['#f97316', '#ef4444'],
    romantic: ['#f43f5e', '#ec4899'],
    focus: ['#14b8a6', '#06b6d4'],
  }

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    const width = canvas.width
    const height = canvas.height
    const bars = 50
    const barWidth = width / bars

    let phase = 0

    const draw = () => {
      ctx.clearRect(0, 0, width, height)

      const gradient = ctx.createLinearGradient(0, 0, width, 0)
      gradient.addColorStop(0, moodColors[mood][0])
      gradient.addColorStop(1, moodColors[mood][1])
      ctx.fillStyle = gradient

      for (let i = 0; i < bars; i++) {
        const amplitude = isPlaying
          ? Math.sin(phase + i * 0.2) * 0.5 + 0.5
          : 0.3
        const barHeight = amplitude * height * 0.8
        const x = i * barWidth
        const y = (height - barHeight) / 2

        ctx.fillRect(x, y, barWidth - 2, barHeight)
      }

      if (isPlaying) {
        phase += 0.1
      }

      animationRef.current = requestAnimationFrame(draw)
    }

    draw()

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [isPlaying, mood])

  return (
    <canvas
      ref={canvasRef}
      width={400}
      height={80}
      className="w-full h-20 rounded-xl"
      aria-hidden="true"
    />
  )
}

export default Waveform
