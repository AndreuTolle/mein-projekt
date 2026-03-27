import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

EODHD_API_KEY = os.getenv("EODHD_API_KEY")


def fetch_eod_data(ticker: str) -> pd.DataFrame:
    if not EODHD_API_KEY:
        raise ValueError("EODHD_API_KEY fehlt in .env")

    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": EODHD_API_KEY,
        "fmt": "json",
        "period": "d",
        "order": "d",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    if not data:
        raise ValueError("Keine Daten von EOD erhalten")

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date", ascending=False).reset_index(drop=True)
    return df