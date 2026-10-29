import os
import time
import threading
import requests
import yfinance as yf
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except:
        pass

def analisar():
    try:
        data = yf.download("EURUSD=X", period="1d", interval="1m", progress=False)
        close = data['Close']
        ema9 = close.ewm(span=9).mean().iloc[-1]
        ema21 = close.ewm(span=21).mean().iloc[-1]
        preco = close.iloc[-1]
        direcao = "COMPRA (CALL) 🟢" if ema9 > ema21 else "VENDA (PUT) 🔴"
        return direcao, float(preco)
    except:
        return None, None

def loop():
    time.sleep(10)
    enviar("✅ *Bot Bullex ligado!*\nSinal a cada 5min + resultado WIN/LOSS")
    while True:
        try:
            direcao, preco = analisar()
            if direcao:
                pe = preco
                enviar(f"📊 *SINAL EUR/USD - 5 MIN*\n\nDireção: *{direcao}*\nPreço: {pe:.5f}\n\nEntra agora! Resultado em 5min")
                time.sleep(300)
                _, pa = analisar()
                if pa:
                    win = (pa > pe) if "COMPRA" in direcao else (pa < pe)
                    txt = f"✅ *WIN GREEN!*\n{pe:.5f} -> {pa:.5f}" if win else f"❌ *LOSS RED!*\n{pe:.5f} -> {pa:.5f}"
                    enviar(txt)
            else:
                time.sleep(60)
        except:
            time.sleep(60)

threading.Thread(target=loop, daemon=True).start()

@app.route("/")
def home():
    return "Bot Bullex OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
