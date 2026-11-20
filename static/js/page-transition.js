(() => {
    const reducedMotion = window.matchMedia(
        '(prefers-reduced-motion: reduce)'
    ).matches;

    if (reducedMotion) return;

    const overlay = document.createElement('div');
    overlay.className = 'page-transition-overlay transition-reveal';
    document.body.appendChild(overlay);

    // Reveal the newly loaded page.
    window.addEventListener('pageshow', () => {
        overlay.classList.remove('transition-cover');
        overlay.classList.add('transition-reveal');
    });

    // Smooth transition for internal page navigation.
    document.addEventListener('click', (event) => {
        const link = event.target.closest('a[href]');
        if (!link) return;

        if (
            event.defaultPrevented ||
            event.button !== 0 ||
            event.ctrlKey ||
            event.shiftKey ||
            event.altKey ||
            event.metaKey ||
            link.target === '_blank' ||
            link.hasAttribute('download')
        ) return;

        const url = new URL(link.href, window.location.href);

        if (
            url.origin !== window.location.origin ||
            url.pathname === window.location.pathname &&
            url.search === window.location.search ||
            link.getAttribute('href').startsWith('#')
        ) return;

        event.preventDefault();

        overlay.classList.remove('transition-reveal');
        overlay.classList.add('transition-cover');

        setTimeout(() => {
            window.location.href = url.href;
        }, 620);
    });
})();
