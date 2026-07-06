export function initNav() {
  const burger = document.querySelector('.burger');
  const mobileNav = document.querySelector('.mobile-nav');
  const header = document.querySelector('#site-header');

  if (header) {
    const onScroll = () => {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  if (!burger || !mobileNav) return;

  const toggle = () => {
    const isOpen = burger.classList.toggle('is-open');
    mobileNav.classList.toggle('is-open', isOpen);
    burger.setAttribute('aria-expanded', String(isOpen));
    document.body.style.overflow = isOpen ? 'hidden' : '';
  };

  burger.addEventListener('click', toggle);

  mobileNav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      if (burger.classList.contains('is-open')) toggle();
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && burger.classList.contains('is-open')) toggle();
  });
}
