const HISTORY_KEY = 'nexgen-music-history'

export const getHistory = () => {
  try {
    const data = localStorage.getItem(HISTORY_KEY)
    return data ? JSON.parse(data) : []
  } catch (error) {
    console.error('Failed to load history:', error)
    return []
  }
}

export const saveToHistory = (track) => {
  try {
    const history = getHistory()
    const newTrack = {
      ...track,
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
    }
    
    // Store without blob for localStorage (blobs can't be serialized)
    const { blob, url, ...trackData } = newTrack
    
    history.unshift(trackData)
    
    // Keep only last 50 tracks
    const trimmed = history.slice(0, 50)
    
    localStorage.setItem(HISTORY_KEY, JSON.stringify(trimmed))
    return newTrack
  } catch (error) {
    console.error('Failed to save to history:', error)
    throw error
  }
}

export const deleteFromHistory = (id) => {
  try {
    const history = getHistory()
    const filtered = history.filter(track => track.id !== id)
    localStorage.setItem(HISTORY_KEY, JSON.stringify(filtered))
  } catch (error) {
    console.error('Failed to delete from history:', error)
    throw error
  }
}

export const clearHistory = () => {
  try {
    localStorage.removeItem(HISTORY_KEY)
  } catch (error) {
    console.error('Failed to clear history:', error)
    throw error
  }
}

export const exportHistoryCSV = () => {
  try {
    const history = getHistory()
    
    if (history.length === 0) {
      alert('No history to export')
      return
    }

    const headers = ['Title', 'Mood', 'Tempo', 'Genre', 'Duration', 'Created At']
    const rows = history.map(track => [
      track.title,
      track.mood,
      track.tempo,
      track.genre,
      track.duration,
      new Date(track.timestamp).toLocaleString()
    ])

    const csv = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n')

    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `nexgenmusic_history_${Date.now()}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Failed to export history:', error)
    throw error
  }
}
