import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.mail import send_mail


def notify_new_appointment(appointment):
    if appointment.is_direction_undecided:
        direction_label = 'Не можу визначитися'
    else:
        direction_label = str(appointment.direction) if appointment.direction else '—'

    subject = f'[TEN clinic] Нова заявка на запис — {appointment.name}'
    body = (
        f'ПІБ: {appointment.name}\n'
        f'Телефон: {appointment.phone}\n'
        f'Email: {appointment.email or "—"}\n'
        f'Напрямок: {direction_label}\n'
        f'Лікар: {appointment.doctor or "—"}\n'
        f'Спосіб звʼязку: {appointment.get_contact_method_display() or "—"}\n'
        f'Коментар: {appointment.comment or "—"}\n'
    )
    recipient = settings.NOTIFICATION_EMAIL
    if recipient:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=True)

    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '')
    if token and chat_id:
        payload = json.dumps({'chat_id': chat_id, 'text': f'Нова заявка\n{body}'}).encode()
        req = Request(
            f'https://api.telegram.org/bot{token}/sendMessage',
            data=payload,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        try:
            urlopen(req, timeout=10)
        except URLError:
            pass
