/**
 * NEXUS ELECTRONICS — ADVANCED ANIMATION & 3D INTERACTION ENGINE
 * Scroll progress, custom cursor, 3D card tilt physics, fly-to-cart bezier curves, and GSAP triggers.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Top Scroll Progress Indicator
  const progressBar = document.getElementById('scrollProgressBar');
  if (progressBar) {
    const updateScrollProgress = () => {
      const scrollTop = window.scrollY || document.documentElement.scrollTop;
      const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      progressBar.style.width = `${progress}%`;
    };

    window.addEventListener('scroll', updateScrollProgress, { passive: true });
    updateScrollProgress();
  }

  // 2. Custom Desktop Micro-Cursor
  const cursorDot = document.getElementById('cursorDot');
  const cursorRing = document.getElementById('cursorRing');

  if (cursorDot && cursorRing && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let ringX = mouseX;
    let ringY = mouseY;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursorDot.style.left = `${mouseX}px`;
      cursorDot.style.top = `${mouseY}px`;
    }, { passive: true });

    // Smooth Lerp loop for outer cursor ring
    const renderCursorRing = () => {
      ringX += (mouseX - ringX) * 0.18;
      ringY += (mouseY - ringY) * 0.18;
      cursorRing.style.left = `${ringX}px`;
      cursorRing.style.top = `${ringY}px`;
      requestAnimationFrame(renderCursorRing);
    };
    renderCursorRing();

    // Hover state expansion on interactive elements
    const interactiveSelectors = 'a, button, input, select, textarea, .product-card, .category-card, .hotspot-point, .promo-card';
    document.querySelectorAll(interactiveSelectors).forEach(el => {
      el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
      el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
    });
  }

  // 3. 3D Card Tilt Engine with Specular Light Glare
  const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  if (!isTouchDevice) {
    const tiltCards = document.querySelectorAll('.card-3d-tilt, .product-card, .category-card, .best-seller-card');
    
    tiltCards.forEach(card => {
      // Ensure specular glare layer exists
      if (!card.querySelector('.tilt-glare')) {
        const glare = document.createElement('div');
        glare.className = 'tilt-glare';
        card.appendChild(glare);
      }

      card.style.transformStyle = 'preserve-3d';

      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const maxTilt = 8; // degrees
        const rotateX = -((y - centerY) / centerY) * maxTilt;
        const rotateY = ((x - centerX) / centerX) * maxTilt;

        card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateZ(4px)`;

        const glare = card.querySelector('.tilt-glare');
        if (glare) {
          const glareX = (x / rect.width) * 100;
          const glareY = (y / rect.height) * 100;
          glare.style.background = `radial-gradient(circle at ${glareX}% ${glareY}%, rgba(255, 255, 255, 0.18), transparent 60%)`;
        }
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
      });
    });
  }

  // 4. GSAP ScrollTrigger Integration (Safe Fallback)
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
    document.body.classList.add('js-ready');

    // Staggered reveal for cards and sections
    gsap.utils.toArray('.reveal-on-scroll').forEach(section => {
      gsap.fromTo(section, 
        { y: 35, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.75,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: section,
            start: 'top 85%',
            toggleActions: 'play none none none'
          }
        }
      );
    });

    // Stagger for product cards
    gsap.utils.toArray('.product-grid-6, .product-grid-4, .product-grid-3').forEach(grid => {
      const cards = grid.querySelectorAll('.product-card');
      if (cards.length > 0) {
        gsap.fromTo(cards,
          { y: 30, opacity: 0 },
          {
            y: 0,
            opacity: 1,
            duration: 0.6,
            stagger: 0.08,
            ease: 'power2.out',
            scrollTrigger: {
              trigger: grid,
              start: 'top 85%',
              toggleActions: 'play none none none'
            }
          }
        );
      }
    });
  }

  // 5. Global Fly-to-Cart Trigger Function
  window.triggerFlyToCart = (startElement) => {
    const cartTarget = document.getElementById('navCartBtn') || document.querySelector('.nav-icon-btn[href*="cart"]');
    if (!startElement || !cartTarget) return;

    const img = startElement.closest('.product-card')?.querySelector('img') || startElement;
    if (!img) return;

    const rect = img.getBoundingClientRect();
    const targetRect = cartTarget.getBoundingClientRect();

    const flyingClone = img.cloneNode(true);
    flyingClone.className = 'flying-cart-item';
    flyingClone.style.left = `${rect.left}px`;
    flyingClone.style.top = `${rect.top}px`;
    flyingClone.style.width = `${rect.width}px`;
    flyingClone.style.height = `${rect.height}px`;
    document.body.appendChild(flyingClone);

    // Force layout reflow
    flyingClone.getBoundingClientRect();

    // Trigger flight transform
    const deltaX = targetRect.left + (targetRect.width / 2) - (rect.left + (rect.width / 2));
    const deltaY = targetRect.top + (targetRect.height / 2) - (rect.top + (rect.height / 2));

    flyingClone.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(0.12)`;
    flyingClone.style.opacity = '0.3';

    setTimeout(() => {
      flyingClone.remove();
      const badge = cartTarget.querySelector('.nav-badge');
      if (badge) {
        badge.classList.remove('cart-badge-pulse');
        void badge.offsetWidth; // trigger reflow
        badge.classList.add('cart-badge-pulse');
      }
    }, 850);
  };
});
