# Carrinho Autônomo com Raspberry Pi

Projeto de carrinho robótico com visão computacional, detecção de objetos em tempo real, rastreamento GPS e stream de vídeo ao vivo via IP público.

## Visão geral

O sistema captura vídeo com uma webcam acoplada ao carrinho, transmite via rede para uma VM com IP público, processa os frames com YOLOv8 para detectar objetos e pessoas, e exibe tudo num painel web com mapa em tempo real via OpenStreetMap.

```
Raspberry Pi Zero 2 W
  └── Webcam USB (stream de vídeo)
  └── GPS NEO-M8N (posição em tempo real)
  └── WireGuard VPN
        └── VM Ubuntu (IP público)
              └── YOLOv8 (detecção de objetos)
              └── Flask + SocketIO (painel web)
              └── OpenStreetMap (mapa ao vivo)
                    └── Navegador (http://IP_PUBLICO)
```

## Hardware utilizado

| Componente | Modelo |
|---|---|
| Computador embarcado | Raspberry Pi Zero 2 W |
| Câmera | Logitech C930e (USB) |
| GPS | u-blox NEO-M8N |
| Sensor de presença | RCWL-0516 |
| VM | Ubuntu Server 22.04 LTS |

## Módulos implementados

| Módulo | Descrição | Status |
|---|---|---|
| Stream de vídeo | Webcam → WireGuard → VM → navegador | ✅ |
| Detecção de objetos | YOLOv8n em tempo real sobre o stream | ✅ |
| GPS ao vivo | Posição e trilha no mapa OpenStreetMap | ✅ |
| Sensor de distância | VL53L1X + frenagem automática | 🔜 |
| Controle do motor | Ponte H + comandos de movimento | 🔜 |
| Reconhecimento de gestos | MediaPipe Hands + comandos visuais | 🔜 |

## Estrutura do repositório

```
carrinho-autonomo-rpi/
├── README.md
├── docs/
│   ├── 01-configuracao-raspberry.md
│   ├── 02-configuracao-vm.md
│   ├── 03-wireguard.md
│   ├── 04-modulo-stream.md
│   ├── 05-modulo-deteccao.md
│   └── 06-modulo-gps.md
├── raspberry/
│   ├── requirements.txt
│   ├── stream_sender.py
│   ├── gps_sender.py
│   └── teste_sensor.py
├── vm/
│   ├── requirements.txt
│   ├── receiver.py
│   └── nginx/
│       └── carrinho.conf
└── web/
    └── index.html
```

## Início rápido

Siga os documentos na pasta `docs/` em ordem numérica:

1. [Configuração da Raspberry Pi](docs/01-configuracao-raspberry.md)
2. [Configuração da VM](docs/02-configuracao-vm.md)
3. [Configuração do WireGuard](docs/03-wireguard.md)
4. [Módulo de Stream](docs/04-modulo-stream.md)
5. [Módulo de Detecção](docs/05-modulo-deteccao.md)
6. [Módulo GPS](docs/06-modulo-gps.md)

## Requisitos de rede

- VM com IP público fixo
- Porta 51820/UDP aberta (WireGuard)
- Porta 80/TCP aberta (nginx)
- Porta 5000/TCP aberta (Flask)
- Raspberry Pi conectada ao Wi-Fi

## Licença

MIT
