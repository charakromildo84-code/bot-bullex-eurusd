import os, threading, time, requests, random
from flask import Flask

app = Flask(__name__)
TOKEN = os.getenv("BOT_TOKEN","")
CHAT = os.getenv("CHANNEL_ID","")

def enviar(txt):
    url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": CHAT,
            "text": txt,
            "parse_mode": "HTML"
        }, timeout=10)
    except:
        pass

def bot_loop():
    enviar("🚀 Bot reconfigurado! $9 WIN/LOSS auto")
    while True:
        d = "COMPRA"
        if random.random() > 0.5:
            d = "VENDA"
        b = "ACIMA"
        if d == "VENDA":
            b = "ABAIXO"
        p = 1.12 + random.uniform(0.005, 0.04)

        msg = "🔔 <b>SINAL BULLEX EUR/USD</b>\n\n"
        msg += f"Direcao: <b>{d} - {b}</b>\n"
        msg += f"Valor: <b>$9</b>\n"
        msg += f"Entrada: <b>{p:.5f}</b>\n"
        msg += f"Tempo: <b>M5</b>"

        enviar(msg)
        time.sleep(300)

        f = p + random.uniform(-0.003, 0.003)
        win = False
        if d == "COMPRA":
            win = f > p
        else:
            win = f < p

        if win:
            enviar(f"✅ <b>WIN +88%</b> +$7,92\n{p:.5f}->{f:.5f}")
        else:
            enviar(f"❌ <b>LOSS</b> {p:.5f}->{f:.5f}\nGALE 1 = $18")

        time.sleep(10)

@app.route("/")
def home():
    return "Bot Online $9"

@app.route("/status")
def status():
    return "Rodando 24h"

threading.Thread(target=bot_loop, daemon=True).start()
