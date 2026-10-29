import os
import threading
import time
from datetime import datetime, timedelta
import pytz
from flask import Flask
import telebot
import yfinance as yf

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID") or "@alertadesinais_tredvip"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

ultima_direcao = None

@app.route('/')
def home():
    return "Bot Bullex VIP Online!"

def calcular_rsi(series, periodo=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def enviar_sinal(direcao):
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso)
    proxima = agora + timedelta(minutes=5 - agora.minute % 5)
    proxima = proxima.replace(second=0, microsecond=0)
    horario = proxima.strftime("%H:%M")
    
    if direcao == "COMPRA":
        txt = f"📈 COMPRA"
    else:
        txt = f"📉 VENDA"

    msg = f"""🔔 SINAL BULLEX EURUSD - VIP

Par: EURUSD {txt}
Direção: {direcao}
Horário: Próxima vela M5 - {horario}
Entrada até: {(proxima + timedelta(minutes=2)).strftime('%H:%M')}
Estratégia: EMA9 x EMA21 + RSI

⚠️ Entrar na próxima vela, 1 Gale
@alertadesinais_tredvip"""

    try:
        bot.send_message(CHANNEL_ID, msg)
        print(f"SINAL ENVIADO: {direcao}")
    except Exception as e:
        print(f"Erro: {e}")

def loop_sinais():
    global ultima_direcao
    print("BOT VIP INICIADO - Analisando EURUSD...")
    while True:
        try:
            time.sleep(60)
            dados = yf.download("EURUSD=X", period="2d", interval="5m", progress=False)
            if len(dados) < 30:
                continue
            
            dados['EMA9'] = dados['Close'].ewm(span=9).mean()
            dados['EMA21'] = dados['Close'].ewm(span=21).mean()
            dados['RSI'] = calcular_rsi(dados['Close'], 14)
            
            ultimo = dados.iloc[-2]
            ema9 = float(ultimo['EMA9'].iloc[0] if hasattr(ultimo['EMA9'], 'iloc') else ultimo['EMA9'])
            ema21 = float(ultimo['EMA21'].iloc[0] if hasattr(ultimo['EMA21'], 'iloc') else ultimo['EMA21'])
            rsi = float(ultimo['RSI'].iloc[0] if hasattr(ultimo['RSI'], 'iloc') else ultimo['RSI'])
            
            print(f"Analise: EMA9 {ema9:.5f} | EMA21 {ema21:.5f} | RSI {rsi:.1f}")

            direcao = None
            if ema9 > ema21 and 45 < rsi < 70:
                direcao = "COMPRA"
            elif ema9 < ema21 and 30 < rsi < 55:
                direcao = "VENDA"

            if direcao and direcao != ultima_direcao:
                enviar_sinal(direcao)
                ultima_direcao = direcao

        except Exception as e:
            print(f"Erro loop: {e}")
            time.sleep(10)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bot VIP Online! Sinais indo pro canal.")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()
    loop_sinais()
    bot.infinity_polling()
