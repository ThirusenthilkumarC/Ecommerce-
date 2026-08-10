// ==========================================
// FLASH DEALS LIVE COUNTDOWN TIMER
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
  const hoursEl = document.getElementById('dealHours');
  const minutesEl = document.getElementById('dealMinutes');
  const secondsEl = document.getElementById('dealSeconds');

  if (!hoursEl || !minutesEl || !secondsEl) return;

  // Set target end time (e.g., 8 hours from now or end of current day)
  let totalSeconds = (7 * 3600) + (45 * 60) + 32;

  function updateTimer() {
    if (totalSeconds <= 0) {
      totalSeconds = 24 * 3600; // Reset loop for demo
    }

    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    hoursEl.textContent = String(hours).padStart(2, '0');
    minutesEl.textContent = String(minutes).padStart(2, '0');
    secondsEl.textContent = String(seconds).padStart(2, '0');

    totalSeconds--;
  }

  updateTimer();
  setInterval(updateTimer, 1000);
});
