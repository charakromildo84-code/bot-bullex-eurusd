import os
import threading
import time
import requests
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "COLOQUE_SEU_TOKEN_AQUI")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@seu_canal_ou_id")

@app.route("/")
def home():
    return "Bot Bullex EURUSD Online!"

@app.route("/status")
def status():
    return "Rodando 24h no Render"

def enviar_sinal():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    while True:
        try:
            mensagem = "🔔 SINAL BULLEX EURUSD\n\nPar: EURUSD\nDireção: COMPRA 📈\nHorário: Próxima vela M5\n\nTeste bot rodando!"
            data = {"chat_id": CHANNEL_ID, "text": mensagem}
            requests.post(url, data=data, timeout=10)
            print("Sinal enviado!")
        except Exception as e:
            print(f"Erro: {e}")
        time.sleep(300)  # envia a cada 5 minutos para teste

if __name__ == "__main__":
    t = threading.Thread(target=enviar_sinal)
    t.daemon = True
    t.start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Bullex EURUSD Online!"

@app.route("/status")
def status():
    return "Rodando 24h no Railway"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
