import { isValidUaPhone } from './phone-input.js?v=20260706i';

const INVALID_CLASS = 'form-input--invalid';

function getVisibleControl(control) {
  if (control instanceof HTMLSelectElement && control.classList.contains('custom-select__native')) {
    return control.closest('.custom-select')?.querySelector('.custom-select__trigger') || control;
  }

  if (control.matches('.date-field__native')) {
    return control.closest('.date-field')?.querySelector('.date-field__trigger') || control;
  }

  return control;
}

function getOrCreateErrorNode(group) {
  let errorNode = group.querySelector('.form-error.js-client-error');
  if (!errorNode) {
    errorNode = document.createElement('p');
    errorNode.className = 'form-error js-client-error';
    errorNode.hidden = true;
    group.appendChild(errorNode);
  }
  return errorNode;
}

function setFieldError(control, message) {
  const group = control.closest('.form-group');
  if (!group) {
    return;
  }

  const visible = getVisibleControl(control);
  const errorNode = getOrCreateErrorNode(group);

  visible.classList.add(INVALID_CLASS);
  visible.setAttribute('aria-invalid', 'true');
  errorNode.textContent = message;
  errorNode.hidden = false;

  if (visible !== control) {
    control.setAttribute('aria-invalid', 'true');
  }
}

export function clearBookingClientErrors(form) {
  form.querySelectorAll('.js-client-error').forEach((node) => {
    node.hidden = true;
    node.textContent = '';
  });

  form.querySelectorAll(`.${INVALID_CLASS}`).forEach((node) => {
    node.classList.remove(INVALID_CLASS);
    node.removeAttribute('aria-invalid');
  });

  form.querySelectorAll('[aria-invalid="true"]').forEach((node) => {
    node.removeAttribute('aria-invalid');
  });
}

function focusFirstInvalid(form) {
  const clientError = form.querySelector('.form-group .form-error.js-client-error:not([hidden])');
  if (clientError) {
    const group = clientError.closest('.form-group');
    group?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    const focusTarget = group?.querySelector(
      '.custom-select__trigger, .date-field__trigger, input:not([type="hidden"]), textarea, select, button[type="button"]',
    );
    focusTarget?.focus({ preventScroll: true });
    return;
  }

  const serverError = form.querySelector('.form-group .form-error:not(.js-client-error)');
  if (serverError) {
    serverError.closest('.form-group')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }

  const invalid = form.querySelector(`.${INVALID_CLASS}, input[aria-invalid="true"], select[aria-invalid="true"], textarea[aria-invalid="true"]`);
  if (!invalid) {
    return;
  }

  const target = invalid.matches('input[type="checkbox"]') ? invalid : getVisibleControl(invalid);
  target.scrollIntoView({ behavior: 'smooth', block: 'center' });
  target.focus({ preventScroll: true });
}

export function validateBookingForm(form) {
  clearBookingClientErrors(form);
  let isValid = true;

  form.querySelectorAll('select.custom-select__native').forEach((select) => {
    if (select.required && !select.value) {
      setFieldError(select, 'Оберіть значення');
      isValid = false;
    }
  });

  const dateInput = form.querySelector('input[type="date"][data-date-input], #id_preferred_date');
  if (dateInput?.required && !dateInput.value) {
    setFieldError(dateInput, 'Оберіть бажану дату');
    isValid = false;
  }

  const phoneInput = form.querySelector('[data-phone-input], #id_phone');
  if (phoneInput?.required && !isValidUaPhone(phoneInput.value)) {
    setFieldError(phoneInput, 'Введіть коректний номер телефону у форматі +38 (0XX) XXX-XX-XX');
    isValid = false;
  }

  form.querySelectorAll('input:not([type="hidden"]):not(.date-field__native):not(.form-honeypot), textarea, select:not(.custom-select__native)').forEach((control) => {
    if (control === phoneInput || control.id === 'id_consent') {
      return;
    }

    if (!control.checkValidity()) {
      setFieldError(control, control.validationMessage || 'Заповніть це поле');
      isValid = false;
    }
  });

  const consent = form.querySelector('#id_consent');
  if (consent?.required && !consent.checked) {
    setFieldError(consent, 'Потрібна згода на обробку персональних даних');
    isValid = false;
  }

  if (!isValid) {
    focusFirstInvalid(form);
  }

  return isValid;
}

function isBookingForm(form) {
  return form instanceof HTMLFormElement && Boolean(form.closest('#booking-form-wrapper'));
}

export function initBookingValidation() {
  document.body.addEventListener('submit', (event) => {
    const form = event.target;
    if (!isBookingForm(form)) {
      return;
    }

    if (!validateBookingForm(form)) {
      event.preventDefault();
      event.stopPropagation();
    }
  }, true);

  document.body.addEventListener('htmx:validation:halted', (event) => {
    const elt = event.detail?.elt;
    const form = elt instanceof HTMLFormElement ? elt : elt?.closest('form');
    if (!isBookingForm(form)) {
      return;
    }

    validateBookingForm(form);
  });

  document.body.addEventListener('input', (event) => {
    const control = event.target;
    if (!(control instanceof HTMLElement)) {
      return;
    }

    const form = control.closest('form');
    if (!isBookingForm(form)) {
      return;
    }

    const group = control.closest('.form-group');
    if (!group) {
      return;
    }

    group.querySelector('.js-client-error')?.remove();
    getVisibleControl(control).classList.remove(INVALID_CLASS);
    control.removeAttribute('aria-invalid');
  });

  document.body.addEventListener('change', (event) => {
    const control = event.target;
    if (!(control instanceof HTMLElement)) {
      return;
    }

    const form = control.closest('form');
    if (!isBookingForm(form)) {
      return;
    }

    if (control instanceof HTMLSelectElement && control.classList.contains('custom-select__native')) {
      const group = control.closest('.form-group');
      group?.querySelector('.js-client-error')?.remove();
      getVisibleControl(control).classList.remove(INVALID_CLASS);
    }

    if (control.matches('.date-field__native') && control.value) {
      const group = control.closest('.form-group');
      group?.querySelector('.js-client-error')?.remove();
      getVisibleControl(control).classList.remove(INVALID_CLASS);
    }

    if (control.id === 'id_consent' && control instanceof HTMLInputElement && control.checked) {
      const group = control.closest('.form-group');
      group?.querySelector('.js-client-error')?.remove();
      control.classList.remove(INVALID_CLASS);
    }
  });
}
