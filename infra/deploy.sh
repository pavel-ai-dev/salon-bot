#!/usr/bin/env bash
# Деплой salon-bot: локальный репозиторий (ПК) -> ${SALON_SSH_HOST:?set SALON_SSH_HOST}:/opt/salon-bot
# Запуск из WSL:  bash infra/deploy.sh
#
# Безопасность: НЕ трогает на сервере .env, data/ (БД клиентов!) и logs/.
# Код заливается rsync без --delete по защищённым путям, затем рестарт + health-check.
set -euo pipefail

LOCAL="${SALON_LOCAL:?set SALON_LOCAL}"
SSH_HOST="${SALON_SSH_HOST:?set SALON_SSH_HOST}"
REMOTE_DIR="/opt/salon-bot"
SERVICE="salon-bot"
OWNER="salonbot:salonbot"

echo "==> 1/4 rsync кода (.env / data / logs на сервере сохраняются)"
rsync -az --no-perms --omit-dir-times \
  --exclude='.git'        --exclude='.github' \
  --exclude='.venv'       --exclude='venv' \
  --exclude='tests'       --exclude='__pycache__' \
  --exclude='*.pyc'       --exclude='.pytest_cache' \
  --exclude='.env'        --exclude='data' \
  --exclude='logs'        --exclude='*.db' \
  --exclude='*.session'   --exclude='conftest.py' \
  "$LOCAL" "${SSH_HOST}:${REMOTE_DIR}/"

echo "==> 2/4 владелец и зависимости"
ssh "$SSH_HOST" "chown -R ${OWNER} ${REMOTE_DIR} && cd ${REMOTE_DIR} && ./venv/bin/pip install -q -r requirements.txt"

echo "==> 3/4 рестарт сервиса"
ssh "$SSH_HOST" "systemctl restart ${SERVICE}"

echo "==> 4/4 проверка (active + health)"
ssh "$SSH_HOST" "sleep 3 && systemctl is-active ${SERVICE} && curl -fsS http://127.0.0.1:8080/health && echo"

echo "==> Деплой завершён."
