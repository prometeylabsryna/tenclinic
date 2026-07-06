function syncDoctorsFilterChips() {
  const bar = document.querySelector('.doctors-page__filter-bar');
  if (!bar) {
    return;
  }

  const activeDirection = new URL(window.location.href).searchParams.get('direction') || '';

  bar.querySelectorAll('.filter-chip').forEach((chip) => {
    const chipDirection = new URL(chip.href, window.location.origin).searchParams.get('direction') || '';
    chip.classList.toggle('is-active', chipDirection === activeDirection);
  });
}

function resetDoctorsRailScroll() {
  const rail = document.querySelector('.doctors-page__rail');
  if (rail) {
    rail.scrollLeft = 0;
  }
}

export function initDoctorsFilters() {
  const page = document.querySelector('.doctors-page');
  if (!page) {
    return;
  }

  document.body.addEventListener('htmx:afterSwap', (event) => {
    if (event.detail.target?.id !== 'doctors-grid') {
      return;
    }

    syncDoctorsFilterChips();
    resetDoctorsRailScroll();
  });
}
