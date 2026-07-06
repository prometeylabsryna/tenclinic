"""Рекомендовані розміри зображень для підказок у адмінці."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageSpec:
    label: str
    width: int
    height: int
    ratio: str
    hint: str

    @property
    def help_text(self) -> str:
        return (
            f'{self.hint} '
            f'Рекомендований розмір: {self.width}×{self.height} px ({self.ratio}). '
            f'Формат: JPG або PNG, оптимізований для веб.'
        )


SITE_LOGO = ImageSpec(
    label='Логотип',
    width=613,
    height=410,
    ratio='≈3:2',
    hint='Відображається у шапці та підвалі сайту.',
)

HERO_BRAND_MARK = ImageSpec(
    label='Логотип у заголовку hero',
    width=655,
    height=215,
    ratio='≈3:1',
    hint='Текстовий знак бренду поруч із заголовком на головній.',
)

HERO_BG = ImageSpec(
    label='Фон hero',
    width=1920,
    height=1280,
    ratio='3:2',
    hint='Велике фото праворуч у блоці hero.',
)

ABOUT_BRAND_MARK = ImageSpec(
    label='Знак бренду в секції «Про клініку»',
    width=560,
    height=170,
    ratio='≈3:1',
    hint='Декоративний логотип у темному блоці «Про клініку».',
)

DOCTOR_PHOTO = ImageSpec(
    label='Фото лікаря',
    width=360,
    height=408,
    ratio='15:17',
    hint='Портрет на картці лікаря та сторінці профілю.',
)

DIRECTION_IMAGE = ImageSpec(
    label='Зображення напрямку',
    width=480,
    height=576,
    ratio='5:6',
    hint='Мініатюра напрямку в каталозі та на головній.',
)

BLOCK_IMAGE_SPECS = {
    ('home', 'hero_brand_mark'): HERO_BRAND_MARK,
    ('home', 'hero_bg_image'): HERO_BG,
    ('home', 'about_brand_mark'): ABOUT_BRAND_MARK,
}

MODEL_IMAGE_SPECS = {
    'SiteSettings.logo': SITE_LOGO,
    'Direction.image': DIRECTION_IMAGE,
    'Doctor.photo': DOCTOR_PHOTO,
}


def block_image_help(page: str, key: str) -> str:
    spec = BLOCK_IMAGE_SPECS.get((page, key))
    return spec.help_text if spec else ''


def model_field_help(model_label: str, field_name: str) -> str:
    spec = MODEL_IMAGE_SPECS.get(f'{model_label}.{field_name}')
    return spec.help_text if spec else ''
