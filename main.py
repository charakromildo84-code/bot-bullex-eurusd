import os
import threading
import time
from datetime import datetime, timedelta
import pytz
from flask import Flask
import telebot
import yfinance as yf

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

ultima_direcao = None

@app.route('/')
def home():
    return "Bot Bullex OK - Rodando 24h"

def enviar_sinal(direcao):
    try:
        agora = datetime.now(pytz.timezone('America/Sao_Paulo'))
        msg = f"""🚨 **SINAL BULLEX - EUR/USD** 🚨

📊 Par: EUR/USD
⏰ Tempo: M5
📈 Direção: **{direcao}**
🕒 Horário: {agora.strftime('%H:%M:%S - %d/%m/%Y')}

✅ Entra na próxima vela!

@alertadesinais_tredvip"""
        bot.send_message(CHANNEL_ID, msg, parse_mode='Markdown')
        print(f"Sinal enviado: {direcao}")
    except Exception as e:
        print(f"Erro ao enviar sinal: {e}")

def loop_sinais():
    global ultima_direcao
    print("Loop de sinais iniciado...")
    while True:
        try:
            # Pega EUR/USD
            dados = yf.download("EURUSD=X", period="2d", interval="5m", progress=False)
            
            if len(dados) < 30:
                time.sleep(60)
                continue

            # Calcula EMA 9, EMA 21 e RSI
            dados['EMA9'] = dados['Close'].ewm(span=9).mean()
            dados['EMA21'] = dados['Close'].ewm(span=21).mean()
            
            delta = dados['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            dados['RSI'] = 100 - (100 / (1 + rs))

            ultimo = dados.tail(1)
            ema9 = float(ultimo['EMA9'].iloc[0])
            ema21 = float(ultimo['EMA21'].iloc[0])
            rsi = float(ultimo['RSI'].iloc[0])

            print(f"Analise: EMA9 {ema9:.5f} | EMA21 {ema21:.5f} | RSI {rsi:.2f}")

            direcao = None
            if ema9 > ema21 and 45 < rsi < 70:
                direcao = "COMPRA"
            elif ema9 < ema21 and 30 < rsi < 55:
                direcao = "VENDA"

            if direcao and direcao != ultima_direcao:
                enviar_sinal(direcao)
                ultima_direcao = direcao

            time.sleep(60)

        except Exception as e:
            print(f"Erro loop: {e}")
            time.sleep(10)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bot VIP Online! Sinais EUR/USD M5 ativos 24h")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000))), daemon=True).start()
    threading.Thread(target=loop_sinais, daemon=True).start()
    bot.infinity_polling()
