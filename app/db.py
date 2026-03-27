import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")


def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL oder SUPABASE_ANON_KEY fehlt in .env")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def store_latest_price(client: Client, symbol: str, price_date: str, close: float) -> dict:
    payload = {
        "symbol": symbol,
        "date": price_date,
        "close": close,
    }
    result = client.table("prices").insert(payload).execute()
    return result.data[0]


def store_signal(client: Client, signal_data: dict) -> dict:
    result = client.table("signals").insert(signal_data).execute()
    return result.data[0]


def get_latest_signal(client: Client):
    response = (
        client.table("signals")
        .select("*")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if not response.data:
        return None
    return response.data[0]