# 01 — Configuração da Raspberry Pi Zero 2 W

## O que você vai precisar

- Cartão microSD (mínimo 16GB, recomendado 32GB classe 10)
- Computador com leitor de cartão SD
- Cabo micro USB para alimentação
- Webcam USB + adaptador micro USB OTG

## Passo 1 — Gravar o sistema operacional

Baixe o [Raspberry Pi Imager](https://www.raspberrypi.com/software) e configure:

- **Device:** Raspberry Pi Zero 2 W
- **OS:** Raspberry Pi OS Lite (64-bit)
- **Storage:** seu cartão SD

Antes de gravar, abra as configurações avançadas e preencha:

| Campo | Valor |
|---|---|
| Hostname | `carrinho` |
| Username | `pi` |
| Senha | sua preferência |
| Wi-Fi SSID | nome da sua rede |
| Wi-Fi Password | senha da sua rede |
| SSH | habilitado (autenticação por senha) |
| Timezone | America/Sao_Paulo |
| Teclado | pt-BR |

## Passo 2 — Primeiro acesso

Após inserir o SD e ligar, aguarde 2 minutos. Descubra o IP da Raspberry no seu roteador ou via nmap:

```bash
nmap -sn 192.168.1.0/24
```

Acesse via SSH:

```bash
ssh pi@IP_DA_RASPBERRY
```

## Passo 3 — Atualizar o sistema

```bash
sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt upgrade -y
```

## Passo 4 — Instalar pacotes base

```bash
sudo apt install -y python3-pip python3-venv git ffmpeg v4l-utils wireguard
```

## Passo 5 — Habilitar porta serial (para o GPS)

```bash
sudo raspi-config
```

Navegue em **Interface Options → Serial Port**:
- Login shell via serial → **No**
- Hardware serial port → **Yes**

Reinicie:

```bash
sudo reboot
```

Confirme que a porta está disponível:

```bash
ls /dev/serial0
```

## Passo 6 — Criar o ambiente Python

```bash
mkdir ~/carrinho && cd ~/carrinho
python3 -m venv venv
source venv/bin/activate
pip install opencv-python-headless pyserial pynmea2 RPi.GPIO \
            python-socketio[client] websocket-client
```

## Passo 7 — Testar a webcam

Conecte a webcam via adaptador OTG e verifique:

```bash
v4l2-ctl --list-devices
```

Deve aparecer a webcam em `/dev/video0`.

## Checklist

- [ ] SSH funcionando
- [ ] Sistema atualizado
- [ ] Porta serial habilitada (`/dev/serial0` existe)
- [ ] Webcam reconhecida em `/dev/video0`
- [ ] Ambiente virtual Python criado em `~/carrinho/venv`
- [ ] Pacotes instalados sem erro
