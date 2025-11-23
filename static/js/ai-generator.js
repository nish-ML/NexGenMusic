// AI Mood Generator Page
const API_BASE = '/api/';
let userToken = null;
let currentAudioUrl = null;
let currentMusicData = null;

// Get token from localStorage
function getToken() {
    return localStorage.getItem('access_token') || localStorage.getItem('token');
}

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    userToken = getToken();
    
    // Check if user is logged in
    if (!userToken) {
        alert('Please log in to use the AI generator');
        window.location.href = '/';
        return;
    }
    
    // Mood chip selection
    const moodChips = document.querySelectorAll('.mood-chip');
    moodChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const mood = chip.getAttribute('data-mood');
            selectMood(mood, chip);
        });
    });
    
    // Generate button
    const generateBtn = document.getElementById('generateBtn');
    if (generateBtn) {
        generateBtn.addEventListener('click', generateMusic);
    }
    
    // Download button
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadMusic);
    }
    
    // Save history button
    const saveHistoryBtn = document.getElementById('saveHistoryBtn');
    if (saveHistoryBtn) {
        saveHistoryBtn.addEventListener('click', saveToHistory);
    }
    
    // Regenerate button
    const regenerateBtn = document.getElementById('regenerateBtn');
    if (regenerateBtn) {
        regenerateBtn.addEventListener('click', generateMusic);
    }
});

// Select mood
function selectMood(mood, chipElement) {
    document.getElementById('moodInput').value = mood;
    
    // Update active state
    document.querySelectorAll('.mood-chip').forEach(chip => {
        chip.classList.remove('active');
    });
    if (chipElement) {
        chipElement.classList.add('active');
    }
}

// Generate music
async function generateMusic() {
    const title = document.getElementById('titleInput').value.trim();
    const mood = document.getElementById('moodInput').value.trim();
    const tempo = document.getElementById('tempoInput').value;
    const genre = document.getElementById('genreInput').value;
    const btn = document.getElementById('generateBtn');
    const playerSection = document.getElementById('playerSection');

    if (!title) {
        alert('Please enter a title for your track!');
        return;
    }

    if (!mood) {
        alert('Please select or enter a mood!');
        return;
    }

    // Check token again
    if (!userToken) {
        alert('Session expired. Please log in again.');
        window.location.href = '/';
        return;
    }

    // Show loading
    btn.disabled = true;
    btn.innerHTML = '<div class="loading-spinner" style="width:30px;height:30px;margin:0 auto;border-width:3px;"></div>';
    playerSection.style.display = 'none';

    try {
        console.log('Generating music for mood:', mood);
        
        // Call backend API
        const response = await fetch(API_BASE + 'generate-audio/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + userToken
            },
            body: JSON.stringify({ 
                title: title,
                text: `I'm feeling ${mood}`,
                mood: mood,
                tempo: tempo,
                genre: genre,
                intensity: 0.7
            })
        });

        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);

        if (response.ok && data.audio_url) {
            // Fetch the actual audio file as blob
            const audioResponse = await fetch(data.audio_url);
            const audioBlob = await audioResponse.blob();
            
            // Create object URL from blob
            const audioURL = URL.createObjectURL(audioBlob);
            
            // Clean up previous URL
            if (currentAudioUrl) {
                URL.revokeObjectURL(currentAudioUrl);
            }
            
            currentAudioUrl = audioURL;
            currentMusicData = {
                title: title,
                mood: mood,
                tempo: tempo,
                genre: genre || 'Any',
                timestamp: new Date().toISOString(),
                audioUrl: audioURL,
                blob: audioBlob
            };
            
            // Automatically save to history
            saveToHistoryAuto(currentMusicData);
            
            // Update UI
            document.getElementById('moodBadge').textContent = `Mood: ${mood}`;
            document.getElementById('tempoBadge').textContent = `Tempo: ${tempo}`;
            document.getElementById('genreBadge').textContent = `Genre: ${genre || 'Any'}`;
            
            // Load audio into player
            const audioPlayer = document.getElementById('audioPlayer');
            const audioSource = document.getElementById('audioSource');
            audioSource.src = audioURL;
            audioPlayer.load();
            
            // Show player section
            playerSection.style.display = 'block';
            
            // Wait for metadata to load
            audioPlayer.addEventListener('loadedmetadata', function() {
                console.log('Audio duration:', audioPlayer.duration, 'seconds');
            }, { once: true });
            
            // Auto-play after loading
            audioPlayer.addEventListener('canplay', function() {
                audioPlayer.play().catch(e => {
                    console.log('Auto-play prevented. Click play button.');
                });
            }, { once: true });
            
            // Scroll to player
            setTimeout(() => {
                playerSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 300);
        } else {
            // Handle specific error cases
            if (response.status === 401) {
                alert('Session expired. Please log in again.');
                localStorage.removeItem('access_token');
                localStorage.removeItem('token');
                window.location.href = '/';
            } else if (response.status === 500) {
                alert('Server error: ' + (data.error || 'Audio generation failed. Please ensure dependencies are installed.'));
            } else {
                alert('Failed to generate music: ' + (data.error || 'Unknown error'));
            }
        }
    } catch (error) {
        console.error('Generation error:', error);
        alert('Connection error. Please check your internet connection and try again.');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span class="btn-icon">✨</span><span class="btn-text">Generate My Music</span>';
    }
}

// Download music
function downloadMusic() {
    if (currentAudioUrl && currentMusicData) {
        const mood = currentMusicData.mood || 'music';
        const timestamp = Date.now();
        const filename = `nexgenmusic_${mood}_${timestamp}.wav`;
        
        const link = document.createElement('a');
        link.href = currentAudioUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } else {
        alert('No music to download. Generate music first!');
    }
}

// Automatically save to history (without alert)
function saveToHistoryAuto(musicData) {
    if (!musicData || !musicData.blob) {
        return;
    }
    
    // Get existing history
    let history = JSON.parse(localStorage.getItem('musicHistory') || '[]');
    
    // Add current music (store as data URL for persistence)
    const reader = new FileReader();
    reader.onloadend = function() {
        const dataUrl = reader.result;
        
        const historyItem = {
            id: Date.now(),
            title: musicData.title || 'Untitled Track',
            mood: musicData.mood,
            tempo: musicData.tempo,
            genre: musicData.genre,
            timestamp: musicData.timestamp,
            audioDataUrl: dataUrl,
            source: 'AI Generator'
        };
        
        history.unshift(historyItem);
        
        // Keep only last 50 items
        if (history.length > 50) {
            history = history.slice(0, 50);
        }
        
        localStorage.setItem('musicHistory', JSON.stringify(history));
        console.log('✅ Music automatically saved to history');
    };
    
    reader.readAsDataURL(musicData.blob);
}

// Save to history (manual - shows confirmation)
function saveToHistory() {
    if (!currentMusicData) {
        alert('No music to save. Generate music first!');
        return;
    }
    
    alert('✅ Music already saved to history automatically!');
}
