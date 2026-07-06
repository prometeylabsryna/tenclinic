export function initReveal() {
  observeReveal(document);

  document.body.addEventListener('htmx:afterSwap', (event) => {
    const target = event.detail?.target;
    if (target) {
      observeReveal(target);
    }
  });
}

export function observeReveal(root = document) {
  const items = root.querySelectorAll('.reveal:not(.is-visible)');
  if (!items.length) return;

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) {
    items.forEach((el) => el.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' },
  );

  items.forEach((el) => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      el.classList.add('is-visible');
      return;
    }
    observer.observe(el);
  });
}
