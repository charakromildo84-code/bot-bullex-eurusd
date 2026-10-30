import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Verifica se as variáveis existem
if not BOT_TOKEN:
    print("ERRO: BOT_TOKEN não encontrado no Environment!")
    while True:
        time.sleep(10)

if not CHAT_ID:
    print("ERRO: CHAT_ID não encontrado no Environment!")
    while True:
        time.sleep(10)

print(f"BOT INICIADO! Token OK...{BOT_TOKEN[-5:]} | Chat ID: {CHAT_ID}")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.get(url, params={"chat_id": CHAT_ID, "text": text})
        print(f"Mensagem enviada: {r.status_code}")
    except Exception as e:
        print(f"Erro ao enviar: {e}")

# Manda uma mensagem assim que liga
send_message("✅ BOT BULLEX EUR/USD ONLINE! - Teste OK Formado!")

# Loop a cada 5 min
while True:
    time.sleep(300)
    send_message("✅ BOTIUM TESTE: Bot ainda online - 5min")
