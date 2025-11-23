// API utility functions for backend communication

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export const apiClient = {
  async get(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`)
    }

    return response.json()
  },

  async post(endpoint, data, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      body: JSON.stringify(data),
      ...options,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: response.statusText }))
      throw new Error(error.message || 'API Error')
    }

    return response
  },

  async put(endpoint, data, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      body: JSON.stringify(data),
      ...options,
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`)
    }

    return response.json()
  },

  async delete(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`)
    }

    return response.json()
  },
}

// Specific API functions
export const generateMusic = async (params) => {
  const response = await apiClient.post('/generate-music', params)
  
  // Check if response is audio
  const contentType = response.headers.get('content-type')
  if (contentType && contentType.startsWith('audio/')) {
    return response.blob()
  }
  
  return response.json()
}

export const getSpotifyRecommendations = async (query = '', page = 1) => {
  return apiClient.get(`/spotify/recommendations?q=${query}&page=${page}`)
}

export const saveHistory = async (track) => {
  return apiClient.post('/history', track)
}

export const fetchHistory = async () => {
  return apiClient.get('/history')
}

export const updateProfile = async (profile) => {
  return apiClient.put('/profile', profile)
}

export const logout = async () => {
  return apiClient.post('/auth/logout', {})
}
