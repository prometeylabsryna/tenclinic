import { initPhoneInputs } from './phone-input.js?v=20260706i';
import { initCustomSelects } from './custom-select.js?v=20260706i';
import { initBookingValidation } from './booking-validation.js?v=20260706i';

const DIRECTION_UNDECIDED = 'undecided';

function showBookingSuccess(swapRoot) {
  const success = swapRoot.querySelector('.booking-success');
  if (!success) {
    return;
  }

  requestAnimationFrame(() => {
    success.scrollIntoView({ behavior: 'smooth', block: 'center' });
    success.focus({ preventScroll: true });
  });
}

export function initBooking() {
  initBookingValidation();
  initPhoneInputs();

  if (!document.body.dataset.bookingHtmxBound) {
    document.body.dataset.bookingHtmxBound = 'true';

    document.body.addEventListener('htmx:afterSwap', (event) => {
      const swapRoot = event.detail?.elt;
      if (swapRoot?.id === 'booking-form-wrapper') {
        if (swapRoot.querySelector('.booking-success')) {
          showBookingSuccess(swapRoot);
          return;
        }

        initPhoneInputs(swapRoot);
        initCustomSelects(swapRoot);
      }
    });

    document.body.addEventListener('htmx:afterSettle', (event) => {
      const swapRoot = event.detail?.elt;
      if (swapRoot?.id === 'booking-form-wrapper' && swapRoot.querySelector('.booking-success')) {
        showBookingSuccess(swapRoot);
      }
    });
  }

  const wrapper = document.querySelector('#booking-form-wrapper');
  if (!wrapper || wrapper.dataset.bookingBound === 'true') {
    return;
  }

  wrapper.dataset.bookingBound = 'true';

  wrapper.addEventListener('change', (event) => {
    const target = event.target;
    if (!(target instanceof HTMLSelectElement) || target.id !== 'id_direction' || !window.htmx) {
      return;
    }

    const doctorsUrl = target.dataset.doctorsUrl;
    if (!doctorsUrl) {
      return;
    }

    const value = target.value;
    const query = value && value !== DIRECTION_UNDECIDED ? `?direction=${encodeURIComponent(value)}` : '';

    window.htmx.ajax('GET', `${doctorsUrl}${query}`, {
      target: '#doctor-select-wrapper',
      swap: 'innerHTML',
    }).then(() => {
      initCustomSelects(document.querySelector('#doctor-select-wrapper'));
    });
  });
}
