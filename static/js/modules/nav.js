export function initNav() {
  const burger = document.querySelector('.burger');
  const mobileNav = document.querySelector('.mobile-nav');
  const header = document.querySelector('#site-header');
  let lockedScrollY = 0;

  if (header) {
    const onScroll = () => {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  if (!burger || !mobileNav) return;

  const lockBody = () => {
    lockedScrollY = window.scrollY;
    document.body.style.position = 'fixed';
    document.body.style.top = `-${lockedScrollY}px`;
    document.body.style.left = '0';
    document.body.style.right = '0';
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';
  };

  const unlockBody = () => {
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.left = '';
    document.body.style.right = '';
    document.body.style.overflow = '';
    document.documentElement.style.overflow = '';
    window.scrollTo(0, lockedScrollY);
  };

  const toggle = (forceOpen) => {
    const isOpen = typeof forceOpen === 'boolean'
      ? forceOpen
      : !burger.classList.contains('is-open');

    burger.classList.toggle('is-open', isOpen);
    mobileNav.classList.toggle('is-open', isOpen);
    burger.setAttribute('aria-expanded', String(isOpen));

    if (isOpen) {
      lockBody();
      return;
    }

    unlockBody();
    mobileNav.scrollTop = 0;
  };

  burger.addEventListener('click', () => toggle());

  mobileNav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      if (burger.classList.contains('is-open')) toggle(false);
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && burger.classList.contains('is-open')) toggle(false);
  });

  window.addEventListener('orientationchange', () => {
    if (!burger.classList.contains('is-open')) return;
    requestAnimationFrame(() => {
      mobileNav.scrollTop = 0;
    });
  });
}
