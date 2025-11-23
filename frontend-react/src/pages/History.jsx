import { useState, useEffect } from 'react'
import { Download, Trash2, Play, FileDown } from 'lucide-react'
import Card from '../components/UI/Card'
import Button from '../components/UI/Button'
import { getHistory, deleteFromHistory, exportHistoryCSV } from '../utils/historyStorage'
import { motion } from 'framer-motion'

const History = () => {
  const [history, setHistory] = useState([])

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = () => {
    const data = getHistory()
    setHistory(data)
  }

  const handleDelete = (id) => {
    if (confirm('Are you sure you want to delete this track?')) {
      deleteFromHistory(id)
      loadHistory()
    }
  }

  const handleDownload = (track) => {
    if (!track.blob) return
    
    const url = URL.createObjectURL(track.blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${track.title.replace(/\s+/g, '_')}.mp3`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handleExport = () => {
    exportHistoryCSV()
  }

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const moodColors = {
    happy: 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-400',
    sad: 'bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400',
    chill: 'bg-purple-100 dark:bg-purple-900/20 text-purple-700 dark:text-purple-400',
    energetic: 'bg-orange-100 dark:bg-orange-900/20 text-orange-700 dark:text-orange-400',
    romantic: 'bg-rose-100 dark:bg-rose-900/20 text-rose-700 dark:text-rose-400',
    focus: 'bg-teal-100 dark:bg-teal-900/20 text-teal-700 dark:text-teal-400',
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gradient mb-2">Generation History</h1>
          <p className="text-gray-600 dark:text-gray-400">
            {history.length} track{history.length !== 1 ? 's' : ''} generated
          </p>
        </div>
        {history.length > 0 && (
          <Button onClick={handleExport} variant="secondary">
            <FileDown className="w-4 h-4 mr-2" />
            Export CSV
          </Button>
        )}
      </div>

      {/* History List */}
      {history.length === 0 ? (
        <Card className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400 text-lg">
            No tracks generated yet. Start creating music in the AI Generator!
          </p>
        </Card>
      ) : (
        <div className="space-y-4">
          {history.map((track, index) => (
            <motion.div
              key={track.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Card className="flex items-center gap-4 hover:shadow-card-hover">
                {/* Play Button */}
                <button className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center hover:shadow-glow transition-all">
                  <Play className="w-5 h-5 text-white ml-0.5" fill="white" />
                </button>

                {/* Track Info */}
                <div className="flex-1 min-w-0">
                  <h3 className="font-bold text-lg text-gray-900 dark:text-white truncate">
                    {track.title}
                  </h3>
                  <div className="flex items-center gap-2 mt-1 flex-wrap">
                    <span className={`px-2 py-1 rounded-lg text-xs font-medium ${moodColors[track.mood] || 'bg-gray-100 dark:bg-gray-700'}`}>
                      {track.mood}
                    </span>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {track.tempo} BPM
                    </span>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {track.duration}s
                    </span>
                    <span className="text-sm text-gray-500 dark:text-gray-500">
                      {formatDate(track.timestamp)}
                    </span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDownload(track)}
                    aria-label="Download track"
                  >
                    <Download className="w-5 h-5" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDelete(track.id)}
                    aria-label="Delete track"
                    className="text-red-500 hover:text-red-600"
                  >
                    <Trash2 className="w-5 h-5" />
                  </Button>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}

export default History
