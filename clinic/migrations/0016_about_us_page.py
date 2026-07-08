from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0015_catalogservice_pricelistitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteblock',
            name='page',
            field=models.CharField(
                choices=[
                    ('home', 'Головна'),
                    ('site', 'Сайт'),
                    ('directions', 'Напрямки'),
                    ('doctors', 'Лікарі'),
                    ('services', 'Послуги'),
                    ('contacts', 'Контакти'),
                    ('booking', 'Запис'),
                    ('privacy', 'Конфіденційність'),
                    ('surgical', 'Хірургія'),
                    ('hearing_aids', 'Слухові апарати'),
                    ('about_us', 'Про нас'),
                    ('direction', 'Сторінка напрямку'),
                ],
                max_length=32,
            ),
        ),
        migrations.CreateModel(
            name='Aboutuspagesettings',
            fields=[
            ],
            options={
                'verbose_name': 'Сторінка «Про нас»',
                'verbose_name_plural': 'Сторінка «Про нас»',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('clinic.sitesettings',),
        ),
    ]
