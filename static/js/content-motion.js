(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const selectors = [
        '.topbar',
        '.page-header',
        '.welcome-section',
        '.section-heading',
        '.statistics-section',
        '.stat-card',
        '.charts-section',
        '.chart-card',
        '.card',
        '.indicator-detail',
        '.dataset-section',
        '.dataset-toolbar',
        '.dataset-table-wrapper',
        '.table-container'
    ];

    const elements = document.querySelectorAll(selectors.join(','));

    elements.forEach((element, index) => {
        element.classList.add('content-reveal');

        if (
            element.matches('.stat-card, .chart-card, .card, .indicator-detail')
        ) {
            const siblings = Array.from(element.parentElement.children);
            const position = siblings.indexOf(element);
            element.style.transitionDelay = `${Math.min(position * 110, 440)}ms`;
        }
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;

            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
        });
    }, {
        threshold: 0.12,
        rootMargin: '0px 0px -35px 0px'
    });

    elements.forEach(element => observer.observe(element));
})();
