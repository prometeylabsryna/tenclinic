const MOBILE_MQ = window.matchMedia('(max-width: 767px)');
const MONTHS_UA = [
  'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
  'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень',
];
const WEEKDAYS_UA = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'];
const OPEN_FIELDS = new Set();
const ALL_INSTANCES = new Set();

function parseIsoDate(value) {
  if (!value) {
    return null;
  }
  const [year, month, day] = value.split('-').map(Number);
  if (!year || !month || !day) {
    return null;
  }
  return new Date(year, month - 1, day);
}

function toIsoDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function formatDisplay(value) {
  const date = parseIsoDate(value);
  if (!date) {
    return 'дд.мм.рррр';
  }
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  return `${day}.${month}.${date.getFullYear()}`;
}

function startWeekday(year, month) {
  const weekday = new Date(year, month, 1).getDay();
  return weekday === 0 ? 6 : weekday - 1;
}

function daysInMonth(year, month) {
  return new Date(year, month + 1, 0).getDate();
}

function lockBodyScroll() {
  document.documentElement.classList.add('date-field-open');
}

function unlockBodyScroll() {
  if (OPEN_FIELDS.size === 0) {
    document.documentElement.classList.remove('date-field-open');
  }
}

function closeField(instance) {
  instance.root.classList.remove('is-open');
  instance.trigger.setAttribute('aria-expanded', 'false');
  instance.sheet.hidden = true;
  instance.backdrop.hidden = true;
  instance.sheet.classList.remove('is-active');
  instance.backdrop.classList.remove('is-active');
  OPEN_FIELDS.delete(instance);
  unlockBodyScroll();
}

function mountSheet(instance) {
  if (instance.sheetMounted) {
    return;
  }
  document.body.append(instance.backdrop, instance.sheet);
  instance.sheetMounted = true;
}

function updateTrigger(instance) {
  const value = instance.input.value;
  instance.trigger.textContent = formatDisplay(value);
  instance.trigger.classList.toggle('is-placeholder', !value);
}

function renderCalendar(instance) {
  const minDate = parseIsoDate(instance.input.min) || new Date();
  minDate.setHours(0, 0, 0, 0);

  const selected = parseIsoDate(instance.input.value);
  const year = instance.viewDate.getFullYear();
  const month = instance.viewDate.getMonth();

  instance.monthLabel.textContent = `${MONTHS_UA[month]} ${year}`;
  instance.grid.innerHTML = '';

  const totalDays = daysInMonth(year, month);
  const leading = startWeekday(year, month);

  for (let i = 0; i < leading; i += 1) {
    const spacer = document.createElement('span');
    spacer.className = 'date-field__day is-empty';
    spacer.setAttribute('aria-hidden', 'true');
    instance.grid.appendChild(spacer);
  }

  for (let day = 1; day <= totalDays; day += 1) {
    const current = new Date(year, month, day);
    current.setHours(0, 0, 0, 0);
    const iso = toIsoDate(current);
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'date-field__day';
    button.textContent = String(day);
    button.dataset.value = iso;

    if (current < minDate) {
      button.disabled = true;
      button.classList.add('is-disabled');
    }

    if (selected && toIsoDate(selected) === iso) {
      button.classList.add('is-selected');
      button.setAttribute('aria-selected', 'true');
    }

    button.addEventListener('click', () => {
      instance.input.value = iso;
      instance.input.dispatchEvent(new Event('change', { bubbles: true }));
      updateTrigger(instance);
      closeField(instance);
    });

    instance.grid.appendChild(button);
  }
}

function openField(instance) {
  OPEN_FIELDS.forEach((item) => {
    if (item !== instance) {
      closeField(item);
    }
  });

  const selected = parseIsoDate(instance.input.value);
  instance.viewDate = selected ? new Date(selected) : new Date();
  renderCalendar(instance);
  mountSheet(instance);

  instance.root.classList.add('is-open');
  instance.sheet.hidden = false;
  instance.backdrop.hidden = false;
  OPEN_FIELDS.add(instance);
  lockBodyScroll();

  requestAnimationFrame(() => {
    instance.sheet.classList.add('is-active');
    instance.backdrop.classList.add('is-active');
  });
}

function bindDateInput(input) {
  if (!input || input.dataset.dateBound === 'true' || !MOBILE_MQ.matches) {
    return null;
  }

  const field = input.closest('.form-group');
  const labelText = field?.querySelector('.form-label')?.textContent.replace('*', '').trim() || 'Дата';

  const root = document.createElement('div');
  root.className = 'date-field';
  input.parentNode.insertBefore(root, input);
  root.appendChild(input);

  input.classList.add('date-field__native');
  input.dataset.dateBound = 'true';

  const triggerId = input.id ? `${input.id}_trigger` : `date-trigger-${Math.random().toString(36).slice(2, 9)}`;
  const trigger = document.createElement('button');
  trigger.type = 'button';
  trigger.className = 'date-field__trigger form-input';
  trigger.id = triggerId;
  trigger.setAttribute('aria-haspopup', 'dialog');
  trigger.setAttribute('aria-expanded', 'false');

  const backdrop = document.createElement('div');
  backdrop.className = 'date-field__backdrop';
  backdrop.hidden = true;

  const sheet = document.createElement('div');
  sheet.className = 'date-field__sheet';
  sheet.hidden = true;
  sheet.setAttribute('role', 'dialog');
  sheet.setAttribute('aria-modal', 'true');

  const head = document.createElement('div');
  head.className = 'date-field__sheet-head';

  const prev = document.createElement('button');
  prev.type = 'button';
  prev.className = 'date-field__nav';
  prev.setAttribute('aria-label', 'Попередній місяць');
  prev.textContent = '‹';

  const monthLabel = document.createElement('p');
  monthLabel.className = 'date-field__month';

  const next = document.createElement('button');
  next.type = 'button';
  next.className = 'date-field__nav';
  next.setAttribute('aria-label', 'Наступний місяць');
  next.textContent = '›';

  const close = document.createElement('button');
  close.type = 'button';
  close.className = 'date-field__close';
  close.setAttribute('aria-label', 'Закрити календар');
  close.innerHTML = '&times;';

  const title = document.createElement('p');
  title.className = 'date-field__title';
  title.textContent = labelText;

  head.append(prev, monthLabel, next, close);

  const weekdays = document.createElement('div');
  weekdays.className = 'date-field__weekdays';
  WEEKDAYS_UA.forEach((name) => {
    const item = document.createElement('span');
    item.textContent = name;
    weekdays.appendChild(item);
  });

  const grid = document.createElement('div');
  grid.className = 'date-field__grid';
  grid.setAttribute('role', 'grid');

  sheet.append(title, head, weekdays, grid);
  root.append(trigger);

  const label = input.id ? document.querySelector(`label[for="${input.id}"]`) : null;
  if (label) {
    label.htmlFor = triggerId;
  }

  const instance = {
    root,
    input,
    trigger,
    backdrop,
    sheet,
    monthLabel,
    grid,
    viewDate: new Date(),
    sheetMounted: false,
  };

  mountSheet(instance);
  updateTrigger(instance);

  trigger.addEventListener('click', () => {
    if (instance.root.classList.contains('is-open')) {
      closeField(instance);
      return;
    }
    trigger.setAttribute('aria-expanded', 'true');
    openField(instance);
  });

  prev.addEventListener('click', () => {
    instance.viewDate.setMonth(instance.viewDate.getMonth() - 1);
    renderCalendar(instance);
  });

  next.addEventListener('click', () => {
    instance.viewDate.setMonth(instance.viewDate.getMonth() + 1);
    renderCalendar(instance);
  });

  backdrop.addEventListener('click', () => closeField(instance));
  close.addEventListener('click', () => closeField(instance));

  input.addEventListener('change', () => updateTrigger(instance));

  ALL_INSTANCES.add(instance);
  return instance;
}

let globalHandlersBound = false;

function bindGlobalHandlers() {
  if (globalHandlersBound) {
    return;
  }
  globalHandlersBound = true;

  document.addEventListener('click', (event) => {
    OPEN_FIELDS.forEach((instance) => {
      if (!instance.root.contains(event.target) && !instance.sheet.contains(event.target)) {
        instance.trigger.setAttribute('aria-expanded', 'false');
        closeField(instance);
      }
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape' || OPEN_FIELDS.size === 0) {
      return;
    }
    [...OPEN_FIELDS].forEach((instance) => {
      instance.trigger.setAttribute('aria-expanded', 'false');
      closeField(instance);
      instance.trigger.focus();
    });
  });
}

export function cleanupOrphanDatePortals() {
  ALL_INSTANCES.forEach((instance) => {
    if (!document.contains(instance.root)) {
      instance.sheet.remove();
      instance.backdrop.remove();
      ALL_INSTANCES.delete(instance);
      OPEN_FIELDS.delete(instance);
    }
  });

  document.querySelectorAll('body > .date-field__backdrop, body > .date-field__sheet').forEach((node) => {
    const tracked = [...ALL_INSTANCES].some(
      (instance) => instance.sheet === node || instance.backdrop === node,
    );
    if (!tracked) {
      node.remove();
    }
  });

  if (OPEN_FIELDS.size === 0) {
    document.documentElement.classList.remove('date-field-open');
  }
}

export function initDateInputs(root = document) {
  if (!MOBILE_MQ.matches) {
    return;
  }

  bindGlobalHandlers();
  cleanupOrphanDatePortals();

  root.querySelectorAll('input[type="date"][data-date-input], input[type="date"].form-input').forEach((input) => {
    bindDateInput(input);
  });
}

export function initDateInputGlobal() {
  initDateInputs();

  const handleSwap = (event) => {
    const swapRoot = event.detail?.elt;
    if (swapRoot instanceof Element) {
      initDateInputs(swapRoot);
    }
  };

  document.body.addEventListener('htmx:afterSwap', handleSwap);
  document.body.addEventListener('htmx:afterSettle', handleSwap);
}
