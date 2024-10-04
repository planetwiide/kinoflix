// Theme Toggle Script
const themeToggle = document.getElementById('themeToggle');
const body = document.body;
const icon = themeToggle.querySelector('i');
const logo = document.getElementById('logo');
const favicon = document.querySelector('link[rel="icon"]');

// Apply saved theme on load
const currentTheme = localStorage.getItem('theme');
if (currentTheme) {
    body.classList.add(currentTheme);
    if (currentTheme === 'light') {
        icon.classList.replace('fa-moon', 'fa-sun');
        logo.src = '/images/kinoflix-light.png'; // light theme logo
        favicon.href = '/images/kinoflix-light.ico'; // light theme favicon
    }
}

// Toggle theme switching
themeToggle.addEventListener('click', () => {
    body.classList.toggle('light');
    if (body.classList.contains('light')) {
        icon.classList.replace('fa-moon', 'fa-sun');
        logo.src = '/images/kinoflix-light.png'; // light theme logo
        favicon.href = '/images/kinoflix-light.ico'; // light theme favicon
        localStorage.setItem('theme', 'light');
    } else {
        icon.classList.replace('fa-sun', 'fa-moon');
        logo.src = '/images/kinoflix.png'; // dark theme logo
        favicon.href = '/images/kinoflix.ico'; // dark theme favicon
        localStorage.setItem('theme', '');
    }
});
