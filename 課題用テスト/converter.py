import requests
from datetime import datetime, timedelta

API_URL = "https://api.frankfurter.app"

def get_exchange_rate(from_currency: str, to_currency: str, timeout: int = 10):
    """指定通貨ペアの最新レートを取得"""
    try:
        if from_currency == to_currency:
            return 1.0
        r = requests.get(f"{API_URL}/latest", params={"from": from_currency, "to": to_currency}, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        rates = data.get("rates", {})
        return rates.get(to_currency)
    except Exception:
        return None

def get_past_rates(from_currency: str, to_currency: str, days: int = 7):
    """過去 N 日間の為替レートを取得"""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    try:
        r = requests.get(f"{API_URL}/{start_date.date()}..{end_date.date()}",
                         params={"from": from_currency, "to": to_currency})
        r.raise_for_status()
        data = r.json()
        # 日付順に並べる
        rates = {date: value[to_currency] for date, value in sorted(data.get("rates", {}).items())}
        return rates
    except Exception:
        return {}
