import os
import time
import threading
import yfinance as yf
import pandas as pd
from flask import Flask
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID", "@alertadesinais_tredvip")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Live - EUR/USD"

def obter_dados():
    try:
        dados = yf.download("EURUSD=X", period="1d", interval="5m", progress=False)
        if dados.empty:
            print("Dados vazios do Yahoo")
            return None
        # Corrige MultiIndex do yfinance novo
        if isinstance(dados.columns, pd.MultiIndex):
            dados.columns = dados.columns.get_level_values(0)
        
        dados['EMA9'] = dados['Close'].ewm(span=9).mean()
        dados['EMA21'] = dados['Close'].ewm(span=21).mean()
        delta = dados['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        dados['RSI'] = 100 - (100 / (1 + rs))
        print(f"Dados OK: {len(dados)} candles | Close: {dados['Close'].iloc[-1]}")
        return dados
    except Exception as e:
        print(f"Erro obter dados: {e}")
        return None

def loop_sinais():
    print("Loop de sinais iniciado...")
    while True:
        try:
            dados = obter_dados()
            if dados is None or len(dados) < 30:
                time.sleep(60)
                continue
            
            ultimo = dados.iloc[-1]
            ema9 = float(ultimo['EMA9'])
            ema21 = float(ultimo['EMA21'])
            rsi = float(ultimo['RSI'])
            
            print(f"Analise: EMA9 {ema9:.5f} | EMA21 {ema21:.5f} | RSI {rsi:.2f}")
            
            sinal = None
            if ema9 > ema21 and rsi < 70 and rsi > 50:
                sinal = "🟢 COMPRA EUR/USD - M5"
            elif ema9 < ema21 and rsi > 30 and rsi < 50:
                sinal = "🔴 VENDA EUR/USD - M5"
            
            if sinal:
                msg = f"{sinal}\nEMA9: {ema9:.5f}\nEMA21: {ema21:.5f}\nRSI: {rsi:.2f}\n@alertadesinais_tredvip"
                bot.send_message(CHAT_ID, msg)
                print(f"SINAL ENVIADO: {sinal}")
                time.sleep(600)
            
            time.sleep(120)
        except Exception as e:
            print(f"Erro loop: {e}")
            time.sleep(60)

threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))).start()
threading.Thread(target=loop_sinais, daemon=True).start()
print("Bot VIP Online! Iniciando polling...")
bot.infinity_polling()
