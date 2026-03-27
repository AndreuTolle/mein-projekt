import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")


def get_latest_signal():
    client = create_client(SUPABASE_URL, SUPABASE_KEY)

    response = (
        client.table("signals")
        .select("*")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        print("Kein Signal gefunden.")
        return

    signal = response.data[0]

    print("\nLatest Signal")
    print("-------------")
    print("Symbol:", signal["symbol"])
    print("Signal:", signal["signal"])
    print("Return (1d):", signal["return_1d"])
    print("Price Date:", signal["price_date"])
    print("Created At:", signal["created_at"])


if __name__ == "__main__":
    get_latest_signal()