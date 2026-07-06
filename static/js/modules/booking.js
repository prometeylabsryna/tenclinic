import { initPhoneInputs } from './phone-input.js?v=20260706i';
import { initCustomSelects } from './custom-select.js?v=20260706i';
import { initDateInputs, cleanupOrphanDatePortals } from './date-input.js?v=20260706i';
import { initBookingValidation } from './booking-validation.js?v=20260706i';

function showBookingSuccess(swapRoot) {
  cleanupOrphanDatePortals();

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
  initDateInputs();

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
        initDateInputs(swapRoot);
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
    if (!(target instanceof HTMLSelectElement) || !window.htmx) {
      return;
    }

    if (target.id === 'id_direction' && target.dataset.servicesUrl) {
      const value = target.value;
      window.htmx.ajax('GET', `${target.dataset.servicesUrl}?direction=${value}`, {
        target: '#service-select-wrapper',
        swap: 'innerHTML',
      }).then(() => {
        initCustomSelects(document.querySelector('#service-select-wrapper'));
      });

      const doctorsUrl = target.dataset.doctorsUrl
        || wrapper.querySelector('#id_service')?.dataset.doctorsUrl;
      if (doctorsUrl) {
        window.htmx.ajax('GET', `${doctorsUrl}?direction=${value}`, {
          target: '#doctor-select-wrapper',
          swap: 'innerHTML',
        }).then(() => {
          initCustomSelects(document.querySelector('#doctor-select-wrapper'));
        });
      }
      return;
    }

    if (target.id === 'id_service' && target.dataset.doctorsUrl) {
      window.htmx.ajax('GET', `${target.dataset.doctorsUrl}?service=${target.value}`, {
        target: '#doctor-select-wrapper',
        swap: 'innerHTML',
      }).then(() => {
        initCustomSelects(document.querySelector('#doctor-select-wrapper'));
      });
    }
  });
}
