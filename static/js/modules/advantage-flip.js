export function initAdvantageFlip() {
  const cards = [...document.querySelectorAll('.advantage-flip')];
  if (!cards.length) return;

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const desktopHover = window.matchMedia(
    '(min-width: 769px) and (hover: hover) and (pointer: fine)',
  ).matches;

  if (reduced || desktopHover) return;

  const CENTER_ZONE_RATIO = 0.1;
  let ticking = false;

  const getViewportCenter = () => {
    const viewport = window.visualViewport;
    if (!viewport) return window.innerHeight * 0.5;

    return viewport.offsetTop + viewport.height * 0.5;
  };

  const getCenterTolerance = () => {
    const viewport = window.visualViewport;
    const height = viewport?.height ?? window.innerHeight;
    return height * CENTER_ZONE_RATIO;
  };

  const updateFlips = () => {
    ticking = false;

    const viewportCenter = getViewportCenter();
    const tolerance = getCenterTolerance();

    let activeCard = null;
    let closestDistance = tolerance;

    cards.forEach((card) => {
      const rect = card.getBoundingClientRect();
      if (rect.bottom <= 0 || rect.top >= window.innerHeight) return;

      const cardCenter = rect.top + rect.height * 0.5;
      const distance = Math.abs(cardCenter - viewportCenter);

      if (distance <= closestDistance) {
        closestDistance = distance;
        activeCard = card;
      }
    });

    cards.forEach((card) => {
      card.classList.toggle('is-flipped', card === activeCard);
    });
  };

  const scheduleUpdate = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(updateFlips);
  };

  updateFlips();
  window.addEventListener('scroll', scheduleUpdate, { passive: true });
  window.addEventListener('resize', scheduleUpdate, { passive: true });
  window.addEventListener('orientationchange', scheduleUpdate);

  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', scheduleUpdate);
    window.visualViewport.addEventListener('scroll', scheduleUpdate);
  }
}
