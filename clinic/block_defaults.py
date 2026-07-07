from clinic.models.site import SiteBlock

PRINCIPLE_DEFAULTS = {
    1: ('Точність', 'Кожне рішення ґрунтується на знаннях, досвіді та деталях.'),
    2: ('Безпека', 'Безпека пацієнта є нашим безумовним пріоритетом.'),
    3: ('Доказовість', 'Ми використовуємо лише сучасні міжнародні стандарти та протоколи.'),
    4: ('Партнерство', 'Лікар і пацієнт приймають рішення разом.'),
    5: ('Індивідуальність', 'Кожен пацієнт потребує персоналізованого підходу.'),
    6: ('Інновації', 'Ми впроваджуємо новітні медичні та хірургічні технології.'),
    7: ('Турбота', 'Повага, емпатія та людяність є невід\'ємною частиною лікування.'),
    8: ('Безперервний супровід', 'Ми поруч із пацієнтом на кожному етапі лікування та відновлення.'),
    9: ('Досконалість', 'Ми прагнемо найкращого функціонального та естетичного результату.'),
    10: ('Результат', 'Якість лікування оцінюється результатом і якістю життя пацієнта.'),
}

BLOCK_DEFAULTS = {
    ('home', 'hero_section_visible'): '1',
    ('home', 'hero_eyebrow'): 'Приватна клініка · Київ',
    ('home', 'hero_title'): 'TEN clinic — новий стандарт медичної допомоги',
    ('home', 'hero_lead'): (
        'Місце, де сучасна медицина працює так, як вона повинна: професійно, чесно, '
        'доказово та з повагою до кожного пацієнта. Ми не просто лікуємо — ми формуємо '
        'новий стандарт медичної допомоги.'
    ),
    ('home', 'hero_btn_primary'): 'Записатися',
    ('home', 'hero_btn_secondary'): 'Напрямки лікування',
    ('home', 'hero_stat_label'): 'Занесення медичних висновків в ЕСОЗ',
    ('home', 'trust_directions_label'): 'медичних напрямків',
    ('home', 'trust_doctors_label'): 'лікарів-експертів',
    ('home', 'trust_visits_value'): '12k',
    ('home', 'trust_visits_label'): 'візитів на рік',
    ('home', 'trust_days_value'): '7',
    ('home', 'trust_days_label'): 'днів на тиждень',
    ('home', 'about_section_visible'): '1',
    ('home', 'about_eyebrow'): 'Про клініку',
    ('home', 'about_title'): 'Медицина, якій довіряють',
    ('home', 'about_brand_note'): 'десять принципів, на яких тримається наша якість',
    ('home', 'about_text'): (
        'Ми команда лікарів, які створили сучасний медичний центр, де пацієнт отримує '
        'достатньо часу для консультації, зрозумілі пояснення та індивідуальний підхід. '
        'Ми обʼєднали лікарів різних спеціальностей, сучасне діагностичне обладнання та '
        'принципи доказової медицини, щоб забезпечити якісну медичну допомогу для дітей і дорослих.'
    ),
    ('home', 'principles_title'): '10 принципів TEN clinic',
    ('home', 'directions_title'): 'Від діагностики до хірургії',
    ('home', 'directions_eyebrow'): 'Напрямки',
    ('home', 'directions_feature_badge'): 'Флагманський напрямок',
    ('home', 'directions_all_link'): 'Усі напрямки →',
    ('home', 'directions_section_visible'): '1',
    ('home', 'doctors_section_visible'): '1',
    ('home', 'doctors_eyebrow'): 'Лікарі',
    ('home', 'doctors_title'): 'Команда, якій ви довіряєте здоровʼя',
    ('home', 'cta_section_visible'): '1',
    ('home', 'cta_eyebrow'): 'Запис на консультацію',
    ('home', 'cta_title'): 'Потрібна консультація?',
    ('home', 'cta_text'): 'Залиште заявку — адміністратор передзвонить і підбере зручний час.',
    ('home', 'cta_btn_primary'): 'Записатися онлайн',
    ('home', 'contacts_section_visible'): '1',
    ('home', 'contacts_eyebrow'): 'Контакти',
    ('home', 'contacts_title'): 'Контакти',
    ('site', 'nav_home'): 'Головна',
    ('site', 'nav_directions'): 'Напрямки',
    ('site', 'nav_doctors'): 'Лікарі',
    ('site', 'nav_services'): 'Послуги',
    ('site', 'nav_services_sub'): 'та ціни',
    ('site', 'nav_surgery'): 'Хірургія',
    ('site', 'nav_surgery_title'): 'Хірургічні операції',
    ('site', 'nav_contacts'): 'Контакти',
    ('site', 'nav_cta'): 'Записатися',
    ('site', 'footer_copyright'): 'TEN clinic',
    ('directions', 'page_eyebrow'): 'Напрямки',
    ('directions', 'page_title'): 'Оберіть напрямок лікування',
    ('directions', 'page_lead'): 'Діагностика та лікування вуха, горла, носа та слуху для дітей і дорослих',
    ('doctors', 'page_eyebrow'): 'Лікарі',
    ('doctors', 'page_title'): 'Команда, якій ви довіряєте здоровʼя',
    ('doctors', 'page_hint'): 'Гортайте →',
    ('services', 'page_eyebrow'): 'Послуги та ціни',
    ('services', 'page_title'): 'Каталог послуг і цін',
    ('services', 'page_note'): 'Ціни вказані за прайсом клініки. Актуальну вартість уточнюйте при записі.',
    ('contacts', 'page_eyebrow'): 'Контакти',
    ('contacts', 'page_title'): 'Контакти',
    ('contacts', 'schedule_title'): 'Графік роботи',
    ('contacts', 'today_label'): 'Сьогодні:',
    ('contacts', 'map_title'): 'Схема проїзду',
    ('contacts', 'route_btn'): 'Прокласти маршрут',
    ('contacts', 'label_email'): 'Email',
    ('contacts', 'label_messengers'): 'Месенджери',
    ('booking', 'page_title'): 'Запис на прийом',
    ('booking', 'page_lead'): 'Заповніть форму — адміністратор підтвердить запис найближчим часом.',
    ('booking', 'label_name'): 'ПІБ',
    ('booking', 'label_phone'): 'Телефон',
    ('booking', 'label_email'): 'Email',
    ('booking', 'label_direction'): 'Напрямок',
    ('booking', 'direction_undecided'): 'Не можу визначитися',
    ('booking', 'label_doctor'): 'Лікар',
    ('booking', 'label_contact_intro'): 'Для узгодження дати та часу візиту Адміністратор незабаром звʼяжеться з Вами.',
    ('booking', 'label_contact_method'): 'Оберіть зручний спосіб звʼязку:',
    ('booking', 'label_comment'): 'Коментар',
    ('booking', 'placeholder_direction'): 'Оберіть напрямок',
    ('booking', 'btn_submit'): 'Надіслати заявку',
    ('booking', 'success_message'): (
        'Дякуємо! Вашу заявку отримано. Адміністратор звʼяжеться з вами найближчим часом.'
    ),
    ('privacy', 'page_title'): 'Політика конфіденційності',
    ('privacy', 'intro'): (
        'TEN clinic поважає вашу конфіденційність і обробляє персональні дані '
        'відповідно до чинного законодавства України.'
    ),
    ('privacy', 'heading_data'): 'Які дані ми збираємо',
    ('privacy', 'text_data'): (
        'Під час запису на прийом ми можемо отримати ваше імʼя, номер телефону, email '
        'та інформацію про бажану послугу.'
    ),
    ('privacy', 'heading_purpose'): 'Мета обробки',
    ('privacy', 'text_purpose'): (
        'Дані використовуються для організації запису, звʼязку з вами та надання медичних послуг.'
    ),
    ('privacy', 'heading_storage'): 'Зберігання та захист',
    ('privacy', 'text_storage'): (
        'Ми застосовуємо організаційні та технічні заходи для захисту ваших персональних '
        'даних від несанкціонованого доступу.'
    ),
    ('privacy', 'heading_contact'): 'Контакти',
    ('privacy', 'text_contact'): 'З питань обробки персональних даних звертайтеся:',
    ('surgical', 'page_eyebrow'): 'Хірургія',
    ('surgical', 'page_title'): 'Хірургічні операції',
    ('surgical', 'page_lead'): (
        'Амбулаторні та планові втручання з повним перед- та післяопераційним супроводом.'
    ),
    ('surgical', 'filter_all'): 'Усі напрямки',
    ('surgical', 'placeholder_text'): (
        'Розділ наповнюється. Незабаром тут зʼявиться каталог хірургічних операцій.'
    ),
    ('surgical', 'placeholder_btn'): 'Записатися на консультацію',
    ('hearing_aids', 'page_eyebrow'): 'Сурдологія',
    ('hearing_aids', 'page_title'): 'Слухові апарати',
    ('hearing_aids', 'page_lead'): (
        'Сучасні моделі з індивідуальним підбором, налаштуванням та супроводом у TEN clinic.'
    ),
    ('hearing_aids', 'empty_text'): (
        'Каталог наповнюється. Зверніться до адміністратора для консультації щодо доступних моделей.'
    ),
    ('hearing_aids', 'cta_btn'): 'Записатися на підбір',
    ('direction', 'detail_eyebrow'): 'Напрямок',
    ('direction', 'detail_desc_heading'): 'Опис',
    ('direction', 'detail_when_heading'): 'Коли варто звернутися?',
    ('direction', 'detail_services_heading'): 'Наші послуги',
    ('direction', 'detail_btn_consultation'): 'Консультативно-діагностичний прийом',
    ('direction', 'detail_btn_surgery'): 'Хірургічна допомога',
    ('direction', 'detail_btn_hearing_aids'): 'Слухові апарати',
    ('direction', 'detail_doctors_heading'): 'Лікарі напрямку',
    ('direction', 'detail_cta_text'): 'Запишіться на консультацію — підберемо зручний час прийому.',
    ('direction', 'detail_cta_btn'): 'Записатися на прийом',
}

for index, (title, text) in PRINCIPLE_DEFAULTS.items():
    BLOCK_DEFAULTS[('home', f'principle_{index}_title')] = title
    BLOCK_DEFAULTS[('home', f'principle_{index}_text')] = text

BLOCK_FIELD_LABELS = {
    'hero_section_visible': 'Показувати головний екран (hero)',
    'hero_eyebrow': 'Рядок над заголовком (наприклад, місто)',
    'hero_title': 'Заголовок головного екрану',
    'hero_lead': 'Основний текст під заголовком',
    'hero_btn_primary': 'Кнопка «Записатися»',
    'hero_btn_secondary': 'Кнопка «Напрямки»',
    'hero_stat_label': 'Підпис біля іконки ЄСОЗ',
    'hero_brand_mark': 'Зображення логотипу в заголовку',
    'hero_bg_image': 'Фонове фото hero',
    'trust_directions_label': 'Підпис: кількість напрямків',
    'trust_doctors_label': 'Підпис: кількість лікарів',
    'trust_visits_value': 'Число візитів (наприклад, 12k)',
    'trust_visits_label': 'Підпис до візитів',
    'trust_days_value': 'Число днів роботи (наприклад, 7)',
    'trust_days_label': 'Підпис до днів роботи',
    'about_section_visible': 'Показувати секцію «Про клініку»',
    'about_eyebrow': 'Мітка над заголовком',
    'about_title': 'Заголовок «Про клініку»',
    'about_brand_note': 'Підпис бренду',
    'about_text': 'Основний текст про клініку',
    'about_brand_mark': 'Зображення знаку бренду',
    'principles_title': 'Заголовок блоку принципів',
    'directions_title': 'Заголовок секції напрямків',
    'directions_eyebrow': 'Мітка над заголовком напрямків',
    'directions_feature_badge': 'Бейдж на картці напрямку',
    'directions_all_link': 'Посилання «Усі напрямки»',
    'directions_section_visible': 'Показувати напрямки на головній',
    'doctors_section_visible': 'Показувати лікарів на головній',
    'doctors_eyebrow': 'Мітка над заголовком лікарів',
    'doctors_title': 'Заголовок секції лікарів',
    'cta_section_visible': 'Показувати блок запису (CTA)',
    'cta_eyebrow': 'Мітка над CTA',
    'cta_title': 'Заголовок CTA',
    'cta_text': 'Текст CTA',
    'cta_btn_primary': 'Кнопка CTA «Записатися онлайн»',
    'contacts_section_visible': 'Показувати контакти на головній',
    'contacts_eyebrow': 'Мітка над контактами',
    'contacts_title': 'Заголовок контактів на головній',
    'nav_home': 'Пункт меню: Головна',
    'nav_directions': 'Пункт меню: Напрямки',
    'nav_doctors': 'Пункт меню: Лікарі',
    'nav_services': 'Пункт меню: Послуги (верхній рядок)',
    'nav_services_sub': 'Пункт меню: та ціни (нижній рядок)',
    'nav_surgery': 'Пункт меню: Хірургія (коротко)',
    'nav_surgery_title': 'Підказка при наведенні на «Хірургія»',
    'nav_contacts': 'Пункт меню: Контакти',
    'nav_cta': 'Кнопка «Записатися» в меню',
    'footer_copyright': 'Назва в копірайті підвалі',
    'page_eyebrow': 'Маленький заголовок над назвою сторінки',
    'page_title': 'Заголовок сторінки',
    'page_lead': 'Вступний текст сторінки',
    'page_hint': 'Підказка для користувача',
    'page_note': 'Примітка під заголовком',
    'schedule_title': 'Заголовок «Графік роботи»',
    'today_label': 'Підпис «Сьогодні»',
    'map_title': 'Заголовок блоку карти',
    'route_btn': 'Текст кнопки маршруту',
    'label_email': 'Підпис поля «Email»',
    'label_messengers': 'Підпис «Месенджери»',
    'label_name': 'Підпис «ПІБ»',
    'label_phone': 'Підпис «Телефон»',
    'label_email': 'Підпис «Email»',
    'label_direction': 'Підпис «Напрямок»',
    'direction_undecided': 'Пункт «Не можу визначитися»',
    'label_doctor': 'Підпис «Лікар»',
    'label_contact_intro': 'Текст про звʼязок адміністратора',
    'label_contact_method': 'Підпис «Спосіб звʼязку»',
    'label_comment': 'Підпис «Коментар»',
    'placeholder_direction': 'Плейсхолдер вибору напрямку',
    'btn_submit': 'Текст кнопки відправки форми',
    'success_message': 'Повідомлення після успішного запису',
    'intro': 'Вступний абзац',
    'heading_data': 'Заголовок: які дані збираємо',
    'text_data': 'Текст: які дані збираємо',
    'heading_purpose': 'Заголовок: мета обробки',
    'text_purpose': 'Текст: мета обробки',
    'heading_storage': 'Заголовок: зберігання',
    'text_storage': 'Текст: зберігання',
    'heading_contact': 'Заголовок: контакти',
    'text_contact': 'Текст: контакти',
    'filter_all': 'Фільтр «Усі напрямки»',
    'placeholder_text': 'Текст-заглушка розділу',
    'placeholder_btn': 'Кнопка в заглушці',
    'detail_eyebrow': 'Мітка «Напрямок»',
    'detail_desc_heading': 'Заголовок «Опис»',
    'detail_when_heading': 'Заголовок «Коли звернутися»',
    'detail_services_heading': 'Заголовок «Наші послуги»',
    'detail_btn_consultation': 'Кнопка консультації',
    'detail_btn_surgery': 'Кнопка хірургії',
    'detail_btn_hearing_aids': 'Кнопка «Слухові апарати»',
    'detail_doctors_heading': 'Заголовок «Лікарі напрямку»',
    'detail_cta_text': 'Текст бокового блоку запису',
    'detail_cta_btn': 'Кнопка запису на сторінці напрямку',
}

for index in PRINCIPLE_DEFAULTS:
    BLOCK_FIELD_LABELS[f'principle_{index}_title'] = f'Принцип {index:02d} — назва'
    BLOCK_FIELD_LABELS[f'principle_{index}_text'] = f'Принцип {index:02d} — опис'

INLINE_KEYS = frozenset({
    'hero_title', 'hero_eyebrow', 'hero_btn_primary', 'hero_btn_secondary',
    'cta_title', 'cta_eyebrow', 'cta_btn_primary', 'about_title', 'about_eyebrow', 'about_brand_note', 'principles_title',
    'directions_title', 'directions_eyebrow', 'directions_feature_badge', 'directions_all_link',
    'doctors_title', 'doctors_eyebrow', 'contacts_title', 'contacts_eyebrow',
    'trust_directions_label', 'trust_doctors_label', 'trust_visits_value',
    'trust_visits_label', 'trust_days_value', 'trust_days_label',
    'nav_home', 'nav_directions', 'nav_doctors', 'nav_services', 'nav_services_sub',
    'nav_surgery', 'nav_surgery_title', 'nav_contacts', 'nav_cta', 'footer_copyright',
    'page_eyebrow', 'page_title', 'page_hint', 'schedule_title', 'today_label',
    'map_title', 'route_btn', 'filter_all', 'placeholder_btn', 'cta_btn',
    'label_email', 'label_phone',
    'label_messengers', 'label_name', 'label_direction', 'label_service',
    'label_doctor', 'label_date', 'label_time', 'label_comment',
    'placeholder_direction', 'btn_submit',
    'heading_data', 'heading_purpose', 'heading_storage', 'heading_contact',
    'detail_eyebrow', 'detail_desc_heading', 'detail_when_heading',
    'detail_services_heading', 'detail_btn_consultation', 'detail_btn_surgery',
    'detail_btn_hearing_aids',
    'detail_doctors_heading', 'detail_cta_btn',
    *(f'principle_{index}_title' for index in PRINCIPLE_DEFAULTS),
})

MULTILINE_KEYS = frozenset({
    'hero_lead', 'about_text', 'cta_text', 'success_message', 'hero_stat_label',
    'page_lead', 'page_note', 'intro', 'text_data', 'text_purpose', 'text_storage',
    'text_contact', 'placeholder_text', 'detail_cta_text', 'empty_text',
    *(f'principle_{index}_text' for index in PRINCIPLE_DEFAULTS),
})

BLOCK_CONTENT_TYPES = {
    ('home', 'hero_brand_mark'): SiteBlock.ContentType.IMAGE,
    ('home', 'hero_bg_image'): SiteBlock.ContentType.IMAGE,
    ('home', 'about_brand_mark'): SiteBlock.ContentType.IMAGE,
}

VISIBILITY_KEYS = frozenset({
    'hero_section_visible', 'about_section_visible', 'directions_section_visible',
    'doctors_section_visible', 'cta_section_visible', 'contacts_section_visible',
})


def is_image_block(page: str, key: str) -> bool:
    return (page, key) in BLOCK_CONTENT_TYPES


def is_visibility_key(key: str) -> bool:
    return key.endswith('_visible')
