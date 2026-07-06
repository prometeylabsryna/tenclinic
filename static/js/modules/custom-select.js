const OPEN_SELECTS = new Set();
const MOBILE_MQ = window.matchMedia('(max-width: 767px)');
let globalHandlersBound = false;

function bindGlobalHandlers() {
  if (globalHandlersBound) {
    return;
  }

  globalHandlersBound = true;

  document.addEventListener('click', (event) => {
    OPEN_SELECTS.forEach((instance) => {
      if (!instance.root.contains(event.target)) {
        closeSelect(instance);
      }
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape' || OPEN_SELECTS.size === 0) {
      return;
    }

    const openInstances = [...OPEN_SELECTS];
    openInstances.forEach((instance) => {
      closeSelect(instance);
      instance.trigger.focus();
    });
  });
}

function getSelectedOption(select) {
  return select.options[select.selectedIndex] || null;
}

function getOptionLabel(option) {
  if (!option) {
    return '';
  }
  return option.textContent.trim();
}

function isPlaceholderOption(option) {
  return !option || option.value === '';
}

function lockBodyScroll() {
  document.documentElement.classList.add('custom-select-open');
}

function unlockBodyScroll() {
  if (OPEN_SELECTS.size === 0) {
    document.documentElement.classList.remove('custom-select-open');
  }
}

function closeSelect(instance) {
  if (!instance?.root) {
    return;
  }

  instance.root.classList.remove('is-open');
  instance.trigger.setAttribute('aria-expanded', 'false');
  instance.dropdown.classList.remove('is-active');
  instance.backdrop.classList.remove('is-active');
  instance.dropdown.hidden = true;
  instance.backdrop.hidden = true;
  OPEN_SELECTS.delete(instance);
  unlockBodyScroll();
  restoreDropdown(instance);
}

function mountDropdown(instance) {
  if (instance.dropdownMounted || !MOBILE_MQ.matches) {
    return;
  }

  document.body.append(instance.backdrop, instance.dropdown);
  instance.dropdownMounted = true;
}

function restoreDropdown(instance) {
  if (!instance.dropdownMounted) {
    return;
  }

  instance.root.append(instance.backdrop, instance.dropdown);
  instance.dropdownMounted = false;
}

function closeAllExcept(current) {
  OPEN_SELECTS.forEach((instance) => {
    if (instance !== current) {
      closeSelect(instance);
    }
  });
}

function updateTrigger(instance) {
  const selected = getSelectedOption(instance.select);
  const label = getOptionLabel(selected);
  instance.valueNode.textContent = label;
  instance.valueNode.classList.toggle('is-placeholder', isPlaceholderOption(selected));
}

function buildOptions(instance) {
  instance.list.innerHTML = '';

  Array.from(instance.select.options).forEach((option) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'custom-select__option';
    button.role = 'option';
    button.dataset.value = option.value;
    button.textContent = option.textContent.trim();
    button.setAttribute('aria-selected', option.selected ? 'true' : 'false');

    if (option.disabled) {
      button.disabled = true;
      button.classList.add('is-disabled');
    }

    if (option.selected) {
      button.classList.add('is-selected');
    }

    button.addEventListener('click', () => {
      if (option.disabled) {
        return;
      }

      instance.select.value = option.value;
      instance.select.dispatchEvent(new Event('change', { bubbles: true }));
      updateTrigger(instance);
      buildOptions(instance);
      closeSelect(instance);
    });

    instance.list.appendChild(button);
  });
}

function openSelect(instance) {
  closeAllExcept(instance);
  updateTrigger(instance);
  buildOptions(instance);
  mountDropdown(instance);

  instance.root.classList.add('is-open');
  instance.trigger.setAttribute('aria-expanded', 'true');
  instance.dropdown.hidden = false;
  instance.backdrop.hidden = false;
  OPEN_SELECTS.add(instance);

  requestAnimationFrame(() => {
    instance.dropdown.classList.add('is-active');
    instance.backdrop.classList.add('is-active');
  });

  if (MOBILE_MQ.matches) {
    lockBodyScroll();
  }
}

function bindCustomSelect(select) {
  if (!select || select.dataset.customSelectBound === 'true') {
    return null;
  }

  if (select.closest('.custom-select')) {
    return null;
  }

  const field = select.closest('.form-group');
  const label = field?.querySelector('.form-label')
    || (select.id
      ? document.querySelector(`label[for="${select.id}"], label[for="${select.id}_trigger"]`)
      : null);
  const labelText = label?.textContent.replace('*', '').trim() || 'Оберіть значення';

  const root = document.createElement('div');
  root.className = 'custom-select';
  select.parentNode.insertBefore(root, select);
  root.appendChild(select);

  select.classList.remove('form-select');
  select.classList.add('custom-select__native');
  select.hidden = true;
  select.tabIndex = -1;
  select.setAttribute('aria-hidden', 'true');
  select.dataset.customSelectBound = 'true';

  const triggerId = select.id ? `${select.id}_trigger` : `custom-select-trigger-${Math.random().toString(36).slice(2, 9)}`;

  const trigger = document.createElement('button');
  trigger.type = 'button';
  trigger.className = 'custom-select__trigger';
  trigger.id = triggerId;
  trigger.setAttribute('aria-haspopup', 'listbox');
  trigger.setAttribute('aria-expanded', 'false');

  const valueNode = document.createElement('span');
  valueNode.className = 'custom-select__value';

  const icon = document.createElement('span');
  icon.className = 'custom-select__icon';
  icon.setAttribute('aria-hidden', 'true');

  trigger.append(valueNode, icon);

  const backdrop = document.createElement('div');
  backdrop.className = 'custom-select__backdrop';
  backdrop.hidden = true;

  const dropdown = document.createElement('div');
  dropdown.className = 'custom-select__dropdown';
  dropdown.hidden = true;

  const sheetHead = document.createElement('div');
  sheetHead.className = 'custom-select__sheet-head';

  const sheetTitle = document.createElement('p');
  sheetTitle.className = 'custom-select__sheet-title';
  sheetTitle.textContent = labelText;

  const sheetClose = document.createElement('button');
  sheetClose.type = 'button';
  sheetClose.className = 'custom-select__sheet-close';
  sheetClose.setAttribute('aria-label', 'Закрити список');
  sheetClose.innerHTML = '&times;';

  sheetHead.append(sheetTitle, sheetClose);

  const list = document.createElement('div');
  list.className = 'custom-select__list';
  list.setAttribute('role', 'listbox');

  dropdown.append(sheetHead, list);
  root.append(trigger, backdrop, dropdown);

  if (label) {
    label.htmlFor = triggerId;
  }

  const instance = {
    root,
    select,
    trigger,
    valueNode,
    dropdown,
    backdrop,
    list,
    sheetClose,
    dropdownMounted: false,
  };

  updateTrigger(instance);
  buildOptions(instance);

  trigger.addEventListener('click', () => {
    if (instance.root.classList.contains('is-open')) {
      closeSelect(instance);
      return;
    }
    openSelect(instance);
  });

  backdrop.addEventListener('click', () => closeSelect(instance));
  sheetClose.addEventListener('click', () => closeSelect(instance));

  select.addEventListener('change', () => {
    updateTrigger(instance);
    buildOptions(instance);
  });

  return instance;
}

export function initCustomSelects(root = document) {
  root.querySelectorAll('.custom-select').forEach((existingRoot) => {
    const native = existingRoot.querySelector('select');
    if (!native || !root.contains(existingRoot)) {
      return;
    }

    existingRoot.remove();
    if (native.parentNode !== root) {
      root.appendChild(native);
    }
    native.hidden = false;
    native.classList.remove('custom-select__native');
    native.classList.add('form-select');
    native.removeAttribute('data-custom-select-bound');
    native.removeAttribute('aria-hidden');
    native.tabIndex = 0;
  });

  root.querySelectorAll('select.form-select').forEach((select) => {
    bindCustomSelect(select);
  });
}

function getSwapRoot(event) {
  const elt = event.detail?.elt;
  return elt instanceof Element ? elt : null;
}

export function initCustomSelectGlobal() {
  bindGlobalHandlers();
  initCustomSelects();

  const handleSwap = (event) => {
    const swapRoot = getSwapRoot(event);
    if (swapRoot) {
      initCustomSelects(swapRoot);
    }
  };

  document.body.addEventListener('htmx:afterSwap', handleSwap);
  document.body.addEventListener('htmx:afterSettle', handleSwap);

  MOBILE_MQ.addEventListener('change', () => {
    OPEN_SELECTS.forEach((instance) => {
      restoreDropdown(instance);
      closeSelect(instance);
    });
  });
}
