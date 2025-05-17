from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime

app = FastAPI()

# Add CORS middleware to allow requests from React app on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/cbbi/latest")
def get_data():
    url = "https://colintalkscrypto.com/cbbi/data/latest.json"
    coingecko_url = "https://api.coingecko.com/api/v3/simple/price"

    cbb_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    # Step 1: Fetch CBBI data
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return JSONResponse(content={"error": "Failed to fetch data"}, status_code=500)

    data = response.json()
    results = []
    latest_values = {}
    timestamps = []

    for key in data:
        timestamp_keys = list(data[key].keys())
        if timestamp_keys:
            latest_timestamp = max(timestamp_keys, key=int)
            latest_timestamp_int = int(latest_timestamp)
            value = data[key].get(str(latest_timestamp_int))

            if value is not None:
                timestamps.append(latest_timestamp_int)
                date = datetime.fromtimestamp(latest_timestamp_int).strftime('%Y-%m-%d %H:%M')
                results.append({"metric": key, "date": date, "value": value})
                if key != "Price":
                    latest_values[key] = value

    if not timestamps:
        return JSONResponse(content={"error": "No valid timestamps found"}, status_code=500)

    average_value = sum(latest_values.values()) / len(latest_values)
    max_date = datetime.fromtimestamp(max(timestamps)).strftime('%Y-%m-%d %H:%M')
    min_date = datetime.fromtimestamp(min(timestamps)).strftime('%Y-%m-%d %H:%M')

    # Step 2: Fetch live BTC price from CoinGecko
    try:
        price_response = requests.get(coingecko_url, params={"ids": "bitcoin", "vs_currencies": "usd"})
        price_response.raise_for_status()
        live_price = price_response.json()["bitcoin"]["usd"]
    except Exception as e:
        live_price = None  # fallback in case of error

    return {
        "data": results,
        "summary": {
            "average_value": average_value,
            "max_date": max_date,
            "min_date": min_date
        },
        "live_btc_price": live_price
    }
