from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0005_alter_sitesettings_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='map_embed_url',
            field=models.URLField(
                blank=True,
                help_text=(
                    'Повне посилання з src у коді «Вбудувати карту» Google Maps. '
                    'Якщо карта не відображається — очистіть поле і вкажіть широту та довготу.'
                ),
                max_length=2000,
                verbose_name='URL карти (embed)',
            ),
        ),
    ]
