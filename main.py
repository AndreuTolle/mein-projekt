from supabase import create_client
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

client = create_client(SUPABASE_URL, SUPABASE_KEY)


def insert_market_data():
    data = {
        "symbol": "TEST",
        "price": 95.0,
        "created_at": datetime.utcnow().isoformat(),
    }

    response = client.table("market_data").insert(data).execute()
    print("Inserted market_data:", response.data)


def generate_signal():
    response = client.table("market_data").select("*").order("created_at", desc=True).limit(1).execute()

    latest = response.data[0]

    signal = "BUY" if latest["price"] < 100 else "SELL"

    signal_data = {
        "symbol": latest["symbol"],
        "signal": signal,
        "created_at": datetime.utcnow().isoformat(),
    }

    response = client.table("signals").insert(signal_data).execute()
    print("Inserted signal:", response.data)


if __name__ == "__main__":
    insert_market_data()
    generate_signal()