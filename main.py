import os,time,threading
import telebot
from flask import Flask
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
bot=telebot.TeleBot(BOT_TOKEN)
app=Flask(__name__)
@app.route('/')
def home():
    return "ONLINE",200
def loop():
    print("Loop iniciado",flush=True)
    time.sleep(5)
    while True:
        try:
            bot.send_message(CHAT_ID,"🔥 TESTE - Bot Bullex EURUSD ONLINE")
            print("Enviado!",flush=True)
        except Exception as e:
            print(f"Erro: {e}",flush=True)
        time.sleep(300)
threading.Thread(target=loop,daemon=True).start()
if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
