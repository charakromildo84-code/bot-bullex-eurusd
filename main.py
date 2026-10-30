import os
import time
import random
import threading
from flask import Flask
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not BOT_TOKEN:
    BOT_TOKEN = "SEU_TOKEN_AQUI"
if not CHAT_ID:
    CHAT_ID = "-1002707115162"

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

@app.route('/')
def home():
    return "Bot Live - OK", 200

def loop_sinais():
    print("Loop iniciado")
    while True:
        try:
            direcao = random.choice(["COMPRA", "VENDA"])
            horario = time.strftime("%H:%M:%S")
            msg = f"🚀 SINAL VIP - MODO ESTUDO 🚀\nPar: EUR/USD\nDirecao: {direcao}\nHorario: {horario}"
            bot.send_message(CHAT_ID, msg)
            print(f"Enviado: {direcao}")
        except Exception as e:
            print(f"Erro: {e}")
        time.sleep(300)

threading.Thread(target=loop_sinais, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
