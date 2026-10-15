// Light/dark toggle. The initial theme is set by an inline script in <head> to avoid a flash.
(function () {
    var root = document.documentElement;
    var button = document.querySelector('.theme-toggle');

    function syncGiscus(theme) {
        var frame = document.querySelector('iframe.giscus-frame');
        if (frame) {
            frame.contentWindow.postMessage(
                { giscus: { setConfig: { theme: theme } } },
                'https://giscus.app'
            );
        }
    }

    function apply(theme) {
        root.setAttribute('data-theme', theme);
        if (button) {
            button.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
        }
        syncGiscus(theme);
    }

    if (button) {
        apply(root.getAttribute('data-theme') || 'light');
        button.addEventListener('click', function () {
            var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            try {
                localStorage.setItem('theme', next);
            } catch (e) {
                // Storage can be blocked (private mode); the toggle still works for this page.
            }
            apply(next);
        });
    }
})();
