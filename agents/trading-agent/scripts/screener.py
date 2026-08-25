"""
Trading Agent — Fundamental Screener
Scrapes Screener.in and Moneycontrol for fundamental data.
Usage: python screener.py <COMPANY_NAME>
Example: python screener.py Tata Consultancy Services
"""

import sys
import json
import re


def install_deps():
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "-q"])


def scrape_screener(company_name):
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        install_deps()
        import requests
        from bs4 import BeautifulSoup

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    result = {
        "company": company_name,
        "source": "screener.in",
        "fetched_at": None,
        "data": {},
        "error": None
    }

    from datetime import datetime
    result["fetched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        search_url = f"https://www.screener.in/company/{company_name.replace(' ', '-').replace('&', 'and').replace('.', '').replace('(', '').replace(')', '').replace("'", '')}/consolidated/"
        search_url_simple = f"https://www.screener.in/company/{company_name.split()[0].upper()}/consolidated/"

        resp = None
        for url in [search_url, search_url_simple]:
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200 and "company" in r.url:
                    resp = r
                    break
            except Exception:
                continue

        if resp is None:
            result["error"] = "Could not find company on Screener.in. Try Moneycontrol fallback."
            return result

        soup = BeautifulSoup(resp.text, "html.parser")

        def extract_number(text):
            if not text:
                return None
            cleaned = re.sub(r"[^\d.\-]", "", text.replace(",", "").replace("%", "").strip())
            try:
                val = float(cleaned)
                return round(val, 2)
            except ValueError:
                return None

        li_items = soup.select("li")
        for li in li_items:
            name_span = li.select_one("span.name")
            value_span = li.select_one("span.number, span.nowrap")
            if name_span and value_span:
                key = name_span.get_text(strip=True).lower().replace(" ", "_").replace(".", "")
                val = extract_number(value_span.get_text(strip=True))
                if val is not None:
                    result["data"][key] = val

        market_cap_elem = soup.select_one("li:has(span:-soup-contains('Market Cap')) span.number")
        if not market_cap_elem:
            market_cap_elem = soup.select_one("li:has(span:-soup-contains('Market Cap')) span.nowrap")
        if market_cap_elem:
            text = market_cap_elem.get_text(strip=True)
            multiplier = 1
            if "Cr" in text or "Cr." in text:
                multiplier = 1
            result["data"]["market_cap_cr"] = extract_number(text)

        stock_price_elem = soup.select_one("span:-soup-contains('Stock P/E') ~ span.number")
        pe_elems = soup.select("span:-soup-contains('Stock P/E')")
        for pe in pe_elems:
            parent = pe.parent
            if parent:
                num = parent.select_one("span.number")
                if num:
                    result["data"]["stock_pe"] = extract_number(num.get_text())

        cagr_section = soup.find("h2", string=re.compile(r"Compounded.*Growth", re.I))
        if cagr_section:
            cagr_table = cagr_section.find_next("table")
            if cagr_table:
                rows = cagr_table.select("tr")[1:]
                for row in rows:
                    cols = row.select("td")
                    if len(cols) >= 3:
                        period = cols[0].get_text(strip=True).lower().replace(" ", "_")
                        val = extract_number(cols[-1].get_text(strip=True))
                        if val is not None and period:
                            result["data"][f"{period}_cagr"] = val

        if not result["data"]:
            result["error"] = "Screener.in returned data but parsing failed. Manual check needed."
        elif result.get("data", {}) == {}:
            result["error"] = "No data extracted from Screener.in page."

    except Exception as e:
        result["error"] = f"Screener.in error: {str(e)}"

    return result


def scrape_moneycontrol(company_name):
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        install_deps()
        import requests
        from bs4 import BeautifulSoup

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    result = {
        "company": company_name,
        "source": "moneycontrol.com",
        "data": {},
        "error": None
    }

    try:
        search_url = f"https://www.moneycontrol.com/stocks/cptmarket/compsearchnew.php?search_data=&cid=&mbsearch_str=&topsearch_type=1&search_str={company_name}"
        r = requests.get(search_url, headers=headers, timeout=15)
        if r.status_code == 200:
            try:
                search_data = r.json()
                if search_data and len(search_data) > 0:
                    item = search_data[0]
                    result["data"]["company_name"] = item.get("fullname", company_name)
                    result["data"]["bse_code"] = item.get("sc_code")
                    result["data"]["nse_code"] = item.get("sc_id")
                    result["data"]["sector"] = item.get("sector_name", "")
            except (json.JSONDecodeError, ValueError):
                pass

    except Exception as e:
        result["error"] = f"Moneycontrol error: {str(e)}"

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python screener.py <COMPANY_NAME>")
        print("Example: python screener.py 'Tata Consultancy Services'")
        sys.exit(1)

    company = " ".join(sys.argv[1:])

    screen_result = scrape_screener(company)
    mc_result = scrape_moneycontrol(company)

    output = {
        "company": company,
        "screener": screen_result,
        "moneycontrol": mc_result,
        "verified": screen_result.get("error") is None and len(screen_result.get("data", {})) > 0
    }

    print(json.dumps(output, indent=2))
