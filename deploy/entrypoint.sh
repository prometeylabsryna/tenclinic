#!/usr/bin/env bash
set -euo pipefail

echo "==> Waiting for PostgreSQL..."
python <<'PY'
import os
import sys
import time

import psycopg2

host = os.environ.get("DB_HOST", "db")
port = os.environ.get("DB_PORT", "5432")
name = os.environ.get("DB_NAME", "")
user = os.environ.get("DB_USER", "")
password = os.environ.get("DB_PASSWORD", "")

if not name:
    sys.exit(0)

for attempt in range(30):
    try:
        psycopg2.connect(
            dbname=name,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        print("==> DB ready")
        break
    except psycopg2.OperationalError:
        time.sleep(2)
else:
    print("FATAL: DB not ready")
    sys.exit(1)
PY

echo "==> Django check + migrate + collectstatic"
python manage.py check --deploy
python manage.py migrate --noinput
python manage.py bootstrap_site
python manage.py collectstatic --noinput

_static_count="$(find "${STATIC_ROOT:-/app/staticfiles}" -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "==> static files: ${_static_count}"
if [ "${_static_count:-0}" -lt 10 ]; then
  echo "WARN: staticfiles count low — перевір STATIC_ROOT і collectstatic"
fi

exec "$@"
