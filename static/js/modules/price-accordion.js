export function initPriceAccordion() {
  const items = document.querySelectorAll('.price-accordion');
  if (!items.length) {
    return;
  }

  const desktopQuery = window.matchMedia('(min-width: 768px)');

  const syncOpenState = () => {
    items.forEach((item) => {
      item.open = desktopQuery.matches;
    });
  };

  syncOpenState();
  desktopQuery.addEventListener('change', syncOpenState);
}
