import os, threading, time, requests, random
from flask import Flask

app = Flask(__name__)
TOKEN = os.getenv("BOT_TOKEN","")
CHAT = os.getenv("CHANNEL_ID","")
API = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def enviar(txt):
    try:
        requests.post(API, json={
            "chat_id": CHAT,
            "text": txt,
            "parse_mode": "HTML"
        }, timeout=10)
    except:
        pass

def bot_loop():
    enviar("🚀 Bot reconfigurado! $9 WIN/LOSS auto")
    while True:
        d = random.choice(["COMPRA","VENDA"])
        b = "ACIMA" if d=="COMPRA" else "ABAIXO"
        p = 1.12 + random.uniform(0.005,0.04)

        enviar(
            f"🔔 <b>SINAL BULLEX EUR/USD</b>\n\n"
            f"Direcao: <b>{d} - {b}</b>\n"
            f"Valor: <b>$9</b>\n"
            f"Entrada: <b>{p:.5f}</b>\n"
            f"Tempo: <b>M5</b>"
        )

        time.sleep(300)
        f = p + random.uniform(-0.003,0.003)
        win = f > p if d=="COMPRA" else f < p

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
