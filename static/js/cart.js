// ==========================================
// NEXUS ELECTRONICS - CART & WISHLIST AJAX
// ==========================================

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <i class="fa-solid ${type === 'success' ? 'fa-circle-check text-green' : 'fa-circle-exclamation text-red'}"></i>
    <span>${message}</span>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Quick Add to Cart via AJAX
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.ajax-add-cart-btn');
  if (!btn) return;

  e.preventDefault();
  const productId = btn.getAttribute('data-product-id');
  if (!productId) return;

  const originalHtml = btn.innerHTML;
  btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
  btn.disabled = true;

  fetch(`/cart/add/${productId}/`, {
    method: 'POST',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  .then(res => res.json())
  .then(data => {
    btn.innerHTML = originalHtml;
    btn.disabled = false;

    if (data.success) {
      showToast(data.message, 'success');
      // Update cart count badge
      const badges = document.querySelectorAll('.cart-badge-count');
      badges.forEach(b => {
        b.textContent = data.cart_count;
        b.style.display = data.cart_count > 0 ? 'flex' : 'none';
      });
    } else {
      showToast(data.message, 'error');
    }
  })
  .catch(err => {
    btn.innerHTML = originalHtml;
    btn.disabled = false;
    showToast('Failed to add product to cart.', 'error');
  });
});

// Toggle Wishlist via AJAX
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.ajax-wishlist-btn');
  if (!btn) return;

  e.preventDefault();
  const productId = btn.getAttribute('data-product-id');
  if (!productId) return;

  fetch(`/wishlist/toggle/${productId}/`, {
    method: 'POST',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      if (data.added) {
        btn.classList.add('active');
        btn.innerHTML = '<i class="fa-solid fa-heart" style="color: #EF4444;"></i>';
      } else {
        btn.classList.remove('active');
        btn.innerHTML = '<i class="fa-regular fa-heart"></i>';
      }
      showToast(data.message, 'info');

      // Update wishlist count badge
      const badges = document.querySelectorAll('.wishlist-badge-count');
      badges.forEach(b => {
        b.textContent = data.wishlist_count;
        b.style.display = data.wishlist_count > 0 ? 'flex' : 'none';
      });
    }
  })
  .catch(err => {
    showToast('Failed to update wishlist.', 'error');
  });
});
