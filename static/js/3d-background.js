// ========== ULTRA-PREMIUM 3D SCENE ==========
let scene, camera, renderer;
let peacock, deer, birds = [];
let emojis = [];
let waveform;
let mouse = { x: 0, y: 0 };
let isLiteMode = false;
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
    directionalLight1.shadow.mapSize.width = 2048;
    directionalLight1.shadow.mapSize.height = 2048;
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
