// Mood Wave Rider Game - NexGenMusic
class MoodWaveRider {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Game state
        this.gameState = 'menu'; // menu, countdown, playing, gameover
        this.score = 0;
        this.startTime = 0;
        this.animationId = null;
        
        // Canvas setup
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
        
        // Player
        this.player = {
            x: 100,
            y: 0,
            radius: 15,
            targetX: 100,
            speed: 8,
            color: '#FF69B4',
            glow: 0
        };
        
        // Wave properties
        this.wave = {
            amplitude: 40,
            frequency: 0.02,
            speed: 2,
            offset: 0,
            baseY: this.canvas.height / 2,
            beatPulse: 0,
            beatInterval: 700,
            lastBeat: 0
        };
        
        // Spikes
        this.spikes = [];
        this.spikeSpawnInterval = 2000;
        this.lastSpikeSpawn = 0;
        
        // Controls
        this.keys = {};
        this.setupControls();
        
        // Floating emojis
        this.emojis = ['🎵', '✨', '🎶', '💫'];
        this.floatingEmojis = [];
        this.createFloatingEmojis();
        
        // Start animation loop
        this.animate();
    }
    
    resizeCanvas() {
        const rect = this.canvas.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
        this.wave.baseY = this.canvas.height / 2;
    }
    
    setupControls() {
        document.addEventListener('keydown', (e) => {
            this.keys[e.key] = true;
            if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {
                e.preventDefault();
            }
            if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {
                e.preventDefault();
            }
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.key] = false;
        });
    }
    
    createFloatingEmojis() {
        for (let i = 0; i < 6; i++) {
            this.floatingEmojis.push({
                emoji: this.emojis[Math.floor(Math.random() * this.emojis.length)],
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                speed: 0.3 + Math.random() * 0.5,
                offset: Math.random() * Math.PI * 2
            });
        }
    }
    
    // Simulate beat detection (can be replaced with real BPM from backend)
    simulateBeat(currentTime) {
        if (currentTime - this.wave.lastBeat > this.wave.beatInterval) {
            this.wave.lastBeat = currentTime;
            this.wave.beatPulse = 1;
            // Vary beat interval slightly for natural feel
            this.wave.beatInterval = 600 + Math.random() * 300;
        }
        // Decay beat pulse
        this.wave.beatPulse *= 0.9;
    }
    
    getWaveY(x, time) {
        const baseWave = Math.sin(x * this.wave.frequency + this.wave.offset);
        const beatEffect = this.wave.beatPulse * 20;
        return this.wave.baseY + (baseWave * this.wave.amplitude) + beatEffect;
    }
    
    drawWave(time) {
        const gradient = this.ctx.createLinearGradient(0, 0, this.canvas.width, 0);
        gradient.addColorStop(0, 'rgba(255, 105, 180, 0.8)');
        gradient.addColorStop(0.5, 'rgba(100, 255, 218, 0.8)');
        gradient.addColorStop(1, 'rgba(0, 206, 209, 0.8)');
        
        // Glow effect
        this.ctx.shadowBlur = 20 + this.wave.beatPulse * 10;
        this.ctx.shadowColor = 'rgba(255, 105, 180, 0.6)';
        
        // Draw wave
        this.ctx.beginPath();
        this.ctx.lineWidth = 4;
        this.ctx.strokeStyle = gradient;
        
        for (let x = 0; x < this.canvas.width; x += 2) {
            const y = this.getWaveY(x, time);
            if (x === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
        }
        
        this.ctx.stroke();
        this.ctx.shadowBlur = 0;
        
        // Update wave offset
        this.wave.offset += this.wave.speed * 0.05;
    }
    
    drawPlayer() {
        // Update player position on wave
        this.player.y = this.getWaveY(this.player.x, Date.now());
        
        // Smooth movement
        const dx = this.player.targetX - this.player.x;
        this.player.x += dx * 0.15;
        
        // Glow animation
        this.player.glow = Math.sin(Date.now() * 0.005) * 0.5 + 0.5;
        
        // Draw glow
        const glowGradient = this.ctx.createRadialGradient(
            this.player.x, this.player.y, 0,
            this.player.x, this.player.y, this.player.radius * 3
        );
        glowGradient.addColorStop(0, `rgba(255, 105, 180, ${0.6 * this.player.glow})`);
        glowGradient.addColorStop(1, 'rgba(255, 105, 180, 0)');
        
        this.ctx.fillStyle = glowGradient;
        this.ctx.beginPath();
        this.ctx.arc(this.player.x, this.player.y, this.player.radius * 3, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Draw player
        const playerGradient = this.ctx.createRadialGradient(
            this.player.x, this.player.y, 0,
            this.player.x, this.player.y, this.player.radius
        );
        playerGradient.addColorStop(0, '#FFB6C1');
        playerGradient.addColorStop(1, '#FF69B4');
        
        this.ctx.fillStyle = playerGradient;
        this.ctx.beginPath();
        this.ctx.arc(this.player.x, this.player.y, this.player.radius, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Draw emoji on player
        this.ctx.font = '20px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText('🎧', this.player.x, this.player.y);
    }
    
    spawnSpike(time) {
        if (time - this.lastSpikeSpawn > this.spikeSpawnInterval) {
            this.lastSpikeSpawn = time;
            
            // Random position but not too close to edges
            const minX = this.canvas.width * 0.7;
            const maxX = this.canvas.width * 0.9;
            const x = minX + Math.random() * (maxX - minX);
            
            this.spikes.push({
                x: x,
                y: this.getWaveY(x, time),
                size: 20,
                speed: 3,
                color: '#FF1493',
                glow: 1
            });
            
            // Vary spawn interval
            this.spikeSpawnInterval = 1500 + Math.random() * 1500;
        }
    }
    
    updateSpikes(time) {
        this.spikes.forEach((spike, index) => {
            // Move spike left
            spike.x -= spike.speed;
            spike.y = this.getWaveY(spike.x, time);
            
            // Remove if off screen
            if (spike.x < -50) {
                this.spikes.splice(index, 1);
            }
            
            // Pulse glow
            spike.glow = Math.sin(time * 0.01) * 0.3 + 0.7;
        });
    }
    
    drawSpikes() {
        this.spikes.forEach(spike => {
            // Glow
            this.ctx.shadowBlur = 15 * spike.glow;
            this.ctx.shadowColor = spike.color;
            
            // Draw triangle spike
            this.ctx.fillStyle = spike.color;
            this.ctx.beginPath();
            this.ctx.moveTo(spike.x, spike.y - spike.size);
            this.ctx.lineTo(spike.x - spike.size / 2, spike.y + spike.size / 2);
            this.ctx.lineTo(spike.x + spike.size / 2, spike.y + spike.size / 2);
            this.ctx.closePath();
            this.ctx.fill();
            
            this.ctx.shadowBlur = 0;
        });
    }
    
    checkCollisions() {
        for (let spike of this.spikes) {
            const dx = this.player.x - spike.x;
            const dy = this.player.y - spike.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < this.player.radius + spike.size / 2) {
                this.gameOver();
                return true;
            }
        }
        return false;
    }
    
    updatePlayerMovement() {
        if (this.keys['ArrowLeft'] || this.keys['a'] || this.keys['A']) {
            this.player.targetX = Math.max(50, this.player.targetX - this.player.speed);
        }
        if (this.keys['ArrowRight'] || this.keys['d'] || this.keys['D']) {
            this.player.targetX = Math.min(this.canvas.width - 50, this.player.targetX + this.player.speed);
        }
    }
    
    drawFloatingEmojis(time) {
        this.ctx.font = '24px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        
        this.floatingEmojis.forEach(item => {
            const floatY = item.y + Math.sin(time * 0.001 * item.speed + item.offset) * 15;
            this.ctx.globalAlpha = 0.4;
            this.ctx.fillText(item.emoji, item.x, floatY);
            this.ctx.globalAlpha = 1;
        });
    }
    
    updateScore() {
        if (this.gameState === 'playing') {
            this.score = Math.floor((Date.now() - this.startTime) / 100);
            document.getElementById('score-value').textContent = this.score;
        }
    }
    
    animate() {
        const time = Date.now();
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw floating emojis
        this.drawFloatingEmojis(time);
        
        if (this.gameState === 'playing') {
            // Simulate beat
            this.simulateBeat(time);
            
            // Draw wave
            this.drawWave(time);
            
            // Update and draw spikes
            this.spawnSpike(time);
            this.updateSpikes(time);
            this.drawSpikes();
            
            // Update player
            this.updatePlayerMovement();
            this.drawPlayer();
            
            // Check collisions
            this.checkCollisions();
            
            // Update score
            this.updateScore();
        } else {
            // Just draw wave when not playing
            this.simulateBeat(time);
            this.drawWave(time);
        }
        
        this.animationId = requestAnimationFrame(() => this.animate());
    }
    
    startGame() {
        document.getElementById('game-overlay').classList.remove('hidden');
        document.getElementById('menu-screen').style.display = 'none';
        document.getElementById('countdown-screen').style.display = 'flex';
        
        let count = 3;
        const countdownEl = document.getElementById('countdown-number');
        countdownEl.textContent = count;
        
        const countdownInterval = setInterval(() => {
            count--;
            if (count > 0) {
                countdownEl.textContent = count;
            } else {
                clearInterval(countdownInterval);
                document.getElementById('game-overlay').classList.add('hidden');
                this.gameState = 'playing';
                this.score = 0;
                this.startTime = Date.now();
                this.spikes = [];
                this.lastSpikeSpawn = Date.now();
                this.player.x = 100;
                this.player.targetX = 100;
            }
        }, 1000);
    }
    
    gameOver() {
        this.gameState = 'gameover';
        document.getElementById('game-overlay').classList.remove('hidden');
        document.getElementById('countdown-screen').style.display = 'none';
        document.getElementById('gameover-screen').style.display = 'flex';
        document.getElementById('final-score').textContent = this.score;
    }
    
    resetGame() {
        this.gameState = 'menu';
        document.getElementById('game-overlay').classList.remove('hidden');
        document.getElementById('gameover-screen').style.display = 'none';
        document.getElementById('menu-screen').style.display = 'flex';
        this.score = 0;
        this.spikes = [];
        document.getElementById('score-value').textContent = '0';
    }
}

// Game initialization and button handlers are now in the HTML file
// This allows for more flexible initialization

// BACKEND INTEGRATION NOTES:
// =============================
// To integrate real BPM detection from your music generation:
//
// 1. Replace simulateBeat() with real beat data:
//    - Fetch BPM from your audio analysis endpoint
//    - Calculate beat interval: beatInterval = 60000 / BPM
//    - Update wave.beatPulse on actual beats
//
// 2. Example integration:
//    async fetchBPM() {
//        const response = await fetch('/api/current-track-bpm/');
//        const data = await response.json();
//        this.wave.beatInterval = 60000 / data.bpm;
//    }
//
// 3. For real-time audio sync:
//    - Use Web Audio API to analyze playing track
//    - Detect beats using frequency analysis
//    - Trigger wave.beatPulse on detected beats
