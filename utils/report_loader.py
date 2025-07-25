import requests
from bs4 import BeautifulSoup

def get_report_text(ticker: str) -> str:
    if ticker != "SOFI":
        return ""

    try:
        # 1. Найдём последний 10-Q или 8-K через CIK
        cik = "0001818874"  # SoFi
        url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-Q&count=10&owner=exclude&output=atom"

        feed = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
        accession_numbers = list(set([
            line.split("accession-number>")[-1].split("<")[0]
            for line in feed.splitlines()
            if "accession-number>" in line
        ]))

        if not accession_numbers:
            return "❌ Не найден 10-Q отчет на SEC для SOFI"

        acc = accession_numbers[0]
        acc_nodashes = acc.replace("-", "")
        html_url = f"https://www.sec.gov/Archives/edgar/data/1818874/{acc_nodashes}/index.json"

        json_data = requests.get(html_url, headers={"User-Agent": "Mozilla/5.0"}).json()
        html_file = next((f for f in json_data["directory"]["item"] if f["name"].endswith(".htm")), None)

        if not html_file:
            return "❌ Не найден HTML-файл отчёта"

        report_url = f"https://www.sec.gov/Archives/edgar/data/1818874/{acc_nodashes}/{html_file['name']}"
        html = requests.get(report_url, headers={"User-Agent": "Mozilla/5.0"}).text

        # 2. Парсим HTML
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n")

        # 3. Извлекаем ключевые разделы
        snippets = []
        for section in ["management’s discussion", "results of operations", "financial highlights", "outlook", "guidance"]:
            section = section.lower()
            found = [line.strip() for line in text.splitlines() if section in line.lower()]
            snippets.extend(found[:5])

        full_report = "\n".join(snippets[:50])
        return full_report if full_report else text[:3000]

    except Exception as e:
        return f"❌ Ошибка при загрузке отчета с SEC: {e}"
