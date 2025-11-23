import { motion } from 'framer-motion'

const moods = [
  { id: 'happy', emoji: '😊', label: 'Happy', color: 'bg-yellow-400' },
  { id: 'sad', emoji: '😢', label: 'Sad', color: 'bg-blue-400' },
  { id: 'chill', emoji: '😌', label: 'Chill', color: 'bg-purple-400' },
  { id: 'energetic', emoji: '⚡', label: 'Energetic', color: 'bg-orange-400' },
  { id: 'romantic', emoji: '💕', label: 'Romantic', color: 'bg-rose-400' },
  { id: 'focus', emoji: '🎯', label: 'Focus', color: 'bg-teal-400' },
]

const MoodSelector = ({ selected, onChange }) => {
  return (
    <div className="grid grid-cols-3 gap-3">
      {moods.map((mood) => (
        <motion.button
          key={mood.id}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => onChange(mood.id)}
          className={`
            p-4 rounded-xl border-2 transition-all duration-200
            ${selected === mood.id
              ? `${mood.color} border-transparent shadow-glow text-white`
              : 'bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
            }
          `}
          aria-label={`Select ${mood.label} mood`}
          aria-pressed={selected === mood.id}
        >
          <div className="text-3xl mb-1">{mood.emoji}</div>
          <div className={`text-sm font-medium ${selected === mood.id ? 'text-white' : 'text-gray-700 dark:text-gray-300'}`}>
            {mood.label}
          </div>
        </motion.button>
      ))}
    </div>
  )
}

export default MoodSelector
