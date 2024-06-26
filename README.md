# Телеграм бота для автоматической посещаемости в университете ЛЭТИ

### Description
Простой асинхронный телеграм бот, который предоставляет возможность пользователям авторизоваться в личном кабинете и перестать беспокоиться о электронной посещаемости на парах.
[https://t.me/etu_autoattendance_bot](https://t.me/etu_autoattendance_bot)
### Технологии
- python 3.12
- selenium *для взаимодействия с личным кабинетом ЛЭТИ*
- aiogram *для взаимодействия с Telegram Bot API*
- psycopg3 *для взаимодействия с базой данных*
- docker *для запуска*
### Внести вклад в разработку
#### Зависимости
- docker 23 и выше
#### Шаги установки
1. делаем fork репозитория
2. клонируем репозиторий
3. создаем `.env` файл внутри *app* директории
  устанавливаем следующие переменные окружения:
  - CELERY_BROKER_URL
  - CELERY_RESULT_BACKEND
  - BOT_TOKEN
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_DB
  - POSTGRES_HOST
  - POSTGRES_PORT
  - SELENIUM_HOST
4. в основной директории `docker compose --env-file ./app/.env up -d --build`
5. создаем Pull Request в мой репозиторий

**Удачи!**
