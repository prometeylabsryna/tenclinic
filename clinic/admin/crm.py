from unfold.admin import ModelAdmin

from clinic.admin.hearing_aid_form import HearingAidAdminForm
from clinic.admin.mixins import DoctorImagePreviewMixin, ImagePreviewMixin, OrderOnCreateMixin, ReadableUnfoldFieldsMixin
from clinic.models import Appointment, Direction, Doctor, HearingAid, Service, WorkingHours


class DirectionAdmin(OrderOnCreateMixin, ImagePreviewMixin, ModelAdmin):
    ordering_field = 'order'
    hide_ordering_field = True
    list_display = ('name', 'image_thumb', 'is_active')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    readonly_fields = ('get_image_preview',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'short_description', 'description', 'image', 'get_image_preview', 'is_active'),
            'description': 'Короткий опис — для картки. Повний опис — на детальній сторінці.',
        }),
        ('Детальна сторінка', {
            'fields': ('when_to_visit', 'services_overview'),
            'description': 'Кожен пункт — з нового рядка. «Наші послуги» показується списком на сторінці напрямку.',
        }),
    )

    def image_thumb(self, obj):
        return self.get_image_preview(obj)

    image_thumb.short_description = 'Фото'


class DoctorAdmin(OrderOnCreateMixin, DoctorImagePreviewMixin, ModelAdmin):
    ordering_field = 'order'
    hide_ordering_field = True
    list_display = ('full_name', 'photo_thumb', 'specialization', 'direction', 'is_active')
    list_filter = ('direction', 'is_active')
    prepopulated_fields = {'slug': ('full_name',)}
    search_fields = ('full_name', 'specialization')
    autocomplete_fields = ('direction',)
    filter_horizontal = ('services',)
    readonly_fields = ('get_image_preview',)
    fieldsets = (
        (None, {
            'fields': (
                'full_name', 'slug', 'photo', 'get_image_preview',
                'specialization', 'direction', 'is_active',
            ),
        }),
        ('Профіль', {
            'fields': ('bio', 'education', 'experience_years', 'services'),
        }),
    )

    def photo_thumb(self, obj):
        return self.get_image_preview(obj)

    photo_thumb.short_description = 'Фото'


class HearingAidAdmin(OrderOnCreateMixin, ReadableUnfoldFieldsMixin, ImagePreviewMixin, ModelAdmin):
    form = HearingAidAdminForm
    ordering_field = 'order'
    hide_ordering_field = True
    list_display = ('name', 'image_thumb', 'caption_preview', 'is_active')
    list_display_links = ('name',)
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description')
    readonly_fields = ('get_image_preview',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'is_active'),
        }),
        ('Картка на сайті', {
            'fields': ('image', 'get_image_preview', 'short_description'),
            'description': (
                'Формат фото: JPG або PNG, рекомендований розмір 400×400 px (1:1). '
                'Фото та підпис відображаються на сторінці «Слухові апарати».'
            ),
        }),
    )

    def image_thumb(self, obj):
        return self.get_image_preview(obj)

    image_thumb.short_description = 'Фото'

    def caption_preview(self, obj):
        if not obj.short_description:
            return '—'
        if len(obj.short_description) <= 60:
            return obj.short_description
        return f'{obj.short_description[:57]}…'

    caption_preview.short_description = 'Підпис'


class ServiceAdmin(OrderOnCreateMixin, ModelAdmin):
    ordering_field = 'order'
    hide_ordering_field = True
    list_display = ('name', 'direction', 'price', 'is_active')
    list_editable = ('price', 'is_active')
    list_filter = ('direction', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    autocomplete_fields = ('direction',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'direction', 'short_description', 'description', 'is_active'),
        }),
        ('Ціна та тривалість', {
            'fields': ('price', 'price_note', 'duration_minutes'),
            'description': 'Ціна відображається на сторінці «Послуги та ціни».',
        }),
    )


class WorkingHoursAdmin(ModelAdmin):
    list_display = ('day_of_week', 'open_time', 'close_time', 'is_closed')


class AppointmentAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'direction', 'service', 'preferred_date', 'status', 'created_at')
    list_filter = ('status', 'direction', 'created_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('created_at', 'ip_address')
    autocomplete_fields = ('direction', 'service', 'doctor')
