from decouple import config

from .production import *  # noqa: F401,F403

# TLS завершується в nginx; Gunicorn працює лише по HTTP.
SECURE_SSL_REDIRECT = False

USE_HTTPS = config('USE_HTTPS', default=False, cast=bool)
if USE_HTTPS:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
