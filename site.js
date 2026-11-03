// Theme toggle. The initial theme is applied by a tiny inline script in <head>
// (before first paint) so the page never flashes the wrong colours.
(function () {
    var root = document.documentElement;
    var toggle = document.getElementById('theme-toggle');
    var media = window.matchMedia('(prefers-color-scheme: dark)');

    function store(key, value) {
        try { localStorage.setItem(key, value); } catch (e) { /* storage blocked */ }
    }
    function read(key) {
        try { return localStorage.getItem(key); } catch (e) { return null; }
    }

    // Effective theme = explicit choice if any, otherwise the OS setting.
    function currentTheme() {
        return root.getAttribute('data-theme') || (media.matches ? 'dark' : 'light');
    }

    function updateIcon() {
        if (!toggle) return;
        var dark = currentTheme() === 'dark';
        var icon = toggle.querySelector('i');
        if (icon) icon.className = dark ? 'fas fa-sun' : 'fas fa-moon';
        toggle.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
        toggle.setAttribute('title', dark ? 'Switch to light mode' : 'Switch to dark mode');
    }

    if (toggle) {
        toggle.addEventListener('click', function () {
            var next = currentTheme() === 'dark' ? 'light' : 'dark';
            root.classList.add('theme-transition');
            root.setAttribute('data-theme', next);
            store('theme', next);
            updateIcon();
            window.setTimeout(function () { root.classList.remove('theme-transition'); }, 300);
        });
    }

    // Follow OS changes live, as long as the visitor hasn't chosen a theme.
    var onSystemChange = function () {
        if (!read('theme')) {
            root.removeAttribute('data-theme');
            updateIcon();
        }
    };
    if (media.addEventListener) media.addEventListener('change', onSystemChange);
    else if (media.addListener) media.addListener(onSystemChange);

    updateIcon();
})();
