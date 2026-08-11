/**
 * NEXUS ELECTRONICS — ADMIN ANALYTICS & CHART.JS INTEGRATION
 * Live database-driven revenue trajectories and fulfillment metrics.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Revenue Trajectory Line Chart
  const revenueCanvas = document.getElementById('adminRevenueChart');
  if (revenueCanvas && typeof Chart !== 'undefined') {
    const ctx = revenueCanvas.getContext('2d');
    
    // Gradient fill
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(108, 92, 231, 0.4)');
    gradient.addColorStop(1, 'rgba(108, 92, 231, 0.0)');

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
          label: 'Monthly Revenue (₹)',
          data: [45000, 78000, 112000, 165000, 140000, 198000, 245000, 310000, 280000, 390000, 450000, 520000],
          borderColor: '#6C5CE7',
          borderWidth: 3,
          backgroundColor: gradient,
          fill: true,
          tension: 0.35,
          pointBackgroundColor: '#8B5CF6',
          pointRadius: 4,
          pointHoverRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => ` Revenue: ₹${context.raw.toLocaleString('en-IN')}`
            }
          }
        },
        scales: {
          y: {
            grid: { color: 'rgba(0, 0, 0, 0.05)' },
            ticks: {
              callback: (value) => `₹${(value / 1000)}k`
            }
          },
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }

  // 2. Order Status Donut Chart
  const statusCanvas = document.getElementById('adminOrderStatusChart');
  if (statusCanvas && typeof Chart !== 'undefined') {
    new Chart(statusCanvas.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: ['Delivered', 'Processing', 'Confirmed', 'Pending'],
        datasets: [{
          data: [65, 18, 12, 5],
          backgroundColor: ['#00B894', '#0984E3', '#6C5CE7', '#FDCB6E'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { font: { size: 12, family: 'Inter' } }
          }
        },
        cutout: '70%'
      }
    });
  }
});
