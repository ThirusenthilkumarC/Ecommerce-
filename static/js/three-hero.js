/**
 * NEXUS ELECTRONICS — PROCEDURAL 3D HERO SHOWCASE
 * High-performance WebGL scene featuring floating flagship gadgets, ambient glow rings,
 * dynamic neon rim lighting, and smooth mouse/touch parallax.
 */

(function() {
  const container = document.getElementById('hero3dContainer');
  if (!container) return;

  if (typeof THREE === 'undefined') {
    container.classList.add('webgl-fallback-active');
    return;
  }

  try {
    // 1. Scene, Camera & Renderer Setup
    const scene = new THREE.Scene();
    const width = container.clientWidth || 540;
    const height = container.clientHeight || 480;

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 0, 7.8);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    const isMobile = window.innerWidth <= 768;
    renderer.setPixelRatio(isMobile ? 1 : Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.35;
    renderer.domElement.className = 'three-canvas';
    container.appendChild(renderer.domElement);

    // Hide fallback image smoothly once canvas is mounted
    container.classList.add('canvas-loaded');

    // 2. Lighting System (Dual Neon Violet & Cyan Rim Lights)
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);

    const violetLight = new THREE.PointLight(0x8B5CF6, 4.0, 22);
    violetLight.position.set(-5, 4, 3.5);
    scene.add(violetLight);

    const cyanLight = new THREE.PointLight(0x06B6D4, 3.8, 22);
    cyanLight.position.set(5, -3, 3.5);
    scene.add(cyanLight);

    const topKeyLight = new THREE.DirectionalLight(0xffffff, 1.4);
    topKeyLight.position.set(0, 8, 5);
    scene.add(topKeyLight);

    // 3. Materials
    const titaniumMaterial = new THREE.MeshStandardMaterial({
      color: 0x181824,
      metalness: 0.9,
      roughness: 0.2,
    });

    const screenMaterial = new THREE.MeshStandardMaterial({
      color: 0x05050A,
      roughness: 0.08,
      metalness: 0.92,
    });

    const neonCyanMaterial = new THREE.MeshBasicMaterial({ color: 0x06B6D4 });
    const neonVioletMaterial = new THREE.MeshBasicMaterial({ color: 0x8B5CF6 });

    // 4. Procedural Flagship Smartphone (Floating Hero)
    const phoneGroup = new THREE.Group();
    
    // Body Chassis
    const bodyGeo = new THREE.BoxGeometry(2.2, 4.5, 0.22);
    const phoneBody = new THREE.Mesh(bodyGeo, titaniumMaterial);
    phoneGroup.add(phoneBody);

    // Front Screen Glass
    const screenGeo = new THREE.PlaneGeometry(2.05, 4.35);
    const phoneScreen = new THREE.Mesh(screenGeo, screenMaterial);
    phoneScreen.position.z = 0.12;
    phoneGroup.add(phoneScreen);

    // Screen Border Glowing Wireframe
    const edgeGeo = new THREE.EdgesGeometry(screenGeo);
    const edgeLine = new THREE.LineSegments(edgeGeo, new THREE.LineBasicMaterial({ color: 0x8B5CF6, transparent: true, opacity: 0.7 }));
    edgeLine.position.z = 0.125;
    phoneGroup.add(edgeLine);

    // Camera Module (Back)
    const camBumpGeo = new THREE.BoxGeometry(0.9, 0.9, 0.08);
    const camBump = new THREE.Mesh(camBumpGeo, titaniumMaterial);
    camBump.position.set(-0.55, 1.55, -0.14);
    phoneGroup.add(camBump);

    // Triple Camera Glass Lenses
    for (let i = 0; i < 3; i++) {
      const lensGeo = new THREE.CylinderGeometry(0.18, 0.18, 0.05, 20);
      lensGeo.rotateX(Math.PI / 2);
      const lens = new THREE.Mesh(lensGeo, new THREE.MeshStandardMaterial({ color: 0x080812, roughness: 0.05, metalness: 0.98 }));
      lens.position.set(-0.55 + (i % 2) * 0.42 - 0.21, 1.55 + (Math.floor(i / 2)) * 0.42 - 0.21, -0.18);
      phoneGroup.add(lens);
    }

    phoneGroup.position.set(0.4, 0.15, 0);
    phoneGroup.rotation.set(0.15, -0.32, 0.06);
    scene.add(phoneGroup);

    // 5. Cyber Ambient Glow Rings (Torus)
    const ring1Geo = new THREE.TorusGeometry(3.4, 0.02, 16, 90);
    const ring1 = new THREE.Mesh(ring1Geo, neonVioletMaterial);
    ring1.rotation.x = Math.PI / 2.6;
    scene.add(ring1);

    const ring2Geo = new THREE.TorusGeometry(2.6, 0.016, 16, 90);
    const ring2 = new THREE.Mesh(ring2Geo, neonCyanMaterial);
    ring2.rotation.y = Math.PI / 3;
    scene.add(ring2);

    // 6. Ambient Floating Glowing Particle Field
    const particleCount = isMobile ? 35 : 90;
    const particleGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const cViolet = new THREE.Color(0x8B5CF6);
    const cCyan = new THREE.Color(0x06B6D4);

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 12;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 8;

      const chosenColor = Math.random() > 0.5 ? cViolet : cCyan;
      colors[i * 3] = chosenColor.r;
      colors[i * 3 + 1] = chosenColor.g;
      colors[i * 3 + 2] = chosenColor.b;
    }

    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particleMat = new THREE.PointsMaterial({
      size: 0.08,
      vertexColors: true,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending
    });

    const particleField = new THREE.Points(particleGeo, particleMat);
    scene.add(particleField);

    // 7. Mouse & Touch Parallax Tracking
    let targetMouseX = 0;
    let targetMouseY = 0;
    let mouseX = 0;
    let mouseY = 0;

    window.addEventListener('mousemove', (e) => {
      targetMouseX = (e.clientX / window.innerWidth - 0.5) * 1.5;
      targetMouseY = (e.clientY / window.innerHeight - 0.5) * 1.5;
    }, { passive: true });

    // 8. Lifecycle & Intersection Observer (Zero GPU usage off-screen)
    let isVisible = true;
    let animationFrameId = null;
    const clock = new THREE.Clock();

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        isVisible = entry.isIntersecting;
        if (isVisible && !animationFrameId) {
          animate();
        }
      });
    }, { threshold: 0.1 });

    observer.observe(container);

    // 9. Animation Render Loop
    const animate = () => {
      if (!isVisible) {
        animationFrameId = null;
        return;
      }

      const elapsedTime = clock.getElapsedTime();

      // Smooth Lerp Mouse Parallax
      mouseX += (targetMouseX - mouseX) * 0.05;
      mouseY += (targetMouseY - mouseY) * 0.05;

      // Floating Gadget Movement
      phoneGroup.position.y = 0.15 + Math.sin(elapsedTime * 1.2) * 0.15;
      phoneGroup.rotation.y = -0.32 + mouseX * 0.45 + Math.sin(elapsedTime * 0.6) * 0.08;
      phoneGroup.rotation.x = 0.15 - mouseY * 0.35 + Math.cos(elapsedTime * 0.8) * 0.05;

      // Ambient Ring Rotations
      ring1.rotation.z = elapsedTime * 0.15;
      ring2.rotation.x = Math.PI / 3 + elapsedTime * 0.2;

      // Particle Swirl
      particleField.rotation.y = elapsedTime * 0.04;
      particleField.rotation.x = elapsedTime * 0.02;

      renderer.render(scene, camera);
      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    // 10. Responsive Canvas Resize Listener
    const onResize = () => {
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight;
      if (newWidth === 0 || newHeight === 0) return;

      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', onResize);

  } catch (err) {
    console.warn("WebGL initialization note:", err);
    container.classList.add('webgl-fallback-active');
  }
})();
