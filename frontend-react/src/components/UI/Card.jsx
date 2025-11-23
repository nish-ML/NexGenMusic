import { motion } from 'framer-motion'

const Card = ({
  children,
  className = '',
  elevation = 'md',
  hoverTilt = false,
  glowColor = null,
  onClick,
  ...props
}) => {
  const elevations = {
    sm: 'shadow-sm',
    md: 'shadow-card',
    lg: 'shadow-card-hover',
  }

  return (
    <motion.div
      whileHover={hoverTilt ? { scale: 1.02, rotateY: 2, rotateX: 2 } : { scale: 1.01 }}
      transition={{ duration: 0.2 }}
      onClick={onClick}
      className={`
        ${elevations[elevation]}
        ${className}
        bg-white dark:bg-gray-800 rounded-2xl p-6
        border border-gray-200 dark:border-gray-700
        transition-all duration-300
        ${onClick ? 'cursor-pointer' : ''}
        ${glowColor ? `hover:shadow-[0_0_30px_${glowColor}]` : 'hover:shadow-card-hover'}
      `}
      style={glowColor ? { '--glow-color': glowColor } : {}}
      {...props}
    >
      {children}
    </motion.div>
  )
}

export default Card
