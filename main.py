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
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=15)
    except Exception as e:
        print(f"Erro: {e}")

def analisar():
    try:
        data = yf.download("EURUSD=X", period="1d", interval="1m", progress=False, auto_adjust=True)
        if data.empty or len(data) < 30:
            return None, None
        close = data['Close']
        if hasattr(close, 'columns'):
            close = close.iloc[:, 0]
        close = close.dropna()
        ema9 = float(close.ewm(span=9).mean().iloc[-1])
        ema21 = float(close.ewm(span=21).mean().iloc[-1])
        preco = float(close.iloc[-1])
        direcao = "COMPRA (CALL) 🟢" if ema9 > ema21 else "VENDA (PUT) 🔴"
        return direcao, preco
    except Exception as e:
        print(f"Erro analisar: {e}")
        return None, None

def loop():
    time.sleep(10)
    enviar("✅ *Bot Bullex ligado!*\nSinal a cada 5min + WIN/LOSS")
    while True:
        try:
            direcao, pe = analisar()
            if direcao:
                enviar(f"📊 *SINAL EUR/USD - 5 MIN*\n\nDireção: *{direcao}*\nPreço: {pe:.5f}\n\nEntra agora! Resultado em 5min")
                time.sleep(300)
                _, pa = analisar()
                if pa:
                    win = (pa > pe) if "COMPRA" in direcao else (pa < pe)
                    txt = f"✅ *WIN GREEN!* {pe:.5f} -> {pa:.5f}" if win else f"❌ *LOSS RED!* {pe:.5f} -> {pa:.5f}"
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
