import os
import requests
from datetime import datetime
from openai import OpenAI
from utils.report_loader import get_sofi_report_text
from utils.telegram import send_telegram

openai_api_key = os.getenv("OPENAI_API_KEY")

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
    print("🔍 STARTING analyze_report")

    report_text = get_sofi_report_text()
    print("📝 Загрузили отчёт:", report_text[:100])

    if not report_text or len(report_text.strip()) < 20:
        print("❌ Пустой или короткий текст отчёта")
        send_telegram("❌ Не удалось загрузить отчет SoFi.")
        return

    prompt = build_prompt(report_text)
    print("📤 Отправляем запрос в OpenAI...")
    
    try:
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        result = response.choices[0].message.content
        print("✅ Ответ GPT получен:", result[:200])
        send_telegram(f"📊 SoFi Earnings ({datetime.today().date()}):\n{result}")

    except Exception as e:
        print("🔥 Ошибка при обращении к OpenAI:", str(e))
        send_telegram(f"❌ Ошибка при работе с OpenAI API: {str(e)}")

if __name__ == "__main__":
    analyze_report()
