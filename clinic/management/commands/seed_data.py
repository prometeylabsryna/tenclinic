from datetime import time

from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings

from clinic.block_defaults import BLOCK_DEFAULTS, BLOCK_FIELD_LABELS, is_visibility_key
from clinic.models import Direction, Doctor, HearingAid, Service, SiteBlock, SiteSettings, WorkingHours


class Command(BaseCommand):
    help = (
        'Seed TEN clinic demo data. На production не перезаписує SiteSettings і CMS-блоки, '
        'якщо вони вже є. Для повного скидання — --force.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перезаписати SiteSettings, CMS-блоки та демо-записи',
        )

    def handle(self, *args, **options):
        force = options['force']
        self._seed_settings(force=force)
        self._seed_blocks(force=force)
        self._seed_working_hours(force=force)
        directions = self._seed_directions(force=force)
        self._seed_services(directions, force=force)
        self._seed_hearing_aids(force=force)
        self._seed_doctors(directions, force=force)
        cache.delete(settings.SITE_BLOCKS_CACHE_KEY)
        self.stdout.write(self.style.SUCCESS('Seed completed.'))

    def _seed_settings(self, *, force=False):
        defaults = {
            'site_name': 'TEN clinic',
            'tagline': 'Medicine & Surgery',
            'address': 'м. Київ, вул. Хрещатик, 1',
            'phone_primary': '+38 (044) 123-45-67',
            'email': 'info@tenclinic.ua',
            'notification_email': 'admin@tenclinic.ua',
            'meta_description': 'TEN clinic — новий стандарт медичної допомоги. Medicine & Surgery.',
            'directions_text': 'Клініка розташована в центрі міста. Парковка біля будівлі.',
            'map_lat': '50.447387',
            'map_lng': '30.524876',
            'map_embed_url': (
                'https://maps.google.com/maps?q=50.447387,30.524876&hl=uk&z=16&output=embed'
            ),
        }
        if SiteSettings.objects.filter(pk=1).exists() and not force:
            self.stdout.write('SiteSettings already exists — skip (use --force to overwrite).')
            return
        SiteSettings.objects.update_or_create(pk=1, defaults=defaults)

    def _seed_blocks(self, *, force=False):
        from clinic.block_defaults import BLOCK_CONTENT_TYPES
        from clinic.site_content_registry import all_registry_block_keys

        keys = all_registry_block_keys() | set(BLOCK_DEFAULTS.keys())
        for page, key in keys:
            default = BLOCK_DEFAULTS.get((page, key), '')
            if is_visibility_key(key) and not default:
                default = '1'
            block_defaults = {
                'label': BLOCK_FIELD_LABELS.get(key, key),
                'text_html': default,
                'content_type': BLOCK_CONTENT_TYPES.get(
                    (page, key),
                    SiteBlock.ContentType.TEXT,
                ),
            }
            if force:
                SiteBlock.objects.update_or_create(
                    page=page,
                    key=key,
                    defaults=block_defaults,
                )
                continue
            SiteBlock.objects.get_or_create(
                page=page,
                key=key,
                defaults=block_defaults,
            )

    def _seed_working_hours(self, *, force=False):
        if WorkingHours.objects.exists() and not force:
            return
        schedule = [
            (0, time(9, 0), time(18, 0), False),
            (1, time(9, 0), time(18, 0), False),
            (2, time(9, 0), time(18, 0), False),
            (3, time(9, 0), time(18, 0), False),
            (4, time(9, 0), time(18, 0), False),
            (5, time(9, 0), time(14, 0), False),
            (6, None, None, True),
        ]
        for day, open_t, close_t, closed in schedule:
            WorkingHours.objects.update_or_create(
                day_of_week=day,
                defaults={'open_time': open_t, 'close_time': close_t, 'is_closed': closed},
            )

    def _seed_directions(self, *, force=False):
        demo_slugs = [
            'zagalna-hirurgiya',
            'cherevna-hirurgiya',
            'terapiya',
            'diagnostyka',
            'plastychna-hirurgiya',
            'profilaktyka',
        ]
        Direction.objects.filter(slug__in=demo_slugs).update(is_active=False)

        lor_data = [
            {
                'slug': 'dytacha-otolaryngologiya',
                'name': 'Дитяча отоларингологія',
                'short_description': (
                    'Діагностика, лікування та профілактика захворювань вуха, горла й носа у дітей '
                    'від народження до 18 років. Делікатний підхід, сучасні методи обстеження '
                    'та лікування з урахуванням вікових особливостей дитини.'
                ),
                'description': (
                    'Дитяча отоларингологія — це напрямок медицини, який займається діагностикою, '
                    'лікуванням і профілактикою захворювань вуха, горла, носа та суміжних органів у '
                    'дітей від народження до 18 років. ЛОР-захворювання в дитячому віці мають свої '
                    'особливості, тому потребують своєчасної діагностики та лікування з урахуванням '
                    'віку дитини.'
                ),
                'when_to_visit': '\n'.join([
                    'утруднене носове дихання',
                    'тривалий або частий нежить',
                    'часті отити',
                    'біль у вусі',
                    'виділення з вуха',
                    'зниження слуху або підозра на його погіршення',
                    'біль у горлі',
                    'часті ангіни',
                    'хропіння або зупинки дихання під час сну',
                    'збільшені аденоїди чи піднебінні мигдалики',
                    'сторонні тіла вуха, носа або глотки',
                    'носові кровотечі',
                    'осиплість голосу',
                ]),
                'services_overview': '\n'.join([
                    'консультація дитячого лікаря-отоларинголога',
                    'відеоендоскопія ЛОР-органів',
                    'тимпанометрія',
                    'видалення сірчаних пробок',
                    'видалення сторонніх тіл із вуха, носа та глотки',
                    'промивання лакун піднебінних мигдаликів',
                    'промивання порожнини носа методом переміщення',
                    'лікувальні маніпуляції при захворюваннях ЛОР-органів',
                    'спостереження дітей із частими ЛОР-захворюваннями',
                    'передопераційний та післяопераційний супровід',
                ]),
                'order': 0,
            },
            {
                'slug': 'otolaryngologiya',
                'name': 'Отоларингологія',
                'short_description': (
                    'Діагностика, лікування та профілактика захворювань вуха, горла й носа '
                    'на основі сучасних медичних стандартів.'
                ),
                'description': (
                    'Здоровʼя ЛОР-органів впливає на те, як ми дихаємо, чуємо, спимо, розмовляємо '
                    'та почуваємося щодня. Саме тому важливо не лише усунути симптоми, а й '
                    'зрозуміти їхню причину.\n\n'
                    'Ми поєднуємо сучасну діагностику, доказову медицину та уважне ставлення '
                    'до кожного пацієнта.'
                ),
                'when_to_visit': '\n'.join([
                    'утруднене носове дихання або тривала закладеність носа',
                    'нежить, який не минає або часто повторюється',
                    'біль чи дискомфорт у горлі',
                    'утруднене або болісне ковтання',
                    'захриплість голосу',
                    'біль у вусі',
                    'виділення з вуха',
                    'зниження слуху',
                    'шум або дзвін у вухах',
                    'запаморочення',
                    'часті синусити чи отити',
                    'носові кровотечі',
                    'хропіння та інші порушення дихання під час сну',
                ]),
                'services_overview': '\n'.join([
                    'консультація лікаря-отоларинголога',
                    'відеоендоскопія ЛОР-органів',
                    'тимпанометрія',
                    'аудіометрія',
                    'видалення сірчаних пробок',
                    'видалення сторонніх тіл із вуха, носа та глотки',
                    'промивання лакун піднебінних мигдаликів',
                    'промивання порожнини носа методом переміщення',
                    'лікувальні маніпуляції при захворюваннях ЛОР-органів',
                    'малоінвазивні амбулаторні процедури',
                    'передопераційний огляд та післяопераційний супровід',
                ]),
                'order': 1,
            },
            {
                'slug': 'surdologiya',
                'name': 'Сурдологія',
                'short_description': (
                    'Повна діагностика, лікування та реабілітація порушень слуху у дітей і дорослих. '
                    'Комплексне обстеження слухової системи із застосуванням сучасних методів '
                    'діагностики та підбір слухових апаратів.'
                ),
                'description': (
                    'Сурдологія — це напрямок медицини, який займається діагностикою, лікуванням '
                    'і реабілітацією порушень слуху у дітей і дорослих.\n\n'
                    'Ми проводимо комплексне обстеження слухової системи із застосуванням сучасного '
                    'діагностичного обладнання дорослим та дітям з першого дня життя. За результатами '
                    'обстеження лікар пояснює причину порушень, визначає подальшу тактику лікування '
                    'або реабілітації та, за потреби, рекомендує слухопротезування новітніми '
                    'слуховими апаратами.'
                ),
                'when_to_visit': '\n'.join([
                    'зниження слуху',
                    'шум або дзвін у вухах',
                    'утруднене розуміння мовлення, особливо в шумному середовищі',
                    'відчуття закладеності у вухах',
                    'запаморочення або порушення рівноваги',
                    'підозра на втрату слуху після перенесених захворювань чи травм',
                    'контроль слуху після лікування',
                    'підбір та налаштування слухових апаратів',
                    'профілактична перевірка слуху у дітей і дорослих',
                    'затримка розвитку мовлення у дітей',
                    'відсутність реакції на звук у дитини',
                ]),
                'services_overview': '\n'.join([
                    'консультація лікаря-сурдолога',
                    'комплексна діагностика слуху',
                    'тональна порогова аудіометрія',
                    'імпедансометрія (тимпанометрія та дослідження акустичних рефлексів)',
                    'отоакустична емісія (ОАЕ)',
                    'слухові викликані потенціали (КСВП/ABR)',
                    'скринінг слуху новонароджених',
                    'підбір, налаштування та супровід користувачів слухових апаратів',
                    'консультації щодо слухової реабілітації',
                ]),
                'order': 2,
            },
        ]

        directions = []
        for item in lor_data:
            obj, _ = Direction.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'name': item['name'],
                    'short_description': item['short_description'],
                    'description': item['description'],
                    'when_to_visit': item['when_to_visit'],
                    'services_overview': item['services_overview'],
                    'order': item['order'],
                    'is_active': True,
                },
            )
            directions.append(obj)
        return directions

    def _seed_services(self, directions, *, force=False):
        demo_slugs = [
            'konsultaciya-hirurga',
            'povtornyj-prijom',
            'uzd-organiv-cherevnoi',
            'check-up',
            'laparoskopiya',
            'korekciya-rubciv',
        ]
        Service.objects.filter(slug__in=demo_slugs).update(is_active=False)

        by_slug = {d.slug: d for d in directions}
        services_data = [
            ('dytacha-konsultaciya-lor', 'консультація дитячого лікаря-отоларинголога', 'dytacha-otolaryngologiya'),
            ('dytacha-videoendoskopiya', 'відеоендоскопія ЛОР-органів', 'dytacha-otolaryngologiya'),
            ('dytacha-timpanometriya', 'тимпанометрія', 'dytacha-otolaryngologiya'),
            ('dytacha-vydalennya-probok', 'видалення сірчаних пробок', 'dytacha-otolaryngologiya'),
            ('dytacha-vydalennya-til', 'видалення сторонніх тіл із вуха, носа та глотки', 'dytacha-otolaryngologiya'),
            ('dytacha-promyvannya-migdalikiv', 'промивання лакун піднебінних мигдаликів', 'dytacha-otolaryngologiya'),
            ('dytacha-promyvannya-nosa', 'промивання порожнини носа методом переміщення', 'dytacha-otolaryngologiya'),
            ('dytacha-likuvalni-manipulyaciyi', 'лікувальні маніпуляції при захворюваннях ЛОР-органів', 'dytacha-otolaryngologiya'),
            ('dytacha-sposterezhennya', 'спостереження дітей із частими ЛОР-захворюваннями', 'dytacha-otolaryngologiya'),
            ('dytacha-operacijnyj-suprovid', 'передопераційний та післяопераційний супровід', 'dytacha-otolaryngologiya'),
            ('lor-konsultaciya', 'консультація лікаря-отоларинголога', 'otolaryngologiya'),
            ('lor-videoendoskopiya', 'відеоендоскопія ЛОР-органів', 'otolaryngologiya'),
            ('lor-timpanometriya', 'тимпанометрія', 'otolaryngologiya'),
            ('lor-audiometriya', 'аудіометрія', 'otolaryngologiya'),
            ('lor-vydalennya-probok', 'видалення сірчаних пробок', 'otolaryngologiya'),
            ('lor-vydalennya-til', 'видалення сторонніх тіл із вуха, носа та глотки', 'otolaryngologiya'),
            ('lor-promyvannya-migdalikiv', 'промивання лакун піднебінних мигдаликів', 'otolaryngologiya'),
            ('lor-promyvannya-nosa', 'промивання порожнини носа методом переміщення', 'otolaryngologiya'),
            ('lor-likuvalni-manipulyaciyi', 'лікувальні маніпуляції при захворюваннях ЛОР-органів', 'otolaryngologiya'),
            ('lor-malo-invazyvni', 'малоінвазивні амбулаторні процедури', 'otolaryngologiya'),
            ('lor-operacijnyj-suprovid', 'передопераційний огляд та післяопераційний супровід', 'otolaryngologiya'),
            ('surdolog-konsultaciya', 'консультація лікаря-сурдолога', 'surdologiya'),
            ('surdolog-diahnostyka', 'комплексна діагностика слуху', 'surdologiya'),
            ('surdolog-tonalna-audiometriya', 'тональна порогова аудіометрія', 'surdologiya'),
            ('surdolog-impedansometriya', 'імпедансометрія (тимпанометрія та дослідження акустичних рефлексів)', 'surdologiya'),
            ('surdolog-oae', 'отоакустична емісія (ОАЕ)', 'surdologiya'),
            ('surdolog-ksvp', 'слухові викликані потенціали (КСВП/ABR)', 'surdologiya'),
            ('surdolog-skrining', 'скринінг слуху новонароджених', 'surdologiya'),
            ('surdolog-aparaty', 'підбір, налаштування та супровід користувачів слухових апаратів', 'surdologiya'),
            ('surdolog-reabilitaciya', 'консультації щодо слухової реабілітації', 'surdologiya'),
        ]
        for i, (slug, name, direction_slug) in enumerate(services_data):
            Service.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'direction': by_slug[direction_slug],
                    'description': f'{name} — послуга TEN clinic.',
                    'short_description': name,
                    'price': None,
                    'order': i,
                    'is_active': True,
                },
            )

    def _seed_hearing_aids(self, *, force=False):
        aids_data = [
            (
                'phonak-audeo-sphere',
                'Phonak Audeo Sphere Infinio',
                'Преміальна модель із штучним інтелектом для чіткого сприйняття мовлення навіть у шумному середовищі.',
            ),
            (
                'oticon-intent',
                'Oticon Intent',
                'Розумний слуховий апарат, який адаптується до ваших наміру та оточення в реальному часі.',
            ),
            (
                'signia-ix',
                'Signia Integrated Xperience',
                'Технологія розділення мовлення та шуму для комфортного спілкування в групах і на вулиці.',
            ),
            (
                'widex-moment',
                'Widex Moment',
                'Природне звучання без затримки сигналу — зручний вибір для тривалого щоденного носіння.',
            ),
        ]
        for i, (slug, name, short_description) in enumerate(aids_data):
            HearingAid.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'short_description': short_description,
                    'order': i,
                    'is_active': True,
                },
            )

    def _seed_doctors(self, directions, *, force=False):
        demo_slugs = [
            'ivanenko-olena',
            'petrenko-andriy',
            'kovalenko-maria',
            'sydorenko-igor',
            'melnyk-oksana',
        ]
        Doctor.objects.filter(slug__in=demo_slugs).update(is_active=False)
