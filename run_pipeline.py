import os
import requests
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

EODHD_API_KEY = os.getenv("EODHD_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

TICKER = "SPY.US"


def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL oder SUPABASE_ANON_KEY fehlt in .env")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


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


def store_latest_price(client: Client, df: pd.DataFrame, symbol: str) -> dict:
    latest = df.iloc[0]

    payload = {
        "symbol": symbol,
        "date": latest["date"].date().isoformat(),
        "close": float(latest["close"]),
    }

    result = client.table("prices").insert(payload).execute()
    return result.data[0]


def calculate_signal(df: pd.DataFrame, symbol: str) -> dict:
    latest = df.iloc[0]
    previous = df.iloc[1]

    latest_close = float(latest["close"])
    previous_close = float(previous["close"])

    return_1d = (latest_close / previous_close) - 1
    signal = "BUY" if return_1d > 0 else "SELL"

    return {
        "symbol": symbol,
        "signal": signal,
        "return_1d": return_1d,
        "price_date": latest["date"].date().isoformat(),
    }


def store_signal(client: Client, signal_data: dict) -> dict:
    result = client.table("signals").insert(signal_data).execute()
    return result.data[0]


def main():
    client = get_supabase_client()
    df = fetch_eod_data(TICKER)

    if len(df) < 2:
        raise ValueError("Zu wenige Datenpunkte für Renditeberechnung")

    price_row = store_latest_price(client, df, TICKER)
    signal_row = calculate_signal(df, TICKER)
    stored_signal = store_signal(client, signal_row)

    print("Stored price:", price_row)
    print("Stored signal:", stored_signal)


if __name__ == "__main__":
    main()