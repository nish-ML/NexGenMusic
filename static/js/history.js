// History Page
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
});

// Load history from localStorage
function loadHistory() {
    const history = JSON.parse(localStorage.getItem('musicHistory') || '[]');
    const historySection = document.getElementById('historySection');
    const historyEmpty = document.getElementById('historyEmpty');
    const historyGrid = document.getElementById('historyGrid');
    
    if (history.length === 0) {
        historyEmpty.style.display = 'block';
        historyGrid.style.display = 'none';
        return;
    }
    
    historyEmpty.style.display = 'none';
    historyGrid.style.display = 'grid';
    
    // Render history items
    historyGrid.innerHTML = history.map((item, index) => {
        const date = new Date(item.timestamp);
        const formattedDate = date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
        
        return `
            <div class="history-card" style="animation-delay: ${index * 0.1}s">
                <div class="history-header">
                    <div>
                        <div class="history-mood">🎵 ${escapeHtml(item.mood)}</div>
                        <div class="history-date">${formattedDate}</div>
                    </div>
                </div>
                
                <div class="history-details">
                    <span class="history-tag">Tempo: ${escapeHtml(item.tempo)}</span>
                    <span class="history-tag">Genre: ${escapeHtml(item.genre)}</span>
                </div>
                
                <div class="history-audio">
                    <audio controls>
                        <source src="${item.audioDataUrl}" type="audio/wav">
                        Your browser does not support the audio element.
                    </audio>
                </div>
                
                <div class="history-actions">
                    <button class="history-btn download" onclick="downloadHistoryItem(${item.id}, '${escapeHtml(item.mood)}')">
                        📥 Download
                    </button>
                    <button class="history-btn delete" onclick="deleteHistoryItem(${item.id})">
                        🗑️ Delete
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// Download history item
function downloadHistoryItem(id, mood) {
    const history = JSON.parse(localStorage.getItem('musicHistory') || '[]');
    const item = history.find(h => h.id === id);
    
    if (item) {
        const filename = `nexgenmusic_${mood}_${id}.wav`;
        const link = document.createElement('a');
        link.href = item.audioDataUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Delete history item
function deleteHistoryItem(id) {
    if (!confirm('Are you sure you want to delete this item?')) {
        return;
    }
    
    let history = JSON.parse(localStorage.getItem('musicHistory') || '[]');
    history = history.filter(h => h.id !== id);
    localStorage.setItem('musicHistory', JSON.stringify(history));
    
    // Reload history
    loadHistory();
}

// Clear all history
function clearAllHistory() {
    if (!confirm('Are you sure you want to clear all history?')) {
        return;
    }
    
    localStorage.removeItem('musicHistory');
    loadHistory();
}
