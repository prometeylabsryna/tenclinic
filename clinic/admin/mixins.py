from django.db.models import Max
from django.utils.html import format_html
from unfold.admin import ModelAdmin


class OrderOnCreateMixin:
    order_field = 'order'

    def save_model(self, request, obj, form, change):
        if not change and hasattr(obj, self.order_field):
            current_max = obj.__class__.objects.aggregate(
                max_order=Max(self.order_field),
            )['max_order'] or 0
            setattr(obj, self.order_field, current_max + 1)
        super().save_model(request, obj, form, change)


class SingletonModelAdminMixin:
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        from django.urls import reverse

        obj = self.model.get_solo()
        return redirect(reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', args=[obj.pk]))


class ReadableUnfoldFieldsMixin:
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        from clinic.admin.widgets import apply_readable_widget
        return apply_readable_widget(formfield)


class ImagePreviewMixin:
    image_preview_field = 'image'
    image_preview_max_height = 80

    def get_image_preview(self, obj):
        image_field = getattr(obj, self.image_preview_field, None)
        if not image_field:
            return '—'
        return format_html(
            '<img src="{}" alt="" style="max-height:{}px;border-radius:6px;" />',
            image_field.url,
            self.image_preview_max_height,
        )

    get_image_preview.short_description = 'Превʼю'


class DoctorImagePreviewMixin(ImagePreviewMixin):
    image_preview_field = 'photo'
