import os, threading, time, requests, random
from flask import Flask
app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN","")
CHANNEL_ID = os.environ.get("CHANNEL_ID","")
def enviar(m):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHANNEL_ID, "text": m, "parse_mode": "HTML"}, timeout=10)
    except: pass
def bot_loop():
    enviar("🚀 Bot reconfigurado! Agora com WIN/LOSS automatico $9")
    while True:
        direcao = random.choice(["COMPRA","VENDA"])
        botao = "ACIMA" if direcao=="COMPRA" else "ABAIXO"
        preco = 1.12 + random.uniform(0.005,0.04)
        enviar(f"🔔 <b>SINAL BULLEX EUR/USD</b>\n\nDirecao: <b>{direcao} - {botao}</b>\nValor: <b>$9</b>\nEntrada: <b>{preco:.5f}</b>\nTempo: <b>M5</b>\n\nEntre na proxima vela!")
        time.sleep(300)
        preco_f = preco + random.uniform(-0.003,0.003)
        win = preco_f > preco if direcao=="COMPRA" else preco_f < preco
        if win:
            enviar(f"✅ <b>WIN +88%</b> +$7,92\nEntrada {preco:.5f} -> {preco_f:.5f}")
        else:
            enviar(f"❌ <b>LOSS</b> {preco:.5f}->{preco_f:.5f}\nGALE 1 = $18")
        time.sleep(10)
@app.route("/")
def home(): return "Bot Online $9 WIN/LOSS"
@app.route("/status")
def status(): return "Rodando 24h"
threading.Thread(target=bot_loop, daemon=True).start()
