/**
 * Module Theme Management (Dark / Light Mode)
 */

function initTheme() {
    const savedTheme = localStorage.getItem('phonecare_theme') || 'dark';
    applyTheme(savedTheme);
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('phonecare_theme', theme);
    
    const iconEl = document.getElementById('theme-icon');
    const textEl = document.getElementById('theme-text');
    if (iconEl && textEl) {
        if (theme === 'light') {
            iconEl.innerText = '☀️';
            textEl.innerText = 'Light Mode';
        } else {
            iconEl.innerText = '🌙';
            textEl.innerText = 'Dark Mode';
        }
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
}
