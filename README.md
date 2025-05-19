# 📊 Salary Aggregate Bot

Асинхронный Telegram-бот для агрегации данных о зарплатах из коллекции MongoDB за указанный период времени с возможностью группировки по дням, неделям или месяцам. Реализован с использованием FastAPI, aiogram и MongoDB.

---

## 🚀 Возможности

- 📆 Группировка данных по дням, неделям или месяцам
- 📈 Агрегация зарплат за заданный период времени
- 🤖 Взаимодействие через Telegram-бота
- 🌐 REST API для получения агрегированных данных
- 🐳 Развёртывание с использованием Docker Compose
- 🧪 Тестирование с использованием pytest

---

## 🧰 Технологии

- Python 3.10+
- FastAPI
- aiogram
- MongoDB
- Docker & Docker Compose
- pytest

---

## ⚙️ Установка и запуск

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/artem-sitd/salary_aggregate_bot.git
   cd salary_aggregate_bot
   ```

2. **Настройте переменные окружения:**

   Переименуйте файл `.env.docker.template` в `.env.docker`:

   ```bash
   cp .env.docker.template .env.docker
   ```

   Отредактируйте файл `.env.docker`, указав необходимые значения:

   - `MONGO_INITDB_ROOT_USERNAME` — имя пользователя MongoDB
   - `MONGO_INITDB_ROOT_PASSWORD` — пароль пользователя MongoDB
   - `MONGO_DB` — имя базы данных MongoDB
   - `TELEGRAM_API_KEY` — токен вашего бота, полученный у [@BotFather](https://t.me/BotFather)

3. **Запустите приложение с помощью Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   Приложение будет доступно по адресу `http://localhost:8000`.

---

## 📦 Пример использования API

**Запрос:**

```json
{
  "dt_from": "2022-09-01T00:00:00",
  "dt_upto": "2022-12-31T23:59:00",
  "group_type": "month"
}
```

**Ответ:**

```json
{
  "dataset": [5906586, 5515874, 5889803, 6092634],
  "labels": [
    "2022-09-01T00:00:00",
    "2022-10-01T00:00:00",
    "2022-11-01T00:00:00",
    "2022-12-01T00:00:00"
  ]
}
```

---

## 📁 Структура проекта

```
├── app/                   # Основная логика приложения
├── data/                  # Скрипты инициализации MongoDB
├── tests/                 # Тесты проекта
├── .env.docker.template   # Шаблон переменных окружения
├── docker-compose.yaml    # Конфигурация Docker Compose
├── Dockerfile             # Dockerfile для сборки образа
├── requirements.txt       # Зависимости проекта
├── README.md              # Документация проекта
└── ...
```

---

## 🧪 Тестирование

Для запуска тестов используйте следующую команду:

```bash
pytest
```

Тесты находятся в директории `tests/` и покрывают основные сценарии использования API.

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. файл `LICENSE`.
