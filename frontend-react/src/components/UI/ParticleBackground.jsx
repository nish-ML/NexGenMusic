import { useEffect, useRef, useState } from 'react'
import { useTheme } from '../../contexts/ThemeContext'

const ParticleBackground = ({ enabled = true }) => {
  const canvasRef = useRef(null)
  const { theme } = useTheme()
  const [particles, setParticles] = useState([])
  const animationRef = useRef(null)

  useEffect(() => {
    if (!enabled) return

    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    // Create particles
    const particleCount = 30
    const newParticles = []
    for (let i = 0; i < particleCount; i++) {
      newParticles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 3 + 1,
        speedX: (Math.random() - 0.5) * 0.5,
        speedY: (Math.random() - 0.5) * 0.5,
        opacity: Math.random() * 0.5 + 0.2,
      })
    }
    setParticles(newParticles)

    // Animation loop
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      newParticles.forEach((particle) => {
        // Update position
        particle.x += particle.speedX
        particle.y += particle.speedY

        // Wrap around edges
        if (particle.x < 0) particle.x = canvas.width
        if (particle.x > canvas.width) particle.x = 0
        if (particle.y < 0) particle.y = canvas.height
        if (particle.y > canvas.height) particle.y = 0

        // Draw particle (music note)
        ctx.fillStyle = theme === 'dark' 
          ? `rgba(139, 92, 246, ${particle.opacity})`
          : `rgba(79, 70, 229, ${particle.opacity})`
        ctx.font = `${particle.size * 8}px Arial`
        ctx.fillText('♪', particle.x, particle.y)
      })

      animationRef.current = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener('resize', resizeCanvas)
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [enabled, theme])

  if (!enabled) return null

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0"
      style={{ opacity: 0.3 }}
      aria-hidden="true"
    />
  )
}

export default ParticleBackground
