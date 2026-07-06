# Деплой TEN clinic на DigitalOcean

## Передумови

- Droplet Ubuntu 24.04, ≥ 2 GB RAM (CMS + адмінка)
- Домен `tenclinic.com.ua` або IP для першого HTTP-деплою
- Git-репозиторій з цим проєктом

## Швидкий старт (HTTP)

```bash
mkdir -p /var/www && cd /var/www
git clone https://github.com/prometeylabsryna/tenclinic.git ten-clinic
cd ten-clinic

bash deploy/docker/install-docker.sh
cp .env.docker.example .env
nano .env   # SECRET_KEY, DB_PASSWORD, ALLOWED_HOSTS (IP + домен + web)

bash deploy/docker/deploy.sh
curl -sf http://127.0.0.1/healthz/
```

## Після першого деплою

```bash
# Якщо superuser не створено через .env:
docker compose exec web python manage.py createsuperuser

# Перевірка адмінки
curl -I http://127.0.0.1/admin/
```

## SSL (Let's Encrypt)

```bash
apt install -y certbot
docker compose stop nginx
certbot certonly --standalone -d tenclinic.com.ua -d www.tenclinic.com.ua
# У .env: USE_HTTPS=true, CSRF_TRUSTED_ORIGINS=https://...

USE_HTTPS=true bash deploy/docker/deploy.sh
```

## Оновлення

```bash
cd /var/www/ten-clinic
git pull origin main
docker compose -f docker-compose.yml -f docker-compose.prod.yml build web
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
docker compose exec web python manage.py migrate --noinput
```

## Зображення

| Тип | Де зберігаються | Як потрапляють на сервер |
|-----|-----------------|--------------------------|
| Бренд (hero, logo) | `static/images/` | `collectstatic` → nginx `/static/` |
| CMS / лікарі / напрямки | `media/` volume | Завантаження через адмінку або rsync volume |

Локальний media (якщо є):

```bash
rsync -av ./media/ user@DROPLET:/var/lib/docker/volumes/ten-clinic_media_volume/_data/
```

## Змінні середовища (.env)

Див. `.env.docker.example`. Обов'язково:

- `SECRET_KEY` — довгий випадковий рядок
- `DB_PASSWORD`
- `ALLOWED_HOSTS` — домен, www, IP Droplet, `127.0.0.1`, `localhost`, **`web`**
- `CSRF_TRUSTED_ORIGINS` — `https://domain` після SSL

Опційно для автоматичного superuser:

```env
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=...
DJANGO_SUPERUSER_EMAIL=admin@tenclinic.ua
```

## Діагностика

```bash
docker compose logs -f web nginx
docker compose exec web python manage.py check --deploy
docker compose exec nginx ls -la /app/staticfiles/ | head
curl -I http://127.0.0.1/static/images/hero-bg.jpg
```

Повний playbook: Prometey vault → `django-digitalocean-deploy.md`, `django-docker-ssl.md`.
