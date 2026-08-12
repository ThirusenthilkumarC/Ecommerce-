/**
 * NEXUS ELECTRONICS — "EXPLORE THE FUTURE" 3D PRODUCT SHOWROOM
 * 360° Drag-to-Rotate WebGL viewer with OrbitControls and 5 interactive pulsing hotspots.
 */

(function() {
  const container = document.getElementById('showroomCanvasContainer');
  if (!container) return;

  if (typeof THREE === 'undefined') {
    container.classList.add('webgl-fallback-active');
    return;
  }

  try {
    // 1. Scene, Camera & Renderer
    const scene = new THREE.Scene();
    const width = container.clientWidth || 600;
    const height = container.clientHeight || 480;

    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(0, 0, 7.5);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    const isMobile = window.innerWidth <= 768;
    renderer.setPixelRatio(isMobile ? 1 : Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.35;
    renderer.domElement.className = 'three-canvas';
    container.appendChild(renderer.domElement);

    container.classList.add('canvas-loaded');

    // 2. OrbitControls (Drag 360 Rotation)
    let controls = null;
    if (typeof THREE.OrbitControls !== 'undefined') {
      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.06;
      controls.enableZoom = true;
      controls.minDistance = 4.5;
      controls.maxDistance = 10.0;
      controls.maxPolarAngle = Math.PI / 1.7;
      controls.minPolarAngle = Math.PI / 3.4;
      controls.autoRotate = true;
      controls.autoRotateSpeed = 1.0;
    }

    // 3. Lighting (Studio Showcase Lighting)
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
    scene.add(ambientLight);

    const topRim = new THREE.DirectionalLight(0xffffff, 1.8);
    topRim.position.set(0, 6, 4);
    scene.add(topRim);

    const violetKey = new THREE.PointLight(0x8B5CF6, 4.2, 20);
    violetKey.position.set(-4, 3, 2.5);
    scene.add(violetKey);

    const cyanFill = new THREE.PointLight(0x06B6D4, 3.6, 20);
    cyanFill.position.set(4, -2, 2.5);
    scene.add(cyanFill);

    // 4. Procedural Flagship 3D Device
    const device = new THREE.Group();

    const chassisMaterial = new THREE.MeshPhysicalMaterial({
      color: 0x161622,
      metalness: 0.92,
      roughness: 0.18,
      clearcoat: 1.0,
      clearcoatRoughness: 0.08
    });

    const screenGlass = new THREE.MeshStandardMaterial({
      color: 0x07070F,
      roughness: 0.05,
      metalness: 0.95,
    });

    // Chassis
    const mainChassis = new THREE.Mesh(new THREE.BoxGeometry(2.3, 4.8, 0.24), chassisMaterial);
    device.add(mainChassis);

    // Front OLED Glass
    const oledDisplay = new THREE.Mesh(new THREE.PlaneGeometry(2.18, 4.68), screenGlass);
    oledDisplay.position.z = 0.125;
    device.add(oledDisplay);

    // Emissive Display Border
    const oledBorder = new THREE.LineSegments(
      new THREE.EdgesGeometry(new THREE.PlaneGeometry(2.18, 4.68)),
      new THREE.LineBasicMaterial({ color: 0x06B6D4, transparent: true, opacity: 0.6 })
    );
    oledBorder.position.z = 0.128;
    device.add(oledBorder);

    // Camera Island (Back)
    const island = new THREE.Mesh(new THREE.BoxGeometry(0.95, 1.3, 0.1), chassisMaterial);
    island.position.set(-0.55, 1.45, -0.15);
    device.add(island);

    // Quad Lens Modules
    for (let i = 0; i < 4; i++) {
      const lGeo = new THREE.CylinderGeometry(0.18, 0.18, 0.06, 20);
      lGeo.rotateX(Math.PI / 2);
      const lMesh = new THREE.Mesh(lGeo, new THREE.MeshStandardMaterial({ color: 0x05050A, metalness: 0.98, roughness: 0.05 }));
      lMesh.position.set(-0.55 + (i % 2) * 0.42 - 0.21, 1.45 + (Math.floor(i / 2)) * 0.45 - 0.22, -0.2);
      device.add(lMesh);
    }

    scene.add(device);

    // 5. 5 Hotspot Coordinate Tracking
    const hotspotData = [
      {
        id: 'hotspotCamera',
        localPos: new THREE.Vector3(-0.55, 1.45, -0.25),
        title: 'Optical Matrix 200MP',
        desc: 'Quad-lens computational array with 5x periscope optical zoom and LiDAR depth mapping.'
      },
      {
        id: 'hotspotDisplay',
        localPos: new THREE.Vector3(0, 0.8, 0.15),
        title: 'Quantum OLED 120Hz',
        desc: 'ProMotion LTPO display with 3000 nits peak brightness and HDR10+ certification.'
      },
      {
        id: 'hotspotChip',
        localPos: new THREE.Vector3(0, -0.2, 0.15),
        title: '3nm Neural Silicon',
        desc: 'Nexus Bionic Core delivering 35 Trillion operations/sec on-device generative AI.'
      },
      {
        id: 'hotspotBattery',
        localPos: new THREE.Vector3(0, -1.8, 0.15),
        title: '5000mAh Ultra-Dense Battery',
        desc: '65W Turbo GaN charging engineered for up to 36 hours of creative battery life.'
      },
      {
        id: 'hotspotMaterials',
        localPos: new THREE.Vector3(1.1, 0, 0),
        title: 'Grade-5 Titanium Frame',
        desc: 'Precision micro-blasted aerospace titanium providing unprecedented strength-to-weight ratio.'
      }
    ];

    // Render 2D Hotspot DOM Elements over Viewport
    const hotspotContainer = document.getElementById('showroomHotspotsOverlay');
    if (hotspotContainer) {
      hotspotContainer.innerHTML = '';
      hotspotData.forEach(h => {
        const pin = document.createElement('div');
        pin.className = 'hotspot-point';
        pin.id = h.id;
        pin.innerHTML = `
          <div class="hotspot-pulse"></div>
          <div class="hotspot-dot"></div>
          <div class="hotspot-card">
            <div class="hotspot-title"><i class="fa-solid fa-microchip"></i> ${h.title}</div>
            <div class="hotspot-desc">${h.desc}</div>
          </div>
        `;
        hotspotContainer.appendChild(pin);

        pin.addEventListener('click', (e) => {
          e.stopPropagation();
          pin.classList.toggle('active');
        });
      });
    }

    // 6. Update Screen-Space Hotspot Projections
    const tempVec = new THREE.Vector3();
    const updateHotspotPositions = () => {
      if (!hotspotContainer) return;

      hotspotData.forEach(h => {
        const el = document.getElementById(h.id);
        if (!el) return;

        // Transform local 3D coordinates to world space
        tempVec.copy(h.localPos).applyMatrix4(device.matrixWorld);

        // Check if point is facing the camera
        const cameraDir = camera.position.clone().sub(tempVec).normalize();
        const dot = cameraDir.dot(new THREE.Vector3(0, 0, h.localPos.z >= 0 ? 1 : -1).applyQuaternion(device.quaternion));

        if (dot < -0.1) {
          el.style.opacity = '0.2';
          el.style.pointerEvents = 'none';
        } else {
          el.style.opacity = '1';
          el.style.pointerEvents = 'auto';
        }

        // Project to 2D normalized screen space
        tempVec.project(camera);
        const x = (tempVec.x * 0.5 + 0.5) * container.clientWidth;
        const y = (-(tempVec.y * 0.5) + 0.5) * container.clientHeight;

        el.style.left = `${x}px`;
        el.style.top = `${y}px`;
      });
    };

    // 7. Lifecycle & Intersection Observer
    let isVisible = true;
    let animId = null;
    const clock = new THREE.Clock();

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        isVisible = entry.isIntersecting;
        if (isVisible && !animId) {
          animate();
        }
      });
    }, { threshold: 0.1 });

    observer.observe(container);

    // 8. Render Loop
    const animate = () => {
      if (!isVisible) {
        animId = null;
        return;
      }

      const elapsed = clock.getElapsedTime();

      if (controls) {
        controls.update();
      } else {
        device.rotation.y = elapsed * 0.4;
      }

      // Subtle breathing float
      device.position.y = Math.sin(elapsed * 1.5) * 0.08;

      updateHotspotPositions();

      renderer.render(scene, camera);
      animId = requestAnimationFrame(animate);
    };

    animate();

    // 9. Resize Handler
    const onResize = () => {
      const w = container.clientWidth;
      const h = container.clientHeight;
      if (w === 0 || h === 0) return;

      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', onResize);

  } catch (err) {
    console.warn("Showroom WebGL initialization note:", err);
    container.classList.add('webgl-fallback-active');
  }
})();
