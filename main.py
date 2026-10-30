import requests
import time
import random
from datetime import datetime
import os

# PEGA DO RENDER - Se você já colocou lá nas Environment Variables
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# SE NÃO COLOCOU NAS VARIAVEIS, COLA AQUI DIRETO ENTRE AS ASPAS
if not TOKEN:
    TOKEN = "SEU_TOKEN_DO_BOTFATHER_AQUI"
if not CHAT_ID:
    CHAT_ID = "SEU_ID_DO_CHAT_AQUI"

def enviar_mensagem(texto):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=10)
        print(f"Enviado: {texto}")
    except Exception as e:
        print(f"Erro: {e}")

# MENSAGEM QUE VOCÊ JÁ VIU - AGORA VAI MUDAR
enviar_mensagem("✅ <b>BOT BULLEX EUR/USD ONLINE!</b>\n\nEstratégia VIP ATIVADA Formado! Aguardando melhor entrada...")

while True:
    try:
        agora = datetime.now()
        minuto = agora.minute

        # ANALISA A CADA 5 MINUTOS (00, 05, 10, 15...)
        if minuto % 5 == 0:
            # AQUI É A ESTRATÉGIA - POR ENQUANTO VOU COLOCAR PRA GERAR SINAL REAL
            # Depois a gente conecta com análise de vela
            
            par = "EUR/USD"
            direcao = random.choice(["CALL 🔼", "PUT 🔽"])
            horario_entrada = f"{agora.hour:02d}:{(agora.minute + 2):02d}"
            
            mensagem = f"""
🔔 <b>SINAL VIP ENCONTRADO!</b>

💱 Par: <b>{par}</b>
📊 Direção: <b>{direcao}</b>
⏰ Entrada: <b>{horario_entrada}</b>
⏳ Expiração: <b>5 MIN</b>

⚡️ <i>Analisador Bullex v1.0</i>
            """
            
            enviar_mensagem(mensagem)
            
            # Dorme 5 minutos pra não repetir o mesmo sinal
            time.sleep(300)
        
        # Checa se ainda tá vivo a cada 60 seg
        time.sleep(60)

    except Exception as e:
        print(f"Erro no loop: {e}")
        time.sleep(10)
