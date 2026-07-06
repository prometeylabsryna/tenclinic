export function initAccordion() {
  document.querySelectorAll('.accordion__trigger').forEach((trigger) => {
    trigger.addEventListener('click', () => {
      const item = trigger.closest('.accordion__item');
      const isOpen = item.classList.contains('is-open');
      const group = item.closest('.accordion');

      if (group?.dataset.accordion === 'single') {
        group.querySelectorAll('.accordion__item.is-open').forEach((openItem) => {
          if (openItem !== item) {
            openItem.classList.remove('is-open');
            openItem.querySelector('.accordion__trigger')?.setAttribute('aria-expanded', 'false');
          }
        });
      }

      item.classList.toggle('is-open', !isOpen);
      trigger.setAttribute('aria-expanded', String(!isOpen));
    });
  });
}
