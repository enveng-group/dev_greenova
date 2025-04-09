document.addEventListener('DOMContentLoaded', function () {
  // Get saved theme from localStorage or use auto
  const savedTheme = localStorage.getItem('theme') || 'auto';

  // Apply the theme
  applyTheme(savedTheme);

  // Function to apply theme
  function applyTheme(theme) {
    if (theme === 'auto') {
      // Check system preference
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.dataset.theme = 'dark';
      } else {
        document.documentElement.dataset.theme = 'light';
      }
    } else {
      document.documentElement.dataset.theme = theme;
    }
  }

  // Set up listener for system preference changes if in auto mode
  if (savedTheme === 'auto') {
    window
      .matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', function (e) {
        applyTheme('auto');
      });
  }
});
