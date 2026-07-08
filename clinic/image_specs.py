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

ABOUT_US_BRAND_MARK = ImageSpec(
    label='Логотип у секції «Про нас»',
    width=560,
    height=170,
    ratio='≈3:1',
    hint='Чорний логотип TEN без фону на сторінці /about/.',
)

# Справа: слот розтягується на висоту текстової колонки, фото кадриться cover.
ABOUT_US_SIDE_PHOTO = ImageSpec(
    label='Фото справа «Про нас»',
    width=960,
    height=720,
    ratio='≈4:3',
    hint=(
        'Права колонка: слот підлаштовується під висоту тексту, '
        'фото обрізається по центру (object-fit: cover). '
        'Горизонтальне фото інтерʼєру/команда; важливий сюжет тримайте в центрі кадру. '
        'Не завантажуйте логотипи й широкі банери.'
    ),
)

# Знизу: фіксований CSS aspect-ratio 4/3.
ABOUT_US_BOTTOM_PHOTO = ImageSpec(
    label='Фото знизу «Про нас»',
    width=800,
    height=600,
    ratio='4:3',
    hint=(
        'Нижня сітка показує фото у фіксованому форматі 4:3. '
        'Горизонтальне фото інтерʼєру/команда; уникайте логотипів і широких банерів.'
    ),
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

HEARING_AID_IMAGE = ImageSpec(
    label='Фото слухового апарата',
    width=400,
    height=400,
    ratio='1:1',
    hint='Зображення на картці в каталозі слухових апаратів.',
)

BLOCK_IMAGE_SPECS = {
    ('home', 'hero_brand_mark'): HERO_BRAND_MARK,
    ('home', 'hero_bg_image'): HERO_BG,
    ('home', 'about_brand_mark'): ABOUT_BRAND_MARK,
    ('about_us', 'about_us_brand_mark'): ABOUT_US_BRAND_MARK,
    ('about_us', 'about_us_photo_1'): ABOUT_US_SIDE_PHOTO,
    ('about_us', 'about_us_photo_2'): ABOUT_US_SIDE_PHOTO,
    **{
        ('about_us', f'about_us_photo_{index}'): ABOUT_US_BOTTOM_PHOTO
        for index in range(3, 11)
    },
}

MODEL_IMAGE_SPECS = {
    'SiteSettings.logo': SITE_LOGO,
    'Direction.image': DIRECTION_IMAGE,
    'Doctor.photo': DOCTOR_PHOTO,
    'HearingAid.image': HEARING_AID_IMAGE,
}


def block_image_help(page: str, key: str) -> str:
    spec = BLOCK_IMAGE_SPECS.get((page, key))
    return spec.help_text if spec else ''


def model_field_help(model_label: str, field_name: str) -> str:
    spec = MODEL_IMAGE_SPECS.get(f'{model_label}.{field_name}')
    return spec.help_text if spec else ''
