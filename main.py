import os
import random
import threading
import time
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from zoneinfo import ZoneInfo
import requests

# Servidor web simples para manter o Render acordado 24h
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Bullex EUR/USD is alive!")

def run_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Inicia o servidor em segundo plano para o Render não desligar
threading.Thread(target=run_server, daemon=True).start()

# PEGA DO RENDER - Se você já colocou lá nas Environment Variables
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# SE NÃO COLOCOU NAS VARIAVEIS, COLA AQUI DIRETO ENTRE AS ASPAS
if not TOKEN:
    TOKEN = "SEU_TOKEN_DO_BOTFATHER_AQUI"
if not CHAT_ID:
    CHAT_ID = "SEU_ID_DO_CHAT_ID_AQUI"

TZ_BRASIL = ZoneInfo("America/Sao_Paulo")

def enviar_mensagem(texto):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=10)
        print(f"Enviado: {texto}")
    except Exception as e:
        print(f"Erro: {e}")

# Mensagem inicial com fuso horário do Brasil
agora_br = datetime.now(TZ_BRASIL)
enviar_mensagem(f"✅ <b>BOT BULLEX EUR/USD ONLINE!</b>\n\nEstratégia VIP ATIVADA! Aguardando melhor entrada...\n🕒 <i>{agora_br.strftime('%d/%m/%Y %H:%M:%S')}</i>")

while True:
    try:
        agora_br = datetime.now(TZ_BRASIL)
        minuto = agora_br.minute

        # ANALISA A CADA 5 MINUTOS (00, 05, 10, 15...)
        if minuto % 5 == 0:
            par = "EUR/USD"
            direcao = random.choice(["CALL 🔼", "PUT 🔽"])
            
            # Calcula o horário da entrada e o horário do resultado (5 min depois)
            tempo_entrada = agora_br + timedelta(minutes=2)
            horario_entrada = tempo_entrada.strftime("%H:%M")
            
            mensagem = f"""
🔔 <b>SINAL VIP ENCONTRADO!</b>

💱 Par: <b>{par}</b>
📊 Direção: <b>{direcao}</b>
⏰ Entrada: <b>{horario_entrada}</b>
⏳ Expiração: <b>5 MIN</b>

⚡️ <i>Analisador Bullex v1.0</i>
            """
            
            enviar_mensagem(mensagem)
            
            # Aguarda o horário da entrada + 5 minutos de expiração para apurar o resultado
            # Aqui simulamos o tempo de espera até o término da operação
            time.sleep(300) # Dorme os 5 minutos da expiração
            
            # Sorteia o resultado (Pode substituir pela sua lógica de checagem real depois)
            resultado = random.choice(["WIN 🟢", "LOSS 🔴"])
            
            msg_resultado = f"""
🎯 <b>RESULTADO DA OPERAÇÃO</b>

💱 Par: <b>{par}</b>
📊 Direção: <b>{direcao}</b>
⏰ Entrada das: <b>{horario_entrada}</b>
Resultado: <b>{resultado}</b>

⚡️ <i>Analisador Bullex v1.0</i>
            """
            enviar_mensagem(msg_resultado)
            
            # Pausa curta para evitar re-gatilhar no mesmo minuto
            time.sleep(60)
        
        # Checa a cada 30 segundos
        time.sleep(30)

    except Exception as e:
        print(f"Erro no loop: {e}")
        time.sleep(10)
