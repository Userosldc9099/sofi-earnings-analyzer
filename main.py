import os
from datetime import datetime
from openai import OpenAI
from utils.report_loader import get_report_text
from utils.telegram import send_telegram

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

TICKERS = ["SOFI"]  # сюда можно будет добавить "TSLA", "UPST", и т.д.

def build_prompt(ticker: str, report_text: str) -> str:
    return f"""
Финансовый отчет {ticker}:

{report_text[:4000]}

1. Превзошла ли {ticker} ожидания по EPS и выручке?
2. Улучшились ли ключевые показатели по сравнению с предыдущим кварталом?
3. Как оценить guidance? Лучше / хуже / в рамках?
4. Есть ли тревожные сигналы, риски или сюрпризы?
5. Вывод: покупать, держать или продавать акции? Объясни решение.
"""

def analyze_ticker(ticker: str):
    print(f"🔍 Анализ {ticker}")
    report = get_report_text(ticker)

    if not report or len(report.strip()) < 20:
        print(f"⚠️ Отчет по {ticker} отсутствует")
        send_telegram(f"⚠️ Нет отчета для {ticker}")
        return

    prompt = build_prompt(ticker, report)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        result = response.choices[0].message.content
        print("✅ GPT результат:", result[:200])

        # Очистка от Markdown-сбоев
        clean = result.replace("*", "").replace("_", "").replace("`", "").replace("~", "").replace(">", "")
        send_telegram(f"📊 {ticker} Earnings ({datetime.today().date()}):\n{clean[:3900]}")
    except Exception as e:
        print(f"❌ Ошибка для {ticker}: {e}")
        send_telegram(f"❌ GPT ошибка по {ticker}: {str(e)}")

if __name__ == "__main__":
    for ticker in TICKERS:
        analyze_ticker(ticker)
