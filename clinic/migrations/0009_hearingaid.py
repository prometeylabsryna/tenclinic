from django.db import migrations, models

import clinic.image_specs


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0008_alter_sitesettings_map_embed_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='HearingAid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Назва')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(
                    blank=True,
                    help_text=clinic.image_specs.HEARING_AID_IMAGE.help_text,
                    upload_to='hearing-aids/',
                    verbose_name='Фото',
                )),
                ('short_description', models.CharField(max_length=300, verbose_name='Короткий опис')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активний')),
            ],
            options={
                'verbose_name': 'Слуховий апарат',
                'verbose_name_plural': 'Слухові апарати',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.AlterField(
            model_name='siteblock',
            name='page',
            field=models.CharField(choices=[
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
                ('direction', 'Сторінка напрямку'),
            ], max_length=32),
        ),
    ]
