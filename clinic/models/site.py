from django.db import models

from clinic.image_specs import SITE_LOGO
from clinic.utils.map_embed import normalize_map_embed, resolve_map_embed_src


class SiteSettings(models.Model):
    site_name = models.CharField('Назва сайту', max_length=100, default='TEN clinic')
    tagline = models.CharField(
        'Слоган під логотипом',
        max_length=200,
        blank=True,
        help_text='Короткий рядок під логотипом у підвалі, наприклад «Medicine & Surgery».',
    )
    logo = models.ImageField(
        'Логотип',
        upload_to='site/',
        blank=True,
        help_text=SITE_LOGO.help_text,
    )
    about_text = models.TextField(
        'Про клініку (резерв)',
        blank=True,
        help_text='Застаріле поле. Основний текст — у «Контент → Про клініку».',
    )

    address = models.CharField(
        'Адреса',
        max_length=500,
        blank=True,
        help_text='Відображається на головній, сторінці «Контакти» та в підвалі.',
    )
    phone_primary = models.CharField(
        'Телефон',
        max_length=20,
        blank=True,
        help_text='Основний номер для дзвінків на всьому сайті.',
    )
    phone_secondary = models.CharField(
        'Додатковий телефон',
        max_length=20,
        blank=True,
        help_text='Необовʼязковий другий номер на сторінці «Контакти».',
    )
    email = models.EmailField('Email', blank=True)
    telegram_url = models.URLField('Telegram', blank=True)
    viber_url = models.URLField('Viber', blank=True)

    map_lat = models.DecimalField('Широта', max_digits=9, decimal_places=6, null=True, blank=True)
    map_lng = models.DecimalField('Довгота', max_digits=9, decimal_places=6, null=True, blank=True)
    map_embed_url = models.TextField(
        'Карта Google Maps',
        blank=True,
        help_text=(
            'Вставте повний код вбудовування з Google Maps («Поділитися → Вбудувати карту») '
            'або лише посилання з src. Якщо поле порожнє — карта будується з широти та довготи.'
        ),
    )
    directions_text = models.TextField('Як доїхати', blank=True)

    notification_email = models.EmailField('Email для заявок', blank=True)
    telegram_bot_token = models.CharField('Telegram Bot Token', max_length=100, blank=True)
    telegram_chat_id = models.CharField('Telegram Chat ID', max_length=50, blank=True)
    meta_description = models.CharField('Meta description', max_length=300, blank=True)

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        if self.map_embed_url:
            self.map_embed_url = normalize_map_embed(self.map_embed_url)
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def map_embed_src(self):
        return resolve_map_embed_src(
            self.map_embed_url,
            lat=self.map_lat,
            lng=self.map_lng,
            address=self.address,
        )


class SiteBlock(models.Model):
    class Page(models.TextChoices):
        HOME = 'home', 'Головна'
        SITE = 'site', 'Сайт'
        DIRECTIONS = 'directions', 'Напрямки'
        DOCTORS = 'doctors', 'Лікарі'
        SERVICES = 'services', 'Послуги'
        CONTACTS = 'contacts', 'Контакти'
        BOOKING = 'booking', 'Запис'
        PRIVACY = 'privacy', 'Конфіденційність'
        SURGICAL = 'surgical', 'Хірургія'
        DIRECTION = 'direction', 'Сторінка напрямку'

    class ContentType(models.TextChoices):
        TEXT = 'text', 'Текст'
        IMAGE = 'image', 'Фото'

    page = models.CharField(max_length=32, choices=Page.choices)
    key = models.CharField(max_length=64)
    label = models.CharField(max_length=128)
    content_type = models.CharField(
        max_length=16,
        choices=ContentType.choices,
        default=ContentType.TEXT,
    )
    text_html = models.TextField(blank=True)
    image = models.ImageField(upload_to='blocks/', blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['page', 'sort_order', 'key']
        verbose_name = 'Блок контенту'
        verbose_name_plural = 'Блоки контенту'
        constraints = [
            models.UniqueConstraint(fields=['page', 'key'], name='unique_site_block_page_key'),
        ]

    def __str__(self):
        return f'{self.page}.{self.key}'

    @property
    def cache_key(self):
        return f'{self.page}.{self.key}'
