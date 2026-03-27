from app.eod import fetch_eod_data
from app.db import get_supabase_client, store_latest_price, store_signal

TICKER = "SPY.US"


def calculate_signal(df, symbol: str) -> dict:
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


def main():
    client = get_supabase_client()
    df = fetch_eod_data(TICKER)

    if len(df) < 2:
        raise ValueError("Zu wenige Datenpunkte für Renditeberechnung")

    latest = df.iloc[0]
    price_row = store_latest_price(
        client=client,
        symbol=TICKER,
        price_date=latest["date"].date().isoformat(),
        close=float(latest["close"]),
    )

    signal_row = calculate_signal(df, TICKER)
    stored_signal = store_signal(client, signal_row)

    print("Stored price:", price_row)
    print("Stored signal:", stored_signal)


if __name__ == "__main__":
    main()