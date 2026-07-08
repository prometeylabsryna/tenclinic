from dataclasses import dataclass, field
from typing import Optional

from clinic.block_defaults import PRINCIPLE_DEFAULTS


@dataclass(frozen=True)
class FieldGroup:
    title: str
    keys: tuple[str, ...]


@dataclass(frozen=True)
class ContentSection:
    slug: str
    page_slug: str
    title: str
    blocks: tuple[tuple[str, str], ...]
    sidebar_title: str = ''
    sidebar_icon: str = 'edit_note'
    preview_url: str = '/'
    description: str = ''
    visibility_key: str = ''
    field_groups: tuple[FieldGroup, ...] = field(default_factory=tuple)
    admin_model_name: str = ''


_PRINCIPLE_KEYS = tuple(
    key
    for index in PRINCIPLE_DEFAULTS
    for key in (f'principle_{index}_title', f'principle_{index}_text')
)

_PRINCIPLE_BLOCKS = tuple(('home', key) for key in _PRINCIPLE_KEYS)

_ABOUT_US_GALLERY_KEYS = tuple(f'about_us_photo_{index}' for index in range(1, 11))
_ABOUT_US_GALLERY_BLOCKS = tuple(('home', key) for key in _ABOUT_US_GALLERY_KEYS)


CONTENT_SECTIONS: tuple[ContentSection, ...] = (
    ContentSection(
        slug='hero',
        page_slug='home',
        title='Головна — Головний екран',
        sidebar_title='Головний екран',
        sidebar_icon='star',
        preview_url='/',
        description='Заголовок, текст, кнопки, фото та показники довіри на першому екрані.',
        visibility_key='hero_section_visible',
        admin_model_name='homeherosettings',
        field_groups=(
            FieldGroup('Відображення', ('hero_section_visible',)),
            FieldGroup('Тексти', (
                'hero_eyebrow', 'hero_title', 'hero_lead',
                'hero_btn_primary', 'hero_btn_secondary', 'hero_stat_label',
            )),
            FieldGroup('Фото', ('hero_brand_mark', 'hero_bg_image')),
            FieldGroup('Показники довіри', (
                'trust_directions_label', 'trust_doctors_label',
                'trust_visits_value', 'trust_visits_label',
                'trust_days_value', 'trust_days_label',
            )),
        ),
        blocks=(
            ('home', 'hero_section_visible'),
            ('home', 'hero_eyebrow'),
            ('home', 'hero_title'),
            ('home', 'hero_lead'),
            ('home', 'hero_btn_primary'),
            ('home', 'hero_btn_secondary'),
            ('home', 'hero_stat_label'),
            ('home', 'hero_brand_mark'),
            ('home', 'hero_bg_image'),
            ('home', 'trust_directions_label'),
            ('home', 'trust_doctors_label'),
            ('home', 'trust_visits_value'),
            ('home', 'trust_visits_label'),
            ('home', 'trust_days_value'),
            ('home', 'trust_days_label'),
        ),
    ),
    ContentSection(
        slug='about',
        page_slug='home',
        title='Головна — Про клініку',
        sidebar_title='Про клініку',
        sidebar_icon='info',
        preview_url='/',
        description='Тексти та зображення секції «Про клініку» і 10 принципів.',
        visibility_key='about_section_visible',
        admin_model_name='homeaboutsettings',
        field_groups=(
            FieldGroup('Відображення', ('about_section_visible',)),
            FieldGroup('Заголовки та текст', (
                'about_title', 'about_brand_note', 'about_text', 'principles_title',
            )),
            FieldGroup('Фото', ('about_brand_mark',)),
            FieldGroup('10 принципів', _PRINCIPLE_KEYS),
        ),
        blocks=(
            ('home', 'about_section_visible'),
            ('home', 'about_eyebrow'),
            ('home', 'about_title'),
            ('home', 'about_brand_note'),
            ('home', 'about_text'),
            ('home', 'about_brand_mark'),
            ('home', 'principles_title'),
            *_PRINCIPLE_BLOCKS,
        ),
    ),
    ContentSection(
        slug='about_us',
        page_slug='home',
        title='Головна — Про нас',
        sidebar_title='Про нас',
        sidebar_icon='photo_library',
        preview_url='/#about-us',
        description='Тексти, логотип і фотогалерея окремої секції «Про нас».',
        visibility_key='about_us_section_visible',
        admin_model_name='homeaboutussettings',
        field_groups=(
            FieldGroup('Відображення', ('about_us_section_visible',)),
            FieldGroup('Заголовки та текст', (
                'about_us_eyebrow', 'about_us_title', 'about_us_text',
            )),
            FieldGroup('Логотип', ('about_us_brand_mark',)),
            FieldGroup('Фото справа (2)', _ABOUT_US_GALLERY_KEYS[:2]),
            FieldGroup('Фото знизу (8)', _ABOUT_US_GALLERY_KEYS[2:]),
        ),
        blocks=(
            ('home', 'about_us_section_visible'),
            ('home', 'about_us_eyebrow'),
            ('home', 'about_us_title'),
            ('home', 'about_us_text'),
            ('home', 'about_us_brand_mark'),
            *_ABOUT_US_GALLERY_BLOCKS,
        ),
    ),
    ContentSection(
        slug='directions',
        page_slug='home',
        title='Головна — Напрямки',
        sidebar_title='Напрямки (головна)',
        sidebar_icon='category',
        preview_url='/',
        description='Заголовок секції напрямків. Картки редагуються в «Каталог → Напрямки».',
        visibility_key='directions_section_visible',
        admin_model_name='homedirectionssettings',
        blocks=(
            ('home', 'directions_section_visible'),
            ('home', 'directions_eyebrow'),
            ('home', 'directions_title'),
            ('home', 'directions_feature_badge'),
            ('home', 'directions_all_link'),
        ),
    ),
    ContentSection(
        slug='doctors',
        page_slug='home',
        title='Головна — Лікарі',
        sidebar_title='Лікарі (головна)',
        sidebar_icon='groups',
        preview_url='/',
        description='Заголовок секції лікарів. Профілі — в «Каталог → Лікарі».',
        visibility_key='doctors_section_visible',
        admin_model_name='homedoctorssettings',
        blocks=(
            ('home', 'doctors_section_visible'),
            ('home', 'doctors_eyebrow'),
            ('home', 'doctors_title'),
        ),
    ),
    ContentSection(
        slug='cta',
        page_slug='home',
        title='Головна — Запис (CTA)',
        sidebar_title='Запис на головній',
        sidebar_icon='campaign',
        preview_url='/',
        visibility_key='cta_section_visible',
        admin_model_name='homectasettings',
        blocks=(
            ('home', 'cta_section_visible'),
            ('home', 'cta_eyebrow'),
            ('home', 'cta_title'),
            ('home', 'cta_text'),
            ('home', 'cta_btn_primary'),
        ),
    ),
    ContentSection(
        slug='contacts',
        page_slug='home',
        title='Головна — Контакти',
        sidebar_title='Контакти (головна)',
        sidebar_icon='location_on',
        preview_url='/',
        description='Заголовок секції. Адреса та телефони — в «Налаштування → Сайт».',
        visibility_key='contacts_section_visible',
        admin_model_name='homecontactssettings',
        blocks=(
            ('home', 'contacts_section_visible'),
            ('home', 'contacts_eyebrow'),
            ('home', 'contacts_title'),
        ),
    ),
    ContentSection(
        slug='menu',
        page_slug='site',
        title='Меню та шапка',
        sidebar_title='Меню сайту',
        sidebar_icon='menu',
        preview_url='/',
        description='Назви пунктів навігації в шапці, мобільному меню та підвалі.',
        admin_model_name='sitemenusettings',
        field_groups=(
            FieldGroup('Пункти меню', (
                'nav_home', 'nav_directions', 'nav_doctors',
                'nav_services', 'nav_services_sub', 'nav_surgery',
                'nav_surgery_title', 'nav_contacts',
            )),
            FieldGroup('Кнопки', ('nav_cta', 'footer_copyright')),
        ),
        blocks=(
            ('site', 'nav_home'),
            ('site', 'nav_directions'),
            ('site', 'nav_doctors'),
            ('site', 'nav_services'),
            ('site', 'nav_services_sub'),
            ('site', 'nav_surgery'),
            ('site', 'nav_surgery_title'),
            ('site', 'nav_contacts'),
            ('site', 'nav_cta'),
            ('site', 'footer_copyright'),
        ),
    ),
    ContentSection(
        slug='directions_page',
        page_slug='directions',
        title='Сторінка «Напрямки»',
        sidebar_title='Сторінка напрямків',
        sidebar_icon='list_alt',
        preview_url='/directions/',
        description='Заголовки сторінки списку напрямків.',
        admin_model_name='directionspagesettings',
        blocks=(
            ('directions', 'page_eyebrow'),
            ('directions', 'page_title'),
            ('directions', 'page_lead'),
        ),
    ),
    ContentSection(
        slug='doctors_page',
        page_slug='doctors',
        title='Сторінка «Лікарі»',
        sidebar_title='Сторінка лікарів',
        sidebar_icon='badge',
        preview_url='/doctors/',
        admin_model_name='doctorspagesettings',
        blocks=(
            ('doctors', 'page_eyebrow'),
            ('doctors', 'page_title'),
            ('doctors', 'page_hint'),
        ),
    ),
    ContentSection(
        slug='services_page',
        page_slug='services',
        title='Сторінка «Послуги та ціни»',
        sidebar_title='Сторінка послуг',
        sidebar_icon='payments',
        preview_url='/services/',
        description='Ціни на послуги редагуються в «Каталог → Послуги».',
        admin_model_name='servicespagesettings',
        blocks=(
            ('services', 'page_eyebrow'),
            ('services', 'page_title'),
            ('services', 'page_note'),
        ),
    ),
    ContentSection(
        slug='contacts_page',
        page_slug='contacts',
        title='Сторінка «Контакти»',
        sidebar_title='Сторінка контактів',
        sidebar_icon='call',
        preview_url='/contacts/',
        description='Заголовки та підписи сторінки. Адреса, телефони, email і карта — лише в «Налаштування → Сайт».',
        admin_model_name='contactspagesettings',
        field_groups=(
            FieldGroup('Заголовки', ('page_eyebrow', 'page_title')),
            FieldGroup('Підписи полів', ('label_email', 'label_messengers')),
            FieldGroup('Графік і карта', (
                'schedule_title', 'today_label', 'map_title', 'route_btn',
            )),
        ),
        blocks=(
            ('contacts', 'page_eyebrow'),
            ('contacts', 'page_title'),
            ('contacts', 'label_email'),
            ('contacts', 'label_messengers'),
            ('contacts', 'schedule_title'),
            ('contacts', 'today_label'),
            ('contacts', 'map_title'),
            ('contacts', 'route_btn'),
        ),
    ),
    ContentSection(
        slug='booking',
        page_slug='booking',
        title='Сторінка «Запис»',
        sidebar_title='Форма запису',
        sidebar_icon='event',
        preview_url='/booking/',
        description='Тексти форми запису на прийом.',
        admin_model_name='bookingsettings',
        field_groups=(
            FieldGroup('Сторінка', ('page_title', 'page_lead')),
            FieldGroup('Поля форми', (
                'label_name', 'label_phone', 'label_email', 'label_direction',
                'direction_undecided', 'label_doctor', 'label_contact_intro',
                'label_contact_method', 'label_comment', 'placeholder_direction',
            )),
            FieldGroup('Кнопки та повідомлення', ('btn_submit', 'success_message')),
        ),
        blocks=(
            ('booking', 'page_title'),
            ('booking', 'page_lead'),
            ('booking', 'label_name'),
            ('booking', 'label_phone'),
            ('booking', 'label_email'),
            ('booking', 'label_direction'),
            ('booking', 'direction_undecided'),
            ('booking', 'label_doctor'),
            ('booking', 'label_contact_intro'),
            ('booking', 'label_contact_method'),
            ('booking', 'label_comment'),
            ('booking', 'placeholder_direction'),
            ('booking', 'btn_submit'),
            ('booking', 'success_message'),
        ),
    ),
    ContentSection(
        slug='privacy',
        page_slug='privacy',
        title='Політика конфіденційності',
        sidebar_title='Конфіденційність',
        sidebar_icon='policy',
        preview_url='/privacy/',
        admin_model_name='privacysettings',
        blocks=(
            ('privacy', 'page_title'),
            ('privacy', 'intro'),
            ('privacy', 'heading_data'),
            ('privacy', 'text_data'),
            ('privacy', 'heading_purpose'),
            ('privacy', 'text_purpose'),
            ('privacy', 'heading_storage'),
            ('privacy', 'text_storage'),
            ('privacy', 'heading_contact'),
            ('privacy', 'text_contact'),
        ),
    ),
    ContentSection(
        slug='surgical',
        page_slug='surgical',
        title='Хірургічні операції',
        sidebar_title='Хірургія',
        sidebar_icon='medical_services',
        preview_url='/surgical-operations/',
        admin_model_name='surgicalsettings',
        blocks=(
            ('surgical', 'page_eyebrow'),
            ('surgical', 'page_title'),
            ('surgical', 'page_lead'),
            ('surgical', 'filter_all'),
            ('surgical', 'placeholder_text'),
            ('surgical', 'placeholder_btn'),
        ),
    ),
    ContentSection(
        slug='hearing_aids',
        page_slug='hearing_aids',
        title='Слухові апарати',
        sidebar_title='Слухові апарати',
        sidebar_icon='hearing',
        preview_url='/hearing-aids/',
        description='Моделі та описи редагуються в «Каталог → Слухові апарати».',
        admin_model_name='hearingaidssettings',
        blocks=(
            ('hearing_aids', 'page_eyebrow'),
            ('hearing_aids', 'page_title'),
            ('hearing_aids', 'page_lead'),
            ('hearing_aids', 'empty_text'),
            ('hearing_aids', 'cta_btn'),
        ),
    ),
    ContentSection(
        slug='direction_detail',
        page_slug='direction',
        title='Сторінка напрямку (спільні тексти)',
        sidebar_title='Тексти напрямку',
        sidebar_icon='article',
        preview_url='/directions/',
        description='Спільні підписи для всіх детальних сторінок напрямків.',
        admin_model_name='directiondetailsettings',
        blocks=(
            ('direction', 'detail_eyebrow'),
            ('direction', 'detail_desc_heading'),
            ('direction', 'detail_when_heading'),
            ('direction', 'detail_services_heading'),
            ('direction', 'detail_btn_consultation'),
            ('direction', 'detail_btn_surgery'),
            ('direction', 'detail_btn_hearing_aids'),
            ('direction', 'detail_doctors_heading'),
            ('direction', 'detail_cta_text'),
            ('direction', 'detail_cta_btn'),
        ),
    ),
)


def all_registry_block_keys():
    keys = set()
    for section in CONTENT_SECTIONS:
        keys.update(section.blocks)
    return keys


def get_section_by_slug(page_slug: str, section_slug: str) -> Optional[ContentSection]:
    for section in CONTENT_SECTIONS:
        if section.page_slug == page_slug and section.slug == section_slug:
            return section
    return None


def build_content_sidebar_items():
    from django.urls import reverse_lazy

    return [
        {
            'title': section.sidebar_title or section.title,
            'icon': section.sidebar_icon,
            'link': reverse_lazy(f'admin:clinic_{section.admin_model_name}_changelist'),
        }
        for section in CONTENT_SECTIONS
    ]
