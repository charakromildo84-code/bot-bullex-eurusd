import os
import threading
from flask import Flask
import telebot

# Pega o token que está no Render
TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN") or os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Formado's Bot Online!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bot Formado's online!")

# ADICIONE SEUS OUTROS COMANDOS AQUI SE TIVER

def rodar_bot():
    print("Iniciando Bot...")
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(
        target=rodar_bot,
        daemon=True
    )
    t.start()
    p = int(
        os.environ.get("PORT", 10000)
    )
    app.run(
        host="0.0.0.0",
        port=p
    )
