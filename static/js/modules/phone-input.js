const PHONE_PREFIX = '+38 (';
const PHONE_ERROR_ID = 'phone-input-error';
const PHONE_ERROR_TEXT = 'Введіть коректний номер телефону у форматі +38 (0XX) XXX-XX-XX';

function extractNationalDigits(value) {
  let digits = (value || '').replace(/\D/g, '');
  if (digits.startsWith('380')) {
    digits = digits.slice(3);
  } else if (digits.startsWith('38')) {
    digits = digits.slice(2);
  }
  if (digits && digits[0] !== '0') {
    digits = `0${digits}`;
  }
  return digits.slice(0, 10);
}

function formatNationalDigits(digits) {
  if (!digits) {
    return '';
  }

  let formatted = PHONE_PREFIX;
  formatted += digits.slice(0, 3);

  if (digits.length > 3) {
    formatted += `) ${digits.slice(3, 6)}`;
  }
  if (digits.length > 6) {
    formatted += `-${digits.slice(6, 8)}`;
  }
  if (digits.length > 8) {
    formatted += `-${digits.slice(8, 10)}`;
  }

  return formatted;
}

export function isValidUaPhone(value) {
  const digits = extractNationalDigits(value);
  return /^0[3-9]\d{8}$/.test(digits);
}

function getOrCreateErrorNode(input) {
  const group = input.closest('.form-group');
  if (!group) {
    return null;
  }

  let errorNode = group.querySelector(`#${PHONE_ERROR_ID}`);
  if (!errorNode) {
    errorNode = document.createElement('p');
    errorNode.id = PHONE_ERROR_ID;
    errorNode.className = 'form-error';
    errorNode.hidden = true;
    group.appendChild(errorNode);
  }

  return errorNode;
}

function setPhoneValidity(input, isValid, message = PHONE_ERROR_TEXT) {
  const errorNode = getOrCreateErrorNode(input);
  input.setAttribute('aria-invalid', isValid ? 'false' : 'true');
  input.classList.toggle('form-input--invalid', !isValid);

  if (!errorNode) {
    return;
  }

  if (isValid) {
    errorNode.hidden = true;
    errorNode.textContent = '';
    input.removeAttribute('aria-describedby');
    return;
  }

  errorNode.hidden = false;
  errorNode.textContent = message;
  input.setAttribute('aria-describedby', PHONE_ERROR_ID);
}

function applyPhoneMask(input) {
  const digits = extractNationalDigits(input.value);
  const formatted = formatNationalDigits(digits);
  input.value = formatted;
}

function bindPhoneInput(input) {
  if (!input || input.dataset.phoneBound === 'true') {
    return;
  }

  input.dataset.phoneBound = 'true';
  input.setAttribute('autocomplete', 'tel');
  input.setAttribute('enterkeyhint', 'done');

  if (input.value) {
    applyPhoneMask(input);
  }

  input.addEventListener('focus', () => {
    if (!input.value) {
      input.value = PHONE_PREFIX;
    }
  });

  input.addEventListener('input', () => {
    applyPhoneMask(input);
    if (isValidUaPhone(input.value)) {
      setPhoneValidity(input, true);
    } else {
      input.classList.remove('form-input--invalid');
    }
  });

  input.addEventListener('blur', () => {
    const digits = extractNationalDigits(input.value);
    if (!digits) {
      input.value = '';
      setPhoneValidity(input, true);
      return;
    }

    applyPhoneMask(input);
    setPhoneValidity(input, isValidUaPhone(input.value));
  });

  input.addEventListener('paste', (event) => {
    event.preventDefault();
    const pasted = event.clipboardData?.getData('text') || '';
    input.value = formatNationalDigits(extractNationalDigits(pasted));
    setPhoneValidity(input, isValidUaPhone(input.value));
  });

  const form = input.closest('form');
  form?.addEventListener('submit', (event) => {
    applyPhoneMask(input);
    if (!isValidUaPhone(input.value)) {
      event.preventDefault();
      setPhoneValidity(input, false);
      input.focus();
    }
  });
}

export function initPhoneInputs(root = document) {
  root.querySelectorAll('[data-phone-input], #id_phone').forEach(bindPhoneInput);
}
