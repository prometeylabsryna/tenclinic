from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0013_appointment_booking_form_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homeaboutussettings',
            fields=[
            ],
            options={
                'verbose_name': 'Головна — Про нас',
                'verbose_name_plural': 'Головна — Про нас',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('clinic.sitesettings',),
        ),
    ]
