// Dashboard functionality
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardStats();
    loadRecentGenerations();
});

// Load dashboard statistics
function loadDashboardStats() {
    const history = getHistory();
    
    // Calculate stats
    const totalGenerated = history.length;
    const genres = history.map(item => item.genre || 'Unknown');
    const genreCounts = genres.reduce((acc, genre) => {
        acc[genre] = (acc[genre] || 0) + 1;
        return acc;
    }, {});
    
    const favoriteGenre = Object.keys(genreCounts).length > 0 
        ? Object.keys(genreCounts).reduce((a, b) => genreCounts[a] > genreCounts[b] ? a : b)
        : 'Unknown';
    
    const listeningTime = Math.round(totalGenerated * 2.5); // ~2.5 min per track
    
    // Update DOM
    document.getElementById('totalGenerated').textContent = totalGenerated;
    document.getElementById('favoriteGenre').textContent = favoriteGenre;
    document.getElementById('listeningTime').textContent = listeningTime + ' min';
}

// Load recent generations
function loadRecentGenerations() {
    const history = getHistory();
    const recentContainer = document.getElementById('recentGenerations');
    
    if (history.length === 0) {
        return; // Keep empty state
    }
    
    // Clear empty state
    recentContainer.innerHTML = '';
    
    // Show last 3 generations
    const recentItems = history.slice(0, 3);
    
    recentItems.forEach(item => {
        const card = createGenerationCard(item);
        recentContainer.appendChild(card);
    });
}

// Create generation card element
function createGenerationCard(item) {
    const card = document.createElement('div');
    card.className = 'generation-card';
    
    const date = new Date(item.timestamp);
    const formattedDate = date.toLocaleDateString();
    
    card.innerHTML = `
        <div class="generation-icon-wrapper">
            <svg class="generation-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path>
            </svg>
        </div>
        <div class="generation-info">
            <h3 class="generation-title">${item.mood || 'Generated Track'}</h3>
            <p class="generation-date">${formattedDate}</p>
            ${item.genre ? `<span class="generation-genre">${item.genre}</span>` : ''}
        </div>
    `;
    
    // Add click handler to play audio if available
    if (item.audioUrl) {
        card.style.cursor = 'pointer';
        card.addEventListener('click', () => {
            window.location.href = '/history/';
        });
    }
    
    return card;
}

// Get history from localStorage
function getHistory() {
    try {
        const history = localStorage.getItem('musicHistory');
        return history ? JSON.parse(history) : [];
    } catch (error) {
        console.error('Error loading history:', error);
        return [];
    }
}

// Save to history
function saveToHistory(item) {
    try {
        const history = getHistory();
        history.unshift({
            ...item,
            timestamp: new Date().toISOString()
        });
        
        // Keep only last 50 items
        if (history.length > 50) {
            history.splice(50);
        }
        
        localStorage.setItem('musicHistory', JSON.stringify(history));
    } catch (error) {
        console.error('Error saving to history:', error);
    }
}
// Theme Toggle
const toggleBtn = document.getElementById("themeToggle");
toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
});

// Load Saved Theme
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
}
