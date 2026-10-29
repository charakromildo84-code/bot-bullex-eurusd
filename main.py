import os, time, threading, requests, yfinance as yf
from flask import Flask
app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=15)
    except:
        pass

def analisar():
    try:
        df = yf.download("EURUSD=X", period="1d", interval="1m", progress=False)
        close = df['Close']
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_now = float(rsi.iloc[-1])
        preco = float(close.iloc[-1])
        ema9 = float(close.ewm(span=9).mean().iloc[-1])

        if rsi_now < 38:
            return "ACIMA", f"RSI {rsi_now:.0f} sobrevendido", preco
        elif rsi_now > 62:
            return "ABAIXO", f"RSI {rsi_now:.0f} sobrecomprado", preco
        elif preco > ema9:
            return "ACIMA", f"Acima EMA9 + RSI {rsi_now:.0f}", preco
        else:
            return "ABAIXO", f"Abaixo EMA9 + RSI {rsi_now:.0f}", preco
    except Exception as e:
        print(f"Erro analise: {e}")
        return "ACIMA", "Analise neutra", 1.08500

@app.route("/")
def home():
    return "Bot Bullex OK - 5+5 min - Lendo Grafico"

def bot_loop():
    while True:
        try:
            direcao, motivo, entrada = analisar()
            emoji = "📈" if direcao == "ACIMA" else "📉"
            
            send_telegram(f"🔔 <b>SINAL BULLEX EUR/USD (OTC)</b>\n\n<b>Direcao: {direcao} {emoji}</b>\nMotivo: {motivo}\nEntrada: {entrada:.5f}\nTempo: 5min Blitz\nValor: $9 (88%)")

            time.sleep(300) # 5 min expiracao

            df2 = yf.download("EURUSD=X", period="1d", interval="1m", progress=False)
            saida = float(df2['Close'].iloc[-1])
            win = (direcao == "ACIMA" and saida > entrada) or (direcao == "ABAIXO" and saida < entrada)

            if win:
                send_telegram(f"✅ <b>WIN +$7,92 (88%)</b>\n{direcao} {entrada:.5f} -> {saida:.5f}")
            else:
                send_telegram(f"❌ <b>LOSS -$9</b>\n{direcao} {entrada:.5f} -> {saida:.5f}\nGale 1 = $18")

            time.sleep(300) # 5 min intervalo

        except Exception as e:
            print(f"Erro loop: {e}")
            time.sleep(60)

threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
