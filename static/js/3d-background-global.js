// Simple 3D Background Animation for Global Use
(function() {
    'use strict';
    
    // Check if Three.js is loaded
    if (typeof THREE === 'undefined') {
        console.warn('Three.js not loaded, skipping 3D background');
        return;
    }
    
    // Check if canvas exists
    const canvas = document.getElementById('canvas3d');
    if (!canvas) {
        console.warn('Canvas element not found');
        return;
    }
    
    let scene, camera, renderer;
    let particles = [];
    let animationId;
    
    function init() {
        // Scene
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xe0e7ff);
        
        // Camera
        camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        camera.position.z = 5;
        
        // Renderer
        renderer = new THREE.WebGLRenderer({ 
            canvas: canvas,
            antialias: true,
            alpha: true 
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        
        // Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 5, 5);
        scene.add(directionalLight);
        
        // Create particles
        createParticles();
        
        // Handle resize
        window.addEventListener('resize', onWindowResize);
        
        // Start animation
        animate();
        
        console.log('✅ 3D Background initialized');
    }
    
    function createParticles() {
        const geometry = new THREE.BufferGeometry();
        const particleCount = 100;
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        
        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 10;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 10;
            
            const color = new THREE.Color();
            color.setHSL(Math.random() * 0.3 + 0.5, 0.7, 0.7);
            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;
        }
        
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        
        const material = new THREE.PointsMaterial({
            size: 0.1,
            vertexColors: true,
            transparent: true,
            opacity: 0.6
        });
        
        const points = new THREE.Points(geometry, material);
        scene.add(points);
        particles.push(points);
    }
    
    function onWindowResize() {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }
    
    function animate() {
        animationId = requestAnimationFrame(animate);
        
        // Rotate particles
        particles.forEach(particle => {
            particle.rotation.y += 0.001;
            particle.rotation.x += 0.0005;
        });
        
        renderer.render(scene, camera);
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
