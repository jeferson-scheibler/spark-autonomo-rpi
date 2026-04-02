# 06 — Módulo GPS

Rastreamento de posição em tempo real com o módulo u-blox NEO-M8N. A posição é enviada via SocketIO para a VM e exibida no painel web com mapa OpenStreetMap, incluindo trilha do trajeto percorrido.

## Hardware

| Componente | Detalhe |
|---|---|
| Módulo | u-blox NEO-M8N |
| Interface | UART (RXD/TXD) |
| Tensão | 3.3V |
| Baud rate | 9600 |
| Constelações | GPS, GLONASS, Galileo |
| Precisão | ~2-3 metros |

## Conexão física

| Pino do GPS | Pino da Raspberry | GPIO |
|---|---|---|
| VCC | Pino 1 | 3.3V |
| GND | Pino 6 | GND |
| TXD | Pino 10 | GPIO 15 (RX) |
| RXD | Pino 8 | GPIO 14 (TX) |
| SDA | não conectar | — |
| SCL | não conectar | — |

> **Atenção:** TX do GPS conecta no RX da Raspberry e vice-versa.

## Configuração da porta serial

Execute na Raspberry:

```bash
sudo raspi-config
```

**Interface Options → Serial Port:**
- Login shell via serial → **No**
- Hardware serial port → **Yes**

Reinicie e confirme:

```bash
ls /dev/serial0
```

## Instalação das dependências

```bash
cd ~/carrinho
source venv/bin/activate
pip install pyserial pynmea2 python-socketio[client] websocket-client
```

## Arquitetura de comunicação

```
GPS (UART) → Raspberry Pi
  └── gps_sender.py
        └── SocketIO (WireGuard 10.0.0.1:5000)
              └── receiver.py na VM
                    └── broadcast para navegadores conectados
                          └── Mapa OpenStreetMap atualizado em tempo real
```

## Sentenças NMEA utilizadas

| Sentença | Dados extraídos |
|---|---|
| `$GNGGA` / `$GPGGA` | Latitude, longitude, altitude, satélites |
| `$GNRMC` / `$GPRMC` | Latitude, longitude, velocidade sobre o solo |

## Primeiro fix de satélites

Na primeira vez ou após longo período sem uso, o módulo pode levar de 1 a 3 minutos para adquirir sinal (cold start). Após o primeiro fix, o tempo de aquisição reduz significativamente.

Coloque o módulo próximo a uma janela ou em ambiente aberto para melhor recepção.

## Na Raspberry — gps_sender.py

Execute:

```bash
cd ~/carrinho
source venv/bin/activate
python gps_sender.py
```

O script conecta ao receiver da VM via SocketIO e emite os dados GPS a cada leitura válida.

## No painel web

O mapa exibe:

- Ponto verde indicando a posição atual
- Trilha verde acumulando o trajeto percorrido
- Coordenadas, altitude, satélites e velocidade no painel lateral

## Checklist

- [ ] Porta serial habilitada (`/dev/serial0`)
- [ ] GPS conectado e testado com `teste_sensor.py`
- [ ] Fix de satélites adquirido (mínimo 4 satélites recomendado)
- [ ] `gps_sender.py` conectando à VM sem erro
- [ ] Ponto e trilha aparecendo no mapa do painel web
