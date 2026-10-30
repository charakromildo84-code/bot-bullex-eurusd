import os
import time
import threading
import random
from flask import Flask
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID", "@alertadesinais_tredvip")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Live - MODO ESTUDO"

def loop_sinais():
    print("Loop MODO ESTUDO iniciado - mandando a cada 5 min")
    count = 0
    while True:
        try:
            count += 1
            # Alterna entre compra e venda pra estudo
            if random.choice([True, False]):
                sinal = "🟢 COMPRA EUR/USD - M5"
                motivo = "Tendencia de alta"
            else:
                sinal = "🔴 VENDA EUR/USD - M5"
                motivo = "Tendencia de baixa"

            msg = f"""📊 SINAL DE ESTUDO #{count} - EUR/USD M5

{sinal}
Horario: 5 minutos
Estrategia: Estudo

⚠️ MODO TESTE - Apenas para estudo

@alertadesinais_tredvip"""

            bot.send_message(CHAT_ID, msg)
            print(f"SINAL ENVIADO #{count}: {sinal}")
            
            # Espera 5 minutos = 300 segundos
            time.sleep(300)
            
        except Exception as e:
            print(f"Erro loop: {e}")
            time.sleep(60)

threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))).start()
threading.Thread(target=loop_sinais, daemon=True).start()
print("Bot VIP Online MODO ESTUDO!")
bot.infinity_polling()
