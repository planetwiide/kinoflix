// Theme Toggle Script
const toggleSwitch = document.getElementById('theme-toggle');
const currentTheme = localStorage.getItem('theme');
const logo = document.querySelector('.logo img');
const favicon = document.querySelector('link[rel="icon"]');

// Apply saved theme on load
if (currentTheme) {
    document.body.classList.add(currentTheme);
    if (currentTheme === 'light-theme') {
        toggleSwitch.checked = true;
        logo.src = '/images/kinoflix-light.png'; // light theme logo
        favicon.href = '/images/kinoflix-light.ico'; // light theme favicon
    }
}

// Switch theme and store in localStorage
toggleSwitch.addEventListener('change', () => {
    if (toggleSwitch.checked) {
        document.body.classList.add('light-theme');
        localStorage.setItem('theme', 'light-theme');
        logo.src = '/images/kinoflix-light.png'; // light theme logo
        favicon.href = '/images/kinoflix-light.ico'; // light theme favicon
    } else {
        document.body.classList.remove('light-theme');
        localStorage.setItem('theme', 'dark-theme');
        logo.src = '/images/kinoflix.png'; // dark theme logo
        favicon.href = '/images/kinoflix.ico'; // dark theme favicon
    }
});
