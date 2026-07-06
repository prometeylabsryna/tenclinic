from unfold.admin import ModelAdmin

from clinic.admin.mixins import ImagePreviewMixin, ReadableUnfoldFieldsMixin, SingletonModelAdminMixin
from clinic.admin.site_settings_form import SiteSettingsAdminForm
from clinic.models import SiteSettings


class SiteSettingsAdmin(ReadableUnfoldFieldsMixin, ImagePreviewMixin, SingletonModelAdminMixin, ModelAdmin):
    form = SiteSettingsAdminForm
    readonly_fields = ('logo_preview',)
    image_preview_field = 'logo'

    fieldsets = (
        ('Основне', {
            'fields': ('site_name', 'tagline', 'logo', 'logo_preview', 'meta_description'),
            'description': (
                'Назва сайту, слоган і логотип відображаються в шапці та підвалі. '
                'Тексти секцій головної — у розділі «Контент сторінок».'
            ),
        }),
        ('Контакти та карта', {
            'fields': (
                'address', 'phone_primary', 'phone_secondary', 'email',
                'telegram_url', 'viber_url',
                'map_lat', 'map_lng', 'map_embed_url', 'directions_text',
            ),
            'description': (
                'Єдине місце для адреси, телефонів і карти. Зміни відображаються на головній, '
                'сторінці «Контакти», у підвалі та в блоці запису. '
                'Для карти найпростіший спосіб — широта + довгота. '
                'Або вставте повний код вбудовування з Google Maps у поле «Карта Google Maps».'
            ),
        }),
        ('Сповіщення про заявки', {
            'fields': ('notification_email', 'telegram_bot_token', 'telegram_chat_id'),
            'classes': ('collapse',),
        }),
    )

    def logo_preview(self, obj):
        return self.get_image_preview(obj)

    logo_preview.short_description = 'Як виглядає зараз'
