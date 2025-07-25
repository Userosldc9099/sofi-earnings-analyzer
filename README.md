# SoFi Earnings Analyzer 🤖

Автоматическая система анализа квартальных отчётов SoFi и отправки инвестиционного вывода в Telegram через ChatGPT.

## 📦 Установка и запуск

1. Залей этот репозиторий в GitHub
2. Подключи его в Render.com как Cron Job
3. Укажи переменные окружения:
   - `OPENAI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. Нажми “Manual deploy” или жди 29 июля

## 🔧 Структура

- `main.py` — точка входа
- `utils/` — обработка отчёта и отправка в Telegram
- `render.yaml` — расписание запуска
