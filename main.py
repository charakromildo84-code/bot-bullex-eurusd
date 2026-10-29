import os, time, random, threading, requests
from flask import Flask
app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=10)
    except: pass

@app.route("/")
def home(): return "Bot Online $9 - Sem Flood"

def bot_loop():
    while True:
        try:
            preco = 1.08500 + random.uniform(-0.003, 0.003)
            send_telegram(f"🔔 SINAL BULLEX EUR/USD\nValor: $9\nDirecao: COMPRA 📈\nEntrada: {preco:.5f}\nTempo: M5")
            time.sleep(300)
            if random.choice([True,True,True,False]):
                send_telegram("✅ WIN +88% +$7,92 - EURUSD")
            else:
                send_telegram("❌ LOSS EURUSD - GALE 1 = $18")
            time.sleep(600)
        except: time.sleep(60)

threading.Thread(target=bot_loop, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
