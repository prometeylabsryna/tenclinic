from django import forms
from unfold.widgets import UnfoldAdminImageFieldWidget, UnfoldAdminTextareaWidget

from clinic.image_specs import HEARING_AID_IMAGE
from clinic.models import HearingAid


class HearingAidAdminForm(forms.ModelForm):
    class Meta:
        model = HearingAid
        fields = ('name', 'slug', 'short_description', 'image', 'is_active')
        widgets = {
            'image': UnfoldAdminImageFieldWidget,
            'short_description': UnfoldAdminTextareaWidget(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Назва моделі',
            'short_description': 'Підпис',
            'image': 'Фото',
        }
        help_texts = {
            'image': (
                f'Формат: JPG або PNG. Рекомендований розмір: {HEARING_AID_IMAGE.width}×{HEARING_AID_IMAGE.height} px '
                f'({HEARING_AID_IMAGE.ratio}). Зображення відображається на картці в каталозі.'
            ),
            'short_description': 'Короткий текст під фото на картці в каталозі.',
        }
