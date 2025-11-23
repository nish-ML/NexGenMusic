#!/usr/bin/env python3
"""
Mood Wave Rider Game Integration Script
Automatically integrates the game into premium-dashboard.html
"""

import re
import os

def integrate_game():
    dashboard_file = 'frontend/premium-dashboard.html'
    
    if not os.path.exists(dashboard_file):
        print(f"❌ Error: {dashboard_file} not found!")
        return False
    
    print("📖 Reading dashboard file...")
    with open(dashboard_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already integrated
    if 'openMoodWaveRider' in content:
        print("⚠️  Game already integrated! Skipping...")
        return True
    
    # Step 1: Add CSS link to head
    print("🎨 Adding CSS link...")
    head_pattern = r'(<link[^>]*styles\.css[^>]*>)'
    css_link = r'\1\n    <link rel="stylesheet" href="/static/css/mood-wave-rider.css">'
    content = re.sub(head_pattern, css_link, content, count=1)
    
    # Step 2: Add game card to stats grid
    print("🎮 Adding game card to stats grid...")
    
    # Find the closing </div> of stats-grid
    stats_grid_pattern = r'(<div class="stat-card">\s*<div class="stat-header">\s*<span class="stat-label">Playlists</span>.*?</div>\s*</div>)\s*(</div>)'
    
    game_card = r'''\1

                <!-- MOOD WAVE RIDER GAME CARD -->
                <div class="stat-card game-card" onclick="openMoodWaveRider()" style="cursor: pointer; background: linear-gradient(135deg, rgba(255, 182, 193, 0.2), rgba(100, 255, 218, 0.2)); border: 2px solid rgba(255, 105, 180, 0.3); transition: all 0.3s ease;">
                    <div class="stat-header">
                        <span class="stat-label">Play Mini Game</span>
                        <div class="stat-icon" style="background: linear-gradient(135deg, #FF69B4, #64FFDA); color: white;">🎮</div>
                    </div>
                    <div class="stat-value" style="font-size: 20px; background: linear-gradient(135deg, #FF69B4, #64FFDA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Mood Wave Rider</div>
                    <div class="stat-change" style="color: #FF69B4; font-weight: 600;">👆 Click to play! 🎵</div>
                </div>
            \2'''
    
    content = re.sub(stats_grid_pattern, game_card, content, flags=re.DOTALL)
    
    # Step 3: Add JavaScript functions before </body>
    print("⚙️  Adding JavaScript functions...")
    
    js_code = '''
    <script>
    // Mood Wave Rider Game Modal Functions
    function openMoodWaveRider() {
        const gameModal = document.createElement('div');
        gameModal.id = 'game-modal';
        gameModal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(10px);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease;
        `;

        gameModal.innerHTML = `
            <div style="position: relative; width: 95%; max-width: 1000px; height: 90vh; max-height: 700px;">
                <button onclick="closeMoodWaveRider()" style="
                    position: absolute;
                    top: -50px;
                    right: 0;
                    background: rgba(255, 255, 255, 0.95);
                    border: none;
                    border-radius: 50%;
                    width: 45px;
                    height: 45px;
                    font-size: 28px;
                    cursor: pointer;
                    color: #FF69B4;
                    box-shadow: 0 4px 16px rgba(255, 105, 180, 0.4);
                    transition: all 0.3s ease;
                    z-index: 10001;
                    font-weight: bold;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                " onmouseover="this.style.transform='scale(1.15) rotate(90deg)'; this.style.background='#FF69B4'; this.style.color='white';" onmouseout="this.style.transform='scale(1) rotate(0deg)'; this.style.background='rgba(255, 255, 255, 0.95)'; this.style.color='#FF69B4';">×</button>
                
                <div id="mood-wave-rider" style="height: 100%; margin: 0;">
                    <div class="game-header">
                        <div class="game-title">🎮 Mood Wave Rider</div>
                        <div class="game-controls">
                            <div class="game-score">Score: <span id="score-value">0</span></div>
                        </div>
                    </div>
                    <div class="game-container" style="height: calc(100% - 70px);">
                        <canvas id="game-canvas"></canvas>
                        <div id="game-overlay" class="game-overlay">
                            <div id="menu-screen" class="overlay-content">
                                <div class="overlay-title">🎵 Mood Wave Rider 🎵</div>
                                <div class="overlay-subtitle">Ride the sound wave and avoid the spikes!</div>
                                <button id="start-btn" class="play-btn">▶ Start Game</button>
                                <div class="game-instructions">
                                    <p><strong>Controls:</strong> Arrow Keys or A/D to move</p>
                                    <p><strong>Goal:</strong> Survive as long as possible!</p>
                                    <p><strong>Tip:</strong> The wave pulses with the beat 🎶</p>
                                </div>
                            </div>
                            <div id="countdown-screen" class="overlay-content" style="display: none;">
                                <div class="countdown" id="countdown-number">3</div>
                            </div>
                            <div id="gameover-screen" class="overlay-content game-over-content" style="display: none;">
                                <div class="overlay-title">💥 Game Over! 💥</div>
                                <div class="final-score" id="final-score">0</div>
                                <div class="overlay-subtitle">points survived!</div>
                                <button id="play-again-btn" class="play-btn">🔄 Play Again</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(gameModal);

        if (!document.getElementById('game-css')) {
            const link = document.createElement('link');
            link.id = 'game-css';
            link.rel = 'stylesheet';
            link.href = '/static/css/mood-wave-rider.css';
            document.head.appendChild(link);
        }

        if (!window.MoodWaveRider) {
            const script = document.createElement('script');
            script.src = '/static/js/mood-wave-rider.js';
            script.onload = () => setTimeout(() => {
                if (window.MoodWaveRider) window.currentGame = new MoodWaveRider('mood-wave-rider');
            }, 100);
            document.body.appendChild(script);
        } else {
            setTimeout(() => {
                if (window.MoodWaveRider) window.currentGame = new MoodWaveRider('mood-wave-rider');
            }, 100);
        }
    }

    function closeMoodWaveRider() {
        const modal = document.getElementById('game-modal');
        if (modal) {
            if (window.currentGame && window.currentGame.animationId) {
                cancelAnimationFrame(window.currentGame.animationId);
                window.currentGame = null;
            }
            modal.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => modal.remove(), 300);
        }
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeMoodWaveRider();
    });

    const gameStyle = document.createElement('style');
    gameStyle.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        @keyframes fadeOut {
            from { opacity: 1; transform: scale(1); }
            to { opacity: 0; transform: scale(0.95); }
        }
        .game-card:hover {
            transform: translateY(-6px) scale(1.03) !important;
            box-shadow: 0 12px 32px rgba(255, 105, 180, 0.4) !important;
        }
        .game-card:active {
            transform: translateY(-4px) scale(1.01) !important;
        }
    `;
    document.head.appendChild(gameStyle);
    </script>
'''
    
    # Insert before closing </body>
    content = content.replace('</body>', js_code + '\n</body>')
    
    # Step 4: Write back to file
    print("💾 Saving changes...")
    with open(dashboard_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Integration complete!")
    print("\n📋 What was added:")
    print("   1. CSS link in <head>")
    print("   2. Game card in stats grid (5th card)")
    print("   3. JavaScript modal functions")
    print("\n🎮 Test it:")
    print("   1. Open your dashboard")
    print("   2. Click the 'Mood Wave Rider' card")
    print("   3. Play the game!")
    
    return True

if __name__ == '__main__':
    print("🎮 Mood Wave Rider - Dashboard Integration")
    print("=" * 50)
    integrate_game()
