from django import forms
from django.contrib import admin, messages
from django.contrib.admin.helpers import AdminForm
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.conf import settings
from unfold.admin import ModelAdmin
from unfold.widgets import (
    UnfoldAdminImageFieldWidget,
    UnfoldAdminTextInputWidget,
    UnfoldAdminTextareaWidget,
    UnfoldBooleanWidget,
)

from clinic.admin.mixins import ReadableUnfoldFieldsMixin, SingletonModelAdminMixin
from clinic.block_defaults import (
    BLOCK_CONTENT_TYPES,
    BLOCK_DEFAULTS,
    BLOCK_FIELD_LABELS,
    INLINE_KEYS,
    MULTILINE_KEYS,
    block_field_label,
    is_image_block,
    is_visibility_key,
)
from clinic.image_specs import block_image_help
from clinic.models import SiteBlock, SiteSettings
from clinic.site_content_registry import CONTENT_SECTIONS, ContentSection, get_section_by_slug


def ensure_block(page, key):
    default = BLOCK_DEFAULTS.get((page, key), '')
    label = block_field_label(page, key)
    content_type = BLOCK_CONTENT_TYPES.get((page, key), SiteBlock.ContentType.TEXT)
    block, _ = SiteBlock.objects.get_or_create(
        page=page,
        key=key,
        defaults={'label': label, 'text_html': default, 'content_type': content_type},
    )
    return block


def _field_name_for_block(page, key):
    if is_visibility_key(key):
        return f'block__{page}__{key}__visible'
    if is_image_block(page, key):
        return f'block__{page}__{key}__image'
    return f'block__{page}__{key}__text_html'


def _resolve_block_key(field_name):
    parts = field_name.split('__')
    if len(parts) < 4:
        return None, None
    return parts[1], parts[2]


class SitePageContentForm(forms.Form):
    section_visible = forms.BooleanField(
        required=False,
        label='Показувати секцію на сайті',
        widget=UnfoldBooleanWidget,
    )

    def __init__(self, section, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.section = section
        for page, key in section.blocks:
            if section.visibility_key and key == section.visibility_key:
                continue
            block = ensure_block(page, key)
            if is_visibility_key(key):
                self.fields[_field_name_for_block(page, key)] = forms.BooleanField(
                    required=False,
                    label=block_field_label(page, key),
                    initial=block.text_html == '1',
                    widget=UnfoldBooleanWidget,
                )
                continue
            if is_image_block(page, key):
                help_text = block_image_help(page, key)
                if block.image:
                    help_text = f'Поточне фото завантажено. {help_text}'
                self.fields[_field_name_for_block(page, key)] = forms.ImageField(
                    required=False,
                    label=block_field_label(page, key),
                    help_text=help_text,
                    widget=UnfoldAdminImageFieldWidget,
                )
                if block.image:
                    self.initial[_field_name_for_block(page, key)] = block.image
                continue
            field_name = _field_name_for_block(page, key)
            if key in INLINE_KEYS:
                widget = UnfoldAdminTextInputWidget
            elif key in MULTILINE_KEYS:
                widget = UnfoldAdminTextareaWidget
            else:
                widget = UnfoldAdminTextareaWidget
            self.fields[field_name] = forms.CharField(
                required=False,
                label=block_field_label(page, key),
                initial=block.text_html,
                widget=widget(attrs={'rows': 4 if key in MULTILINE_KEYS else 2}),
            )
        if section.visibility_key:
            vis = ensure_block(section.page_slug, section.visibility_key)
            self.fields['section_visible'].initial = vis.text_html == '1'

    def save(self):
        if self.section.visibility_key:
            vis = ensure_block(self.section.page_slug, self.section.visibility_key)
            vis.text_html = '1' if self.cleaned_data.get('section_visible') else '0'
            vis.save()
        for name, value in self.cleaned_data.items():
            if name == 'section_visible':
                continue
            page, key = _resolve_block_key(name)
            if not page:
                continue
            if name.endswith('__visible'):
                block = ensure_block(page, key)
                block.text_html = '1' if value else '0'
                block.save()
            elif name.endswith('__image'):
                block = ensure_block(page, key)
                if value is False:
                    if block.image:
                        block.image.delete(save=False)
                    block.image = None
                elif value:
                    block.image = value
                block.content_type = SiteBlock.ContentType.IMAGE
                block.save()
            elif name.endswith('__text_html'):
                block = ensure_block(page, key)
                block.text_html = value
                block.save()
        cache.delete(settings.SITE_BLOCKS_CACHE_KEY)


def build_form_field_groups(section: ContentSection, form: SitePageContentForm):
    assigned = set()
    groups = []
    visibility_in_group = False

    def append_field(fields, page, key):
        nonlocal visibility_in_group
        if section.visibility_key and key == section.visibility_key:
            if 'section_visible' in form.fields and (page, key) not in assigned:
                fields.append(form['section_visible'])
                assigned.add((page, key))
                visibility_in_group = True
            return
        field_name = _field_name_for_block(page, key)
        if field_name in form.fields:
            bound = form[field_name]
            fields.append(bound)
            assigned.add((page, key))

    if section.field_groups:
        for group in section.field_groups:
            fields = []
            for key in group.keys:
                for page, block_key in section.blocks:
                    if block_key == key:
                        append_field(fields, page, block_key)
            if fields:
                groups.append({'title': group.title, 'fields': fields, 'hint': ''})
    else:
        fields = []
        for page, key in section.blocks:
            if section.visibility_key and key == section.visibility_key:
                continue
            if is_visibility_key(key):
                continue
            if (page, key) in assigned:
                continue
            append_field(fields, page, key)
        if fields:
            groups.append({'title': 'Вміст', 'fields': fields, 'hint': ''})

    if section.visibility_key and not visibility_in_group and 'section_visible' in form.fields:
        groups.insert(0, {
            'title': 'Відображення на сайті',
            'fields': [form['section_visible']],
            'hint': 'Вимкніть, щоб приховати всю секцію.',
        })

    leftover = []
    for page, key in section.blocks:
        if (page, key) in assigned:
            continue
        if section.visibility_key and key == section.visibility_key:
            continue
        append_field(leftover, page, key)
    if leftover:
        groups.append({'title': 'Додатково', 'fields': leftover, 'hint': ''})

    return groups


def build_content_admin_fieldsets(field_groups):
    fieldsets = []
    for group in field_groups:
        fieldsets.append((
            group['title'],
            {
                'fields': [field.name for field in group['fields']],
                'description': group.get('hint') or '',
            },
        ))
    return fieldsets


def build_content_admin_context(request, admin_instance, section, form, field_groups):
    fieldsets = build_content_admin_fieldsets(field_groups)
    adminform = AdminForm(
        form,
        fieldsets,
        prepopulated_fields={},
        readonly_fields=(),
        model_admin=admin_instance,
    )
    return {
        **admin_instance.admin_site.each_context(request),
        'title': section.title,
        'subtitle': section.description,
        'section': section,
        'form': form,
        'field_groups': field_groups,
        'preview_url': section.preview_url,
        'opts': admin_instance.model._meta,
        'add': False,
        'change': True,
        'is_popup': False,
        'save_as': False,
        'show_save': True,
        'show_save_and_continue': False,
        'show_save_and_add_another': False,
        'has_add_permission': admin_instance.has_add_permission(request),
        'has_change_permission': admin_instance.has_change_permission(request),
        'has_view_permission': admin_instance.has_change_permission(request),
        'has_delete_permission': False,
        'has_editable_inline_admin_formsets': False,
        'has_file_field': form.is_multipart(),
        'adminform': adminform,
        'errors': adminform.errors,
        'inline_admin_formsets': [],
        'original': None,
        'media': adminform.media,
        'preserved_filters': '',
    }


class SiteContentSectionAdmin(SingletonModelAdminMixin, ReadableUnfoldFieldsMixin, ModelAdmin):
    page_slug = ''
    section_slug = ''

    def has_module_permission(self, request):
        return request.user.is_staff

    def changelist_view(self, request, extra_context=None):
        section = get_section_by_slug(self.page_slug, self.section_slug)
        if not section:
            return redirect('admin:index')
        if request.method == 'POST':
            form = SitePageContentForm(section, request.POST, request.FILES)
            if form.is_valid():
                form.save()
                self.message_user(request, 'Зміни збережено.')
                return redirect(request.path)
            self.message_user(
                request,
                'Не вдалося зберегти. Перевірте формат файлів і розмір зображень.',
                level=messages.ERROR,
            )
        else:
            form = SitePageContentForm(section)
        field_groups = build_form_field_groups(section, form)
        context = build_content_admin_context(request, self, section, form, field_groups)
        return render(request, 'admin/site_content_page.html', context)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return False


def register_site_content_section_admins():
    for section in CONTENT_SECTIONS:
        model_name = section.admin_model_name.title().replace(' ', '')
        meta = type('Meta', (), {
            'proxy': True,
            'verbose_name': section.title,
            'verbose_name_plural': section.title,
        })
        proxy_model = type(
            model_name,
            (SiteSettings,),
            {
                '__module__': 'clinic.models.site',
                'Meta': meta,
            },
        )
        admin_class = type(
            f'{model_name}Admin',
            (SiteContentSectionAdmin,),
            {
                'page_slug': section.page_slug,
                'section_slug': section.slug,
            },
        )
        try:
            admin.site.register(proxy_model, admin_class)
        except admin.sites.AlreadyRegistered:
            pass
