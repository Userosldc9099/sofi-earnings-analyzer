import os
import requests
from datetime import datetime
from openai import OpenAI
from utils.report_loader import get_sofi_report_text
from utils.telegram import send_telegram

openai_api_key = os.getenv("OPENAI_API_KEY")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

def build_prompt(report_text):
    return f"""
Финансовый отчет SoFi (SOFI):

{report_text[:4000]}

1. Превзошла ли SoFi ожидания по EPS и выручке?
2. Улучшились ли ключевые показатели по сравнению с предыдущим кварталом?
3. Как оценить guidance? Лучше / хуже / в рамках?
4. Есть ли тревожные сигналы, риски или сюрпризы?
5. Вывод: покупать, держать или продавать акции? Объясни решение.
"""

def analyze_report():
    report_text = get_sofi_report_text()
    if not report_text:
        send_telegram("❌ Не удалось загрузить отчет SoFi. Проверь источник.")
        return

    client = OpenAI(api_key=openai_api_key)
    prompt = build_prompt(report_text)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    result = response.choices[0].message.content
    send_telegram(f"📊 SoFi Earnings ({datetime.today().date()}):\n" + result)

if __name__ == "__main__":
    analyze_report()
