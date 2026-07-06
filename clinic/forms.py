from datetime import date

from django import forms
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ValidationError

from clinic.models import Appointment, Direction, Doctor, Service
from clinic.utils.phone_validation import normalize_ua_phone


class AppointmentForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-honeypot',
        'tabindex': '-1',
        'autocomplete': 'off',
    }))

    consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'id': 'id_consent'}),
    )

    class Meta:
        model = Appointment
        fields = [
            'name', 'phone', 'email', 'direction', 'service',
            'doctor', 'preferred_date', 'preferred_time', 'comment',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ваше імʼя'}),
            'phone': forms.TelInput(attrs={
                'class': 'form-input',
                'placeholder': '+38 (0XX) XXX-XX-XX',
                'inputmode': 'tel',
                'autocomplete': 'tel',
                'data-phone-input': '',
                'pattern': r'\+38 \(0[3-9]\d{2}\) \d{3}-\d{2}-\d{2}',
                'title': 'Формат: +38 (0XX) XXX-XX-XX',
            }),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}),
            'direction': forms.Select(attrs={'class': 'form-select', 'hx-get': '', 'hx-target': '#service-field', 'hx-trigger': 'change'}),
            'service': forms.Select(attrs={'class': 'form-select', 'hx-get': '', 'hx-target': '#doctor-field', 'hx-trigger': 'change'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'preferred_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'data-date-input': '',
            }),
            'preferred_time': forms.Select(
                attrs={'class': 'form-select'},
                choices=[
                    ('', 'Оберіть час'),
                    ('morning', 'Ранок (09:00–12:00)'),
                    ('day', 'День (12:00–16:00)'),
                    ('evening', 'Вечір (16:00–18:00)'),
                ],
            ),
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Коментар (опційно)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direction'].queryset = Direction.objects.filter(is_active=True)
        self.fields['direction'].empty_label = 'Оберіть напрямок'
        self.fields['service'].queryset = Service.objects.none()
        self.fields['service'].empty_label = 'Оберіть послугу'
        self.fields['doctor'].queryset = Doctor.objects.none()
        self.fields['doctor'].empty_label = 'Будь-який лікар'
        self.fields['doctor'].required = False
        self.fields['email'].required = False
        self.fields['preferred_date'].widget.attrs['min'] = date.today().isoformat()

        direction_id = None
        if self.data.get('direction'):
            direction_id = self.data.get('direction')
        elif self.initial.get('direction'):
            direction_id = self.initial['direction'].pk if hasattr(self.initial['direction'], 'pk') else self.initial['direction']

        if direction_id:
            self.fields['service'].queryset = Service.objects.filter(direction_id=direction_id, is_active=True)

        service_id = self.data.get('service') or (self.initial.get('service').pk if self.initial.get('service') else None)
        if service_id:
            self.fields['doctor'].queryset = Doctor.objects.filter(services__id=service_id, is_active=True).distinct()
        elif direction_id:
            self.fields['doctor'].queryset = Doctor.objects.filter(direction_id=direction_id, is_active=True)

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('Spam detected')
        return ''

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip()
        if not phone:
            raise forms.ValidationError('Введіть коректний номер телефону')
        try:
            return normalize_ua_phone(phone)
        except ValidationError as exc:
            raise forms.ValidationError(exc.messages[0]) from exc

    def clean_preferred_date(self):
        preferred = self.cleaned_data.get('preferred_date')
        if preferred and preferred < date.today():
            raise forms.ValidationError('Дата не може бути в минулому')
        return preferred


def is_rate_limited(ip: str) -> bool:
    if not ip:
        return False
    key = f'booking_rate_{ip}'
    count = cache.get(key, 0)
    return count >= settings.BOOKING_RATE_LIMIT


def increment_rate_limit(ip: str):
    if not ip:
        return
    key = f'booking_rate_{ip}'
    count = cache.get(key, 0)
    cache.set(key, count + 1, settings.BOOKING_RATE_WINDOW)
