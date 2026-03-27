import os
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

app = FastAPI()


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
        return None

    return response.data[0]


@app.get("/")
def home():
    signal = get_latest_signal()

    if not signal:
        return {"message": "No signal found"}

    return {
        "symbol": signal["symbol"],
        "signal": signal["signal"],
        "return_1d": signal["return_1d"],
        "price_date": signal["price_date"],
        "created_at": signal["created_at"],
    }