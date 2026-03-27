from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.db import get_supabase_client, get_latest_signal

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    client = get_supabase_client()
    signal = get_latest_signal(client)

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