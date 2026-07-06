#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

COMPOSE_FILES=(-f docker-compose.yml)
if [[ "${USE_HTTPS:-false}" == "true" ]]; then
  COMPOSE_FILES+=(-f docker-compose.prod.yml)
fi

free_host_ports() {
  if command -v systemctl >/dev/null 2>&1; then
    systemctl stop nginx 2>/dev/null || true
    systemctl disable nginx 2>/dev/null || true
    systemctl stop 'gunicorn-*' 2>/dev/null || true
    systemctl disable 'gunicorn-*' 2>/dev/null || true
  fi
}

free_host_ports

echo "==> Building and starting containers"
docker compose "${COMPOSE_FILES[@]}" build web
docker compose "${COMPOSE_FILES[@]}" up -d

echo "==> Waiting for healthcheck"
for _ in $(seq 1 30); do
  if curl -sf "http://127.0.0.1:${HTTP_PORT:-80}/healthz/" >/dev/null; then
    echo "==> HTTP healthcheck OK"
    exit 0
  fi
  sleep 2
done

echo "WARN: healthcheck not ready — перевір логи:"
docker compose "${COMPOSE_FILES[@]}" logs --tail=50 web nginx
exit 1
