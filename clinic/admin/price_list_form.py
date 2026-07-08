from django import forms
from django.utils.text import slugify

from clinic.models import PriceListItem
from clinic.price_items import PRICE_SLUG_PREFIX, price_item_slug


def unique_price_slug(base):
    from clinic.models import Service

    slug = price_item_slug(base)
    if not Service.objects.filter(slug=slug).exists():
        return slug
    for index in range(2, 100):
        candidate = price_item_slug(f'{base}-{index}')
        if not Service.objects.filter(slug=candidate).exists():
            return candidate
    raise ValueError('Не вдалося згенерувати унікальний slug.')


class PriceListItemForm(forms.ModelForm):
    class Meta:
        model = PriceListItem
        fields = (
            'name',
            'direction',
            'price',
            'price_note',
            'duration_minutes',
            'is_active',
        )

    def save(self, commit=True):
        obj = super().save(commit=False)
        if not obj.description:
            obj.description = ''
        if not obj.short_description:
            obj.short_description = ''
        if not obj.slug:
            base = slugify(obj.name, allow_unicode=True) or 'posytsiya'
            obj.slug = unique_price_slug(base)
        elif not obj.slug.startswith(PRICE_SLUG_PREFIX):
            obj.slug = price_item_slug(obj.slug.removeprefix(PRICE_SLUG_PREFIX))
        if commit:
            obj.save()
        return obj
