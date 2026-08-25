# Salon Bot v14

[![tests](https://github.com/pavel-ai-dev/salon-bot/actions/workflows/tests.yml/badge.svg)](https://github.com/pavel-ai-dev/salon-bot/actions/workflows/tests.yml)

Telegram-бот для автоматизации записи клиентов в салон красоты / студию мастера.

## Что умеет

- Онлайн-запись клиентов на услуги с выбором дня и времени
- Управление расписанием мастера (блокировка дней, просмотр записей)
- Портфолио работ с фото (управление через бот)
- Напоминания клиентам за 24 часа и 2 часа до записи
- Отзывы клиентов после оказания услуги
- Чёрный список нежелательных клиентов
- Экспорт записей в Excel
- Rate limiting и защита от дублей нажатий

## Архитектура

Многослойная структура: хендлеры → сервисы → репозитории → модели.

```
app/
├── bot/
│   ├── handlers/      client.py, master.py — Telegram-хендлеры (клиент / мастер)
│   └── helpers.py     клавиатуры, безопасная отправка, StepDispatcher
├── core/              инфраструктура:
│                        settings, database, healthcheck,
│                        rate_limiter, step_guard, callback_dedup,
│                        phone, time_utils
├── models/            domain.py — доменные модели
├── repositories/      repo.py — доступ к данным (паттерн Repository)
└── services/          бизнес-логика: services, excel_worker, reminder_guard
main.py                точка входа (python-telegram-bot, polling)
```

## Стек

- Python 3.12
- python-telegram-bot 22.x (polling mode) + APScheduler (job-queue)
- SQLite (файл: `data/salon.db`)
- openpyxl — экспорт в Excel
- pytz — временные зоны

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # заполнить BOT_TOKEN и параметры мастера
python main.py
```

## Systemd

Юнит-файл: [`infra/salon_bot.service`](infra/salon_bot.service). `WorkingDirectory`/`ExecStart`/`User` подгоняются под окружение сервера.

```bash
sudo cp infra/salon_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now salon_bot
sudo systemctl status salon_bot
```

## Переменные окружения

| Переменная | Описание |
|---|---|
| `BOT_TOKEN` | Telegram Bot API токен (обязателен) |
| `ADMIN_IDS` | Telegram ID администраторов через запятую |
| `MASTER_USERNAME` | Имя/username мастера (отображается клиентам) |
| `MASTER_ADDRESS` | Адрес для напоминаний |
| `MASTER_CONTACT` | Контакт мастера (по умолчанию = MASTER_USERNAME) |
| `YANDEX_MAPS_URL` | Ссылка на точку в Яндекс.Картах |
| `MASTER_BIO` / `MASTER_PHOTO_ID` | Био и фото мастера |
| `MAX_SLOTS_PER_DAY` | Слотов в день (по умолчанию 4) |
| `BOOKING_WINDOW_DAYS` | Глубина записи вперёд, дней (60) |
| `RETURN_NOTIFY_DAYS` | Через сколько дней звать вернуться (21) |
| `RESCHEDULE_TIMEOUT_HOURS` | Таймаут переноса записи, часов (24) |
| `REVIEW_DELAY_HOURS` | Задержка перед запросом отзыва, часов (4) |
| `RATE_BOOKING` / `RATE_REVIEW` / `RATE_RESCHEDULE` | Лимиты в формате `N/секунды` |
| `TIMEZONE` | Часовой пояс (по умолчанию Europe/Moscow) |

## Backup

Ежедневно в 03:00:
- `salon.db` и `bookings.xlsx` — в каталог бэкапов, подпапка по дате
- код — архивом туда же
- хранится последних 30 бэкапов

## Тесты

Unit-тесты на чистые модули `core` (pytest). 42 теста, прогоняются в CI на каждый push/PR.

```bash
pip install -r requirements.txt
pytest
```

Покрыто: `phone` (валидация/нормализация номеров), `rate_limiter` (sliding window), `step_guard` (таймаут шагов), `callback_dedup` (дедуп callback'ов с TTL), `time_utils` (даты, UTC-конверсия, окно записи).
