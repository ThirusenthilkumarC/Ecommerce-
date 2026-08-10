// ==========================================
// HERO SECTION INTERACTIVE CAROUSEL
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.hero-slide');
  const prevBtn = document.getElementById('heroPrevBtn');
  const nextBtn = document.getElementById('heroNextBtn');
  const currentIndicator = document.getElementById('heroCurrentIndex');
  const totalIndicator = document.getElementById('heroTotalIndex');

  if (!slides.length) return;

  let currentIdx = 0;
  const totalSlides = slides.length;

  if (totalIndicator) {
    totalIndicator.textContent = String(totalSlides).padStart(2, '0');
  }

  function showSlide(index) {
    slides.forEach((s, i) => {
      if (i === index) {
        s.style.display = 'grid';
        s.classList.add('active');
      } else {
        s.style.display = 'none';
        s.classList.remove('active');
      }
    });

    if (currentIndicator) {
      currentIndicator.textContent = String(index + 1).padStart(2, '0');
    }
  }

  // Initialize
  showSlide(currentIdx);

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      currentIdx = (currentIdx - 1 + totalSlides) % totalSlides;
      showSlide(currentIdx);
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      currentIdx = (currentIdx + 1) % totalSlides;
      showSlide(currentIdx);
    });
  }

  // Optional subtle auto-rotate every 7 seconds
  setInterval(() => {
    currentIdx = (currentIdx + 1) % totalSlides;
    showSlide(currentIdx);
  }, 7000);
});
