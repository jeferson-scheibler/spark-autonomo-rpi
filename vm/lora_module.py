# lora_module.py
import time
import json

def iniciar_lora(socketio):
    print("LoRa iniciado...")

    while True:
        # 🔄 SIMULA dados (depois você troca pelo LoRa real)
        dados = {
            "velocidade": 10,
            "bateria": 85,
            "status": "ok"
        }

        print("LoRa:", dados)

        # envia para o frontend via socket
        socketio.emit('telemetria', dados)

        time.sleep(2)
