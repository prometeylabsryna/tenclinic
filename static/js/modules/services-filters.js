function syncServicesFilterChips() {
  const bar = document.querySelector('.services-page__filters');
  if (!bar) {
    return;
  }

  const activeDirection = new URL(window.location.href).searchParams.get('direction') || '';

  bar.querySelectorAll('.filter-chip').forEach((chip) => {
    const chipDirection = new URL(chip.href, window.location.origin).searchParams.get('direction') || '';
    chip.classList.toggle('is-active', chipDirection === activeDirection);
  });
}

export function initServicesFilters() {
  const page = document.querySelector('.services-page');
  if (!page) {
    return;
  }

  syncServicesFilterChips();

  document.body.addEventListener('htmx:afterSwap', (event) => {
    if (event.detail.target?.id !== 'services-grid') {
      return;
    }

    syncServicesFilterChips();
  });

  window.addEventListener('popstate', syncServicesFilterChips);
}
