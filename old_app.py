from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client
from dotenv import load_dotenv
import os

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


@app.get("/", response_class=HTMLResponse)
def home():
    signal = get_latest_signal()

    if not signal:
        return "<h2>No signal available</h2>"

    html = f"""
    <html>
        <head>
            <title>Latest Signal</title>
            <style>
                body {{
                    font-family: Arial;
                    margin: 40px;
                    background-color: #f5f5f5;
                }}
                .card {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    width: 400px;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                }}
                .signal {{
                    font-size: 28px;
                    font-weight: bold;
                    color: {"green" if signal["signal"] == "BUY" else "red"};
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Latest Signal</h2>
                <p><strong>Symbol:</strong> {signal["symbol"]}</p>
                <p class="signal">{signal["signal"]}</p>
                <p><strong>Return (1d):</strong> {signal["return_1d"]:.4f}</p>
                <p><strong>Price Date:</strong> {signal["price_date"]}</p>
                <p><strong>Updated At:</strong> {signal["created_at"]}</p>
            </div>
        </body>
    </html>
    """

    return html