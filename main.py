import os
import threading
from flask import Flask
import telebot
import time

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID") or "@alertadesinais_tredvip"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Formado's Bot Online!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bot Formado's online e mandando sinais no canal VIP!")

def loop_sinais():
    print("Bot iniciado - Mandando teste no canal...")
    while True:
        try:
            # Teste pra ver se tá mandando no canal
            bot.send_message(CHANNEL_ID, "✅ Bot Bullex EURUSD Conectado! Aguardando sinais...")
            print("Mensagem de teste enviada pro canal!")
            break
        except Exception as e:
            print(f"Erro ao mandar no canal: {e}")
            print("Verifica se o bot é ADM no canal @alertadesinais_tredvip")
            time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()
    loop_sinais()
    bot.infinity_polling()
