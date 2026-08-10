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

  // 3. Mobile Menu Drawer Toggle
  const mobileToggle = document.getElementById('mobileMenuToggle');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const drawerClose = document.getElementById('drawerClose');

  if (mobileToggle && mobileDrawer) {
    mobileToggle.addEventListener('click', () => {
      mobileDrawer.classList.toggle('active');
    });
  }

  if (drawerClose && mobileDrawer) {
    drawerClose.addEventListener('click', () => {
      mobileDrawer.classList.remove('active');
    });
  }

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
        input.value = val + 1;
      });
    }
  });
});