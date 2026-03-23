// Load saved theme
if (localStorage.getItem('theme') === 'light') {
    document.documentElement.classList.remove('dark');
} else {
    document.documentElement.classList.add('dark');
}

function toggleTheme() {
    if (document.documentElement.classList.contains('dark')) {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    } else {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }
}

window.toggleTheme = toggleTheme;