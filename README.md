# Salon Bot v14

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



## Стек

- Python 3.11
- python-telegram-bot 21.x (polling mode)
- SQLite (файл: data/salon.db)
- openpyxl — Excel экспорт
- pytz — временные зоны

## Запуск



## Systemd



## Переменные окружения

| Переменная | Описание |
|---|---|
| BOT_TOKEN | Telegram Bot API токен |
| MASTER_CHAT_ID | Telegram ID мастера |
| MASTER_USERNAME | Имя мастера (отображается клиентам) |
| MASTER_ADDRESS | Адрес для напоминаний |
| TIMEZONE | Часовой пояс (Europe/Moscow) |
| DB_PATH | Путь к SQLite базе |

## Backup

Ежедневно в 03:00 запускается :
- salon.db → /root/backups/YYYYMMDD/
- bookings.xlsx → /root/backups/YYYYMMDD/
- код v14 → /root/backups/YYYYMMDD/v14_code.tar.gz
- Хранится последних 30 бэкапов

## Тесты


