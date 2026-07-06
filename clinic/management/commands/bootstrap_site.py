from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from clinic.models import SiteSettings


class Command(BaseCommand):
    help = 'Початкове наповнення БД для production (fixture або seed_data)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force-seed',
            action='store_true',
            help='Завжди запускати seed_data після завантаження fixture',
        )

    def handle(self, *args, **options):
        self._ensure_content(options['force_seed'])
        self._ensure_superuser()

    def _ensure_content(self, force_seed):
        if SiteSettings.objects.filter(pk=1).exists() and not force_seed:
            self.stdout.write('Site content already exists — skip bootstrap.')
            return

        fixture = Path('deploy/fixtures/initial_data.json')
        if fixture.is_file():
            self.stdout.write(f'Loading fixture: {fixture}')
            call_command('loaddata', str(fixture), verbosity=0)
        else:
            self.stdout.write('Fixture not found — running seed_data.')
            call_command('seed_data')

        if force_seed:
            call_command('seed_data', force=True)

    def _ensure_superuser(self):
        user_model = get_user_model()
        if user_model.objects.filter(is_superuser=True).exists():
            return

        username = self._env('DJANGO_SUPERUSER_USERNAME')
        password = self._env('DJANGO_SUPERUSER_PASSWORD')
        email = self._env('DJANGO_SUPERUSER_EMAIL', 'admin@tenclinic.ua')

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Superuser not created — set DJANGO_SUPERUSER_USERNAME and '
                    'DJANGO_SUPERUSER_PASSWORD in .env or run createsuperuser manually.'
                )
            )
            return

        user_model.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))

    @staticmethod
    def _env(name, default=''):
        import os

        return os.environ.get(name, default)
