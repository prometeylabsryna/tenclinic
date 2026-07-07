from django import forms
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ValidationError

from clinic.block_defaults import BLOCK_DEFAULTS
from clinic.models import Appointment, Direction, Doctor
from clinic.utils.phone_validation import normalize_ua_phone


class AppointmentForm(forms.ModelForm):
    DIRECTION_UNDECIDED = 'undecided'

    direction = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_direction'}),
    )

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
            'name', 'phone', 'email', 'doctor', 'contact_method', 'comment',
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
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'contact_method': forms.RadioSelect(),
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Коментар (опційно)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        undecided_label = BLOCK_DEFAULTS.get(('booking', 'direction_undecided'), 'Не можу визначитися')
        direction_choices = [('', 'Оберіть напрямок')]
        direction_choices.extend(
            (str(direction.pk), direction.name)
            for direction in Direction.objects.filter(is_active=True)
        )
        direction_choices.append((self.DIRECTION_UNDECIDED, undecided_label))
        self.fields['direction'].choices = direction_choices

        self.fields['doctor'].queryset = Doctor.objects.none()
        self.fields['doctor'].empty_label = 'Будь-який лікар'
        self.fields['doctor'].required = False
        self.fields['email'].required = False
        self.fields['contact_method'].choices = Appointment.CONTACT_METHOD_CHOICES
        self.fields['contact_method'].widget = forms.RadioSelect()

        direction_value = self.data.get('direction') if self.is_bound else None
        if not direction_value and self.initial.get('direction'):
            direction_obj = self.initial['direction']
            direction_value = str(direction_obj.pk if hasattr(direction_obj, 'pk') else direction_obj)
            self.initial['direction'] = direction_value

        if direction_value and direction_value != self.DIRECTION_UNDECIDED:
            self.fields['doctor'].queryset = Doctor.objects.filter(
                directions__id=direction_value,
                is_active=True,
            ).distinct()

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

    def clean_direction(self):
        value = self.cleaned_data.get('direction')
        if not value:
            raise forms.ValidationError('Оберіть напрямок')
        if value == self.DIRECTION_UNDECIDED:
            return value
        if not Direction.objects.filter(pk=value, is_active=True).exists():
            raise forms.ValidationError('Оберіть напрямок')
        return value

    def save(self, commit=True):
        instance = super().save(commit=False)
        direction_value = self.cleaned_data.get('direction')
        if direction_value == self.DIRECTION_UNDECIDED:
            instance.direction = None
            instance.is_direction_undecided = True
        else:
            instance.direction = Direction.objects.filter(pk=direction_value).first()
            instance.is_direction_undecided = False
        instance.service = None
        instance.preferred_date = None
        instance.preferred_time = ''
        if commit:
            instance.save()
        return instance


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
