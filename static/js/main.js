// ==========================================
// NEXUS ELECTRONICS - MAIN JAVASCRIPT
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
  // 1. Global Image Error Fallback Handler
  const DEFAULT_PLACEHOLDER = 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=500&auto=format&fit=crop&q=80';
  
  document.querySelectorAll('img').forEach(img => {
    img.addEventListener('error', function() {
      if (this.src !== DEFAULT_PLACEHOLDER) {
        this.src = DEFAULT_PLACEHOLDER;
      }
    });
  });

  // 2. Toast Auto-Dismiss
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach(toast => {
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 4500);
  });

  // 3. Mobile Navigation Drawer Controller (Modal Pattern)
  const mobileToggle = document.getElementById('mobileMenuToggle');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const drawerOverlay = document.getElementById('mobileDrawerOverlay');
  const drawerClose = document.getElementById('drawerClose');

  const openDrawer = () => {
    if (mobileDrawer) mobileDrawer.classList.add('active');
    if (drawerOverlay) drawerOverlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Lock scroll
  };

  const closeDrawer = () => {
    if (mobileDrawer) mobileDrawer.classList.remove('active');
    if (drawerOverlay) drawerOverlay.classList.remove('active');
    document.body.style.overflow = ''; // Unlock scroll
  };

  if (mobileToggle) {
    mobileToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      openDrawer();
    });
  }

  if (drawerClose) {
    drawerClose.addEventListener('click', closeDrawer);
  }

  if (drawerOverlay) {
    drawerOverlay.addEventListener('click', closeDrawer);
  }

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeDrawer();
    }
  });

  // Automatically close drawer if resized to desktop (>= 1024px)
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024) {
      closeDrawer();
    }
  });

  // 4. User Account Dropdown Click Toggle
  const userAccountBtn = document.getElementById('userAccountBtn');
  const userDropdown = document.getElementById('userDropdown');

  if (userAccountBtn && userDropdown) {
    userAccountBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      userDropdown.classList.toggle('active');
    });

    document.addEventListener('click', () => {
      userDropdown.classList.remove('active');
    });
  }

  // 5. Quantity Stepper Controls
  const qtyWrappers = document.querySelectorAll('.quantity-picker');
  qtyWrappers.forEach(wrapper => {
    const decBtn = wrapper.querySelector('.qty-dec');
    const incBtn = wrapper.querySelector('.qty-inc');
    const input = wrapper.querySelector('.qty-input');

    if (decBtn && incBtn && input) {
      decBtn.addEventListener('click', () => {
        let val = parseInt(input.value) || 1;
        if (val > 1) {
          input.value = val - 1;
        }
      });

      incBtn.addEventListener('click', () => {
        let val = parseInt(input.value) || 1;
        let max = parseInt(input.getAttribute('max')) || 999;
        if (val < max) {
          input.value = val + 1;
        }
      });
    }
  });

  // 6. Category Horizontal Carousel Controls
  const catScrollContainer = document.getElementById('categoryScrollContainer');
  const catPrevBtn = document.getElementById('catPrevBtn');
  const catNextBtn = document.getElementById('catNextBtn');

  if (catScrollContainer && catPrevBtn && catNextBtn) {
    const scrollAmount = 280;

    catPrevBtn.addEventListener('click', (e) => {
      e.preventDefault();
      catScrollContainer.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });

    catNextBtn.addEventListener('click', (e) => {
      e.preventDefault();
      catScrollContainer.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });

    const updateArrows = () => {
      const { scrollLeft, scrollWidth, clientWidth } = catScrollContainer;
      // Fade out left arrow if at start
      catPrevBtn.style.opacity = scrollLeft <= 10 ? '0.35' : '1';
      catPrevBtn.style.pointerEvents = scrollLeft <= 10 ? 'none' : 'auto';
      // Fade out right arrow if at end
      const atEnd = scrollLeft + clientWidth >= scrollWidth - 10;
      catNextBtn.style.opacity = atEnd ? '0.35' : '1';
      catNextBtn.style.pointerEvents = atEnd ? 'none' : 'auto';
    };

    catScrollContainer.addEventListener('scroll', updateArrows, { passive: true });
    window.addEventListener('resize', updateArrows);
    // Initial check
    setTimeout(updateArrows, 100);
  }
});