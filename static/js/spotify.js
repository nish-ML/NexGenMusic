// Spotify Recommendations Page
const API_BASE = '/api/';
let userToken = null;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    userToken = await autoLogin();
    
    // Enter key search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') searchMusic();
        });
    }
});

// Quick search
function quickSearch(query) {
    const searchInput = document.getElementById('searchInput');
    searchInput.value = query;
    
    // Update active chip
    document.querySelectorAll('.chip').forEach(chip => {
        chip.classList.remove('active');
        if (chip.textContent.trim() === query) {
            chip.classList.add('active');
        }
    });
    
    searchMusic();
}

// Search music
async function searchMusic() {
    const query = document.getElementById('searchInput').value.trim();
    const resultsSection = document.getElementById('resultsSection');
    
    if (!query) {
        resultsSection.innerHTML = '<div class="loading"><p>Please enter a search term</p></div>';
        return;
    }

    // Show loading
    resultsSection.innerHTML = `
        <div class="loading">
            <div class="loading-spinner"></div>
            <p>Finding perfect tracks for you...</p>
        </div>
    `;

    try {
        const response = await fetch(API_BASE + 'generate-playlist/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + userToken
            },
            body: JSON.stringify({ 
                mood: query,
                genre: query,
                limit: 12
            })
        });

        const data = await response.json();

        if (response.ok && data.playlist && data.playlist.length > 0) {
            displayResults(data.playlist);
        } else {
            resultsSection.innerHTML = '<div class="loading"><p>No tracks found. Try a different search term.</p></div>';
        }
    } catch (error) {
        console.error('Search error:', error);
        resultsSection.innerHTML = '<div class="loading"><p>Connection error. Please try again.</p></div>';
    }
}

// Display results
function displayResults(tracks) {
    const resultsSection = document.getElementById('resultsSection');
    
    let html = `
        <h2 class="results-header">🎵 Found ${tracks.length} Amazing Tracks</h2>
        <div class="tracks-grid">
    `;

    tracks.forEach((track, index) => {
        // Store track data in a global variable for onclick access
        const trackId = `track_${Date.now()}_${index}`;
        window[trackId] = track;
        
        html += `
            <div class="track-card" style="animation-delay: ${index * 0.1}s">
                <div class="track-image">
                    ${track.album_image ? 
                        `<img src="${track.album_image}" alt="${escapeHtml(track.song_name)}">` : 
                        '🎵'}
                </div>
                <div class="track-info">
                    ${track.popularity ? `<span class="track-popularity">🔥 ${track.popularity}</span>` : ''}
                    <div class="track-title">${escapeHtml(track.song_name)}</div>
                    <div class="track-artist">${escapeHtml(track.artist_name)}</div>
                </div>
                <button class="play-btn" onclick="playOnSpotify('${track.spotify_url}', window['${trackId}'])">
                    ▶️ Play on Spotify
                </button>
            </div>
        `;
    });

    html += '</div>';
    resultsSection.innerHTML = html;
}

// Play on Spotify and save to history
function playOnSpotify(url, trackData) {
    if (url) {
        // Save to history
        saveSpotifyToHistory(trackData);
        
        // Open Spotify
        window.open(url, '_blank');
    }
}

// Save Spotify track to history
function saveSpotifyToHistory(trackData) {
    if (!trackData) return;
    
    // Get existing history
    let history = JSON.parse(localStorage.getItem('musicHistory') || '[]');
    
    const historyItem = {
        id: Date.now(),
        title: trackData.song_name || 'Untitled Track',
        artist: trackData.artist_name || 'Unknown Artist',
        album: trackData.album_name || '',
        mood: trackData.mood || 'Spotify',
        genre: trackData.genre || 'Various',
        timestamp: new Date().toISOString(),
        spotifyUrl: trackData.spotify_url,
        albumImage: trackData.album_image || '',
        source: 'Spotify'
    };
    
    history.unshift(historyItem);
    
    // Keep only last 50 items
    if (history.length > 50) {
        history = history.slice(0, 50);
    }
    
    localStorage.setItem('musicHistory', JSON.stringify(history));
    console.log('✅ Spotify track saved to history:', trackData.song_name);
}


// Helper function to escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Helper function for autoLogin (if not defined elsewhere)
async function autoLogin() {
    const token = localStorage.getItem('access_token') || localStorage.getItem('token');
    if (!token) {
        console.warn('No token found, user may need to log in');
    }
    return token;
}
