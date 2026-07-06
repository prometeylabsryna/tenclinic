from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0009_hearingaid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hearingaid',
            name='short_description',
            field=models.CharField(
                help_text='Короткий текст під фото на картці.',
                max_length=300,
                verbose_name='Підпис',
            ),
        ),
    ]
