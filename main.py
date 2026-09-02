import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

sent_stocks = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

send_telegram("🚀 NSE 14% Alert Bot Started!")

while True:
    try:
        url = "https://www.nseindia.com/api/market-data-pre-open?key=ALL"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        data = requests.get(url, headers=headers).json()

        for item in data["data"]:
            stock = item["metadata"]["symbol"]
            change = float(item["metadata"]["pChange"])
            price = float(item["metadata"]["lastPrice"])

            if change >= 14 and price >= 200 and stock not in sent_stocks:
                send_telegram(
                    f"🔥 NSE ALERT\n\n{stock}\nPrice: ₹{price}\nGain: {change}%"
                )
                sent_stocks.add(stock)

    except Exception as e:
        print(e)

    time.sleep(300)
