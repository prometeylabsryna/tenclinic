export function initHtmxCsrf() {
  if (!window.htmx) return;

  window.htmx.config.reportValidityOfForms = true;

  const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  if (!token) return;

  document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = token;
  });
}
