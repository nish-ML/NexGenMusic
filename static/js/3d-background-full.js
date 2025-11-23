// ========== FULL 3D SCENE WITH ANIMALS ==========
(function() {
    let scene, camera, renderer;
    let peacock, deer, birds = [];
    let emojis = [];
    let waveform;
    let particles = [];
    let mouse = { x: 0, y: 0 };
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function init3DScene() {
        const canvas = document.getElementById('canvas3d');
        if (!canvas) return;
        
        // Scene
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xe0e7ff);
        scene.fog = new THREE.Fog(0xe0e7ff, 20, 60);

        // Camera
        camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 4, 18);
        camera.lookAt(0, 2, 0);

        // Renderer
        renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;

        // Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);

        const directionalLight1 = new THREE.DirectionalLight(0xa5b4fc, 1.2);
        directionalLight1.position.set(10, 15, 10);
        directionalLight1.castShadow = true;
        scene.add(directionalLight1);

        const directionalLight2 = new THREE.DirectionalLight(0xfae8ff, 0.8);
        directionalLight2.position.set(-10, 10, -5);
        scene.add(directionalLight2);

        const pointLight = new THREE.PointLight(0xd1fae5, 0.6, 50);
        pointLight.position.set(0, 8, 5);
        scene.add(pointLight);

        // Create scene elements
        createGround();
        createPeacock();
        createDeer();
        createBirds();
        createFloatingEmojis();
        createWaveform();
        createParticles();

        // Event listeners
        window.addEventListener('resize', onWindowResize);
        window.addEventListener('mousemove', onMouseMove);

        // Start animation
        animate();
    }

    function createGround() {
        const groundGeometry = new THREE.PlaneGeometry(100, 100);
        const groundMaterial = new THREE.MeshStandardMaterial({
            color: 0xdbeafe,
            roughness: 0.8,
            metalness: 0.1
        });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = 0;
        ground.receiveShadow = true;
        scene.add(ground);
    }

    function createPeacock() {
        const peacockGroup = new THREE.Group();

        // Body
        const bodyGeometry = new THREE.SphereGeometry(0.8, 20, 20);
        const bodyMaterial = new THREE.MeshStandardMaterial({
            color: 0xa5b4fc,
            roughness: 0.3,
            metalness: 0.2
        });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        body.scale.set(1, 1.3, 0.9);
        body.castShadow = true;
        peacockGroup.add(body);

        // Head
        const headGeometry = new THREE.SphereGeometry(0.45, 16, 16);
        const headMaterial = new THREE.MeshStandardMaterial({ color: 0xc7d2fe });
        const head = new THREE.Mesh(headGeometry, headMaterial);
        head.position.set(0, 1, 0.4);
        head.castShadow = true;
        peacockGroup.add(head);

        // Beak
        const beakGeometry = new THREE.ConeGeometry(0.1, 0.25, 8);
        const beakMaterial = new THREE.MeshStandardMaterial({ color: 0xfbbf24 });
        const beak = new THREE.Mesh(beakGeometry, beakMaterial);
        beak.position.set(0, 1, 0.75);
        beak.rotation.x = Math.PI / 2;
        peacockGroup.add(beak);

        // Eyes
        const eyeGeometry = new THREE.SphereGeometry(0.1, 8, 8);
        const eyeMaterial = new THREE.MeshStandardMaterial({ color: 0x1e293b });
        const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        leftEye.position.set(-0.2, 1.1, 0.65);
        const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        rightEye.position.set(0.2, 1.1, 0.65);
        peacockGroup.add(leftEye, rightEye);

        // Tail feathers
        const featherGroup = new THREE.Group();
        for (let i = 0; i < 11; i++) {
            const angle = (i - 5) * 0.22;
            const featherGeometry = new THREE.PlaneGeometry(0.5, 2);
            const featherMaterial = new THREE.MeshStandardMaterial({
                color: i % 2 === 0 ? 0x6366f1 : 0xa855f7,
                side: THREE.DoubleSide,
                emissive: i % 2 === 0 ? 0x6366f1 : 0xa855f7,
                emissiveIntensity: 0.4,
                transparent: true,
                opacity: 0.95
            });
            const feather = new THREE.Mesh(featherGeometry, featherMaterial);
            feather.position.set(Math.sin(angle) * 1.2, 0.8, -0.6 + Math.cos(angle) * 0.4);
            feather.rotation.y = angle;
            featherGroup.add(feather);
        }
        peacockGroup.add(featherGroup);
        peacockGroup.userData.feathers = featherGroup;

        peacockGroup.position.set(-10, 0.8, 2);
        peacockGroup.userData.baseY = 0.8;
        peacockGroup.userData.time = 0;
        peacockGroup.scale.set(1.8, 1.8, 1.8);
        
        scene.add(peacockGroup);
        peacock = peacockGroup;
    }

    function createDeer() {
        const deerGroup = new THREE.Group();

        // Body
        const bodyGeometry = new THREE.BoxGeometry(1, 0.8, 1.5);
        const bodyMaterial = new THREE.MeshStandardMaterial({
            color: 0xfed7aa,
            roughness: 0.5
        });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        body.castShadow = true;
        deerGroup.add(body);

        // Head
        const headGeometry = new THREE.BoxGeometry(0.6, 0.6, 0.8);
        const head = new THREE.Mesh(headGeometry, bodyMaterial);
        head.position.set(0, 0.5, 1);
        head.castShadow = true;
        deerGroup.add(head);

        // Snout
        const snoutGeometry = new THREE.BoxGeometry(0.4, 0.25, 0.4);
        const snout = new THREE.Mesh(snoutGeometry, bodyMaterial);
        snout.position.set(0, 0.4, 1.5);
        deerGroup.add(snout);

        // Nose
        const noseGeometry = new THREE.SphereGeometry(0.1, 8, 8);
        const noseMaterial = new THREE.MeshStandardMaterial({ color: 0x1e293b });
        const nose = new THREE.Mesh(noseGeometry, noseMaterial);
        nose.position.set(0, 0.4, 1.7);
        deerGroup.add(nose);

        // Eyes
        const eyeGeometry = new THREE.SphereGeometry(0.12, 8, 8);
        const eyeMaterial = new THREE.MeshStandardMaterial({ color: 0x1e293b });
        const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        leftEye.position.set(-0.2, 0.6, 1.3);
        const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        rightEye.position.set(0.2, 0.6, 1.3);
        deerGroup.add(leftEye, rightEye);

        // Ears
        const earGeometry = new THREE.ConeGeometry(0.2, 0.5, 8);
        const leftEar = new THREE.Mesh(earGeometry, bodyMaterial);
        leftEar.position.set(-0.3, 0.9, 1);
        leftEar.rotation.z = -0.3;
        const rightEar = new THREE.Mesh(earGeometry, bodyMaterial);
        rightEar.position.set(0.3, 0.9, 1);
        rightEar.rotation.z = 0.3;
        deerGroup.add(leftEar, rightEar);
        deerGroup.userData.ears = [leftEar, rightEar];

        // Antlers
        const antlerMaterial = new THREE.MeshStandardMaterial({ color: 0x92400e });
        const antlerGeometry = new THREE.CylinderGeometry(0.04, 0.06, 0.6, 8);
        const leftAntler = new THREE.Mesh(antlerGeometry, antlerMaterial);
        leftAntler.position.set(-0.25, 1.1, 0.9);
        const rightAntler = new THREE.Mesh(antlerGeometry, antlerMaterial);
        rightAntler.position.set(0.25, 1.1, 0.9);
        deerGroup.add(leftAntler, rightAntler);

        // Legs
        const legGeometry = new THREE.CylinderGeometry(0.1, 0.1, 0.8, 8);
        const positions = [[-0.4, -0.8, 0.5], [0.4, -0.8, 0.5], [-0.4, -0.8, -0.5], [0.4, -0.8, -0.5]];
        positions.forEach(pos => {
            const leg = new THREE.Mesh(legGeometry, bodyMaterial);
            leg.position.set(...pos);
            leg.castShadow = true;
            deerGroup.add(leg);
        });

        deerGroup.position.set(10, 1.2, 2);
        deerGroup.userData.baseY = 1.2;
        deerGroup.userData.time = 0;
        deerGroup.scale.set(1.5, 1.5, 1.5);
        
        scene.add(deerGroup);
        deer = deerGroup;
    }

    function createBirds() {
        const colors = [0x93c5fd, 0xbfdbfe, 0xdbeafe];
        for (let i = 0; i < 5; i++) {
            const birdGroup = new THREE.Group();

            // Body
            const bodyGeometry = new THREE.SphereGeometry(0.2, 12, 12);
            const bodyMaterial = new THREE.MeshStandardMaterial({
                color: colors[i % 3],
                roughness: 0.4
            });
            const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
            body.scale.set(1, 0.8, 1.2);
            body.castShadow = true;
            birdGroup.add(body);

            // Head
            const headGeometry = new THREE.SphereGeometry(0.12, 12, 12);
            const head = new THREE.Mesh(headGeometry, bodyMaterial);
            head.position.set(0, 0.15, 0.2);
            birdGroup.add(head);

            // Beak
            const beakGeometry = new THREE.ConeGeometry(0.04, 0.1, 6);
            const beakMaterial = new THREE.MeshStandardMaterial({ color: 0xfbbf24 });
            const beak = new THREE.Mesh(beakGeometry, beakMaterial);
            beak.position.set(0, 0.15, 0.32);
            beak.rotation.x = Math.PI / 2;
            birdGroup.add(beak);

            // Wings
            const wingGeometry = new THREE.BoxGeometry(0.4, 0.05, 0.2);
            const leftWing = new THREE.Mesh(wingGeometry, bodyMaterial);
            leftWing.position.set(-0.25, 0, 0);
            const rightWing = new THREE.Mesh(wingGeometry, bodyMaterial);
            rightWing.position.set(0.25, 0, 0);
            birdGroup.add(leftWing, rightWing);
            birdGroup.userData.wings = [leftWing, rightWing];

            // Position in circular path
            const angle = (i / 5) * Math.PI * 2;
            const radius = 8;
            birdGroup.position.set(
                Math.cos(angle) * radius,
                5 + Math.sin(i) * 2,
                Math.sin(angle) * radius
            );
            birdGroup.userData.angle = angle;
            birdGroup.userData.radius = radius;
            birdGroup.userData.time = i * 0.5;

            scene.add(birdGroup);
            birds.push(birdGroup);
        }
    }

    function createFloatingEmojis() {
        const colors = [0xfbbf24, 0xec4899, 0xa855f7, 0x6366f1, 0x10b981, 0xf59e0b, 0x8b5cf6];

        for (let i = 0; i < 30; i++) {
            const emojiGroup = new THREE.Group();
            
            const geometry = new THREE.SphereGeometry(0.3, 16, 16);
            const material = new THREE.MeshStandardMaterial({
                color: colors[i % colors.length],
                emissive: colors[i % colors.length],
                emissiveIntensity: 0.4,
                transparent: true,
                opacity: 0.8
            });
            const emoji = new THREE.Mesh(geometry, material);
            emojiGroup.add(emoji);

            emojiGroup.position.set(
                (Math.random() - 0.5) * 30,
                Math.random() * 10 + 2,
                Math.random() * 15 + 5
            );
            emojiGroup.userData.baseY = emojiGroup.position.y;
            emojiGroup.userData.speed = 0.5 + Math.random() * 0.5;
            emojiGroup.userData.time = Math.random() * Math.PI * 2;

            scene.add(emojiGroup);
            emojis.push(emojiGroup);
        }
    }

    function createWaveform() {
        const waveformGroup = new THREE.Group();
        const barCount = 20;
        const bars = [];

        for (let i = 0; i < barCount; i++) {
            const height = 1 + Math.random() * 3;
            const geometry = new THREE.BoxGeometry(0.3, height, 0.3);
            const material = new THREE.MeshStandardMaterial({
                color: 0x6366f1,
                emissive: 0x6366f1,
                emissiveIntensity: 0.5,
                transparent: true,
                opacity: 0.8
            });
            const bar = new THREE.Mesh(geometry, material);
            bar.position.set((i - barCount / 2) * 0.5, height / 2, 0);
            bar.userData.baseHeight = height;
            waveformGroup.add(bar);
            bars.push(bar);
        }

        waveformGroup.position.set(0, 0, -10);
        waveformGroup.userData.bars = bars;
        scene.add(waveformGroup);
        waveform = waveformGroup;
    }

    function createParticles() {
        const particleCount = 200;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 50;
            positions[i * 3 + 1] = Math.random() * 20;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 50;

            const color = new THREE.Color();
            color.setHSL(Math.random() * 0.3 + 0.5, 0.7, 0.7);
            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 0.15,
            vertexColors: true,
            transparent: true,
            opacity: 0.6,
            blending: THREE.AdditiveBlending
        });

        const particleSystem = new THREE.Points(geometry, material);
        scene.add(particleSystem);
        particles.push(particleSystem);
    }

    function onMouseMove(event) {
        mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

        if (!prefersReducedMotion) {
            camera.position.x = mouse.x * 2;
            camera.position.y = 5 + mouse.y * 1;
            camera.lookAt(0, 3, 0);
        }
    }

    function onWindowResize() {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }

    function animate() {
        requestAnimationFrame(animate);

        const time = Date.now() * 0.001;

        if (!prefersReducedMotion) {
            // Peacock animation
            if (peacock) {
                peacock.userData.time += 0.01;
                peacock.position.y = peacock.userData.baseY + Math.sin(peacock.userData.time) * 0.2;
                peacock.rotation.y = Math.sin(peacock.userData.time * 0.5) * 0.3;
                
                if (peacock.userData.feathers) {
                    peacock.userData.feathers.rotation.y = Math.sin(time * 0.8) * 0.2;
                }
            }

            // Deer animation
            if (deer) {
                deer.userData.time += 0.01;
                deer.rotation.x = Math.sin(deer.userData.time * 2) * 0.05;
                deer.position.y = deer.userData.baseY + Math.sin(deer.userData.time) * 0.1;
            }

            // Birds animation
            birds.forEach((bird, i) => {
                bird.userData.time += 0.01;
                bird.userData.angle += 0.005;
                bird.position.x = Math.cos(bird.userData.angle) * bird.userData.radius;
                bird.position.z = Math.sin(bird.userData.angle) * bird.userData.radius;
                bird.position.y = 5 + Math.sin(bird.userData.time * 2) * 1;
                bird.lookAt(
                    Math.cos(bird.userData.angle + 0.1) * bird.userData.radius,
                    bird.position.y,
                    Math.sin(bird.userData.angle + 0.1) * bird.userData.radius
                );

                if (bird.userData.wings) {
                    const flapAngle = Math.sin(time * 10 + i) * 0.5;
                    bird.userData.wings[0].rotation.z = flapAngle;
                    bird.userData.wings[1].rotation.z = -flapAngle;
                }
            });

            // Emojis animation
            emojis.forEach((emoji) => {
                emoji.userData.time += emoji.userData.speed * 0.01;
                emoji.position.y = emoji.userData.baseY + Math.sin(emoji.userData.time) * 0.5;
                emoji.rotation.y += 0.02;
                emoji.rotation.x = Math.sin(emoji.userData.time * 0.5) * 0.3;
            });

            // Waveform animation
            if (waveform && waveform.userData.bars) {
                waveform.userData.bars.forEach((bar, i) => {
                    bar.scale.y = 1 + Math.sin(time * 2 + i * 0.3) * 0.2;
                });
            }

            // Particles rotation
            particles.forEach(p => {
                p.rotation.y += 0.001;
            });
        }

        renderer.render(scene, camera);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init3DScene);
    } else {
        init3DScene();
    }
})();
