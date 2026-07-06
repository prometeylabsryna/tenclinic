from django import forms
from django.core.exceptions import ValidationError
from unfold.widgets import UnfoldAdminTextareaWidget

from clinic.models import SiteSettings
from clinic.utils.map_embed import is_allowed_map_embed_url, normalize_map_embed


class SiteSettingsAdminForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'map_embed_url': UnfoldAdminTextareaWidget(attrs={'rows': 5}),
        }

    def clean_map_embed_url(self):
        raw = self.cleaned_data.get('map_embed_url', '')
        if not (raw or '').strip():
            return ''

        normalized = normalize_map_embed(raw)
        if not normalized:
            raise ValidationError(
                'Не вдалося знайти посилання в коді iframe. '
                'Скопіюйте повний код з Google Maps або вставте лише URL з src.'
            )
        if not is_allowed_map_embed_url(normalized):
            raise ValidationError('Дозволені лише посилання Google Maps для вбудовування карти.')
        return normalized
