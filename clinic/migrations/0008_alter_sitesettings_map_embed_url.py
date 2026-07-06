from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0007_alter_sitesettings_map_embed_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='map_embed_url',
            field=models.TextField(
                blank=True,
                help_text=(
                    'Вставте повний код вбудовування з Google Maps («Поділитися → Вбудувати карту») '
                    'або лише посилання з src. Якщо поле порожнє — карта будується з широти та довготи.'
                ),
                verbose_name='Карта Google Maps',
            ),
        ),
    ]
