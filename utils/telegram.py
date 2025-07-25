import os
import requests

def send_telegram(message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    print(f"📨 Отправка сообщения в Telegram: chat_id={chat_id}, message={message[:50]}")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message[:3900],  # урежем сообщение до лимита
        "parse_mode": "MarkdownV2"  # ИЛИ убери это поле, если глючит
    }

    try:
        response = requests.post(url, data=payload)
        print(f"📦 Статус отправки: {response.status_code}, ответ: {response.text}")
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Ошибка при отправке в Telegram: {e}")
