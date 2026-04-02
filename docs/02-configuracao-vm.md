# 02 — Configuração da VM

## Pré-requisitos

- Ubuntu Server 22.04 LTS
- IP público fixo já atribuído
- Acesso SSH com usuário sudo

## Passo 1 — Atualizar o sistema

```bash
sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt upgrade -y
```

## Passo 2 — Instalar pacotes

```bash
sudo apt install -y nginx python3-pip python3-venv git ufw wireguard
```

## Passo 3 — Desativar atualizador automático

```bash
sudo systemctl disable unattended-upgrades
sudo systemctl stop unattended-upgrades
```

## Passo 4 — Configurar o firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 5000/tcp
sudo ufw allow 51820/udp
sudo ufw enable
```

## Passo 5 — Configurar o nginx

```bash
sudo nano /etc/nginx/sites-available/carrinho
```

Cole o conteúdo do arquivo `vm/nginx/carrinho.conf` deste repositório.

Ative a configuração:

```bash
sudo ln -s /etc/nginx/sites-available/carrinho /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

Crie a pasta da página:

```bash
sudo mkdir -p /var/www/carrinho
sudo chown $USER:$USER /var/www/carrinho
```

Copie o arquivo `web/index.html` deste repositório para `/var/www/carrinho/index.html`.

## Passo 6 — Criar o ambiente Python

```bash
mkdir ~/carrinho && cd ~/carrinho
python3 -m venv venv
source venv/bin/activate
pip install opencv-python-headless flask flask-socketio \
            ultralytics python-socketio eventlet
```

## Passo 7 — Habilitar túnel reverso SSH (opcional, apenas para testes)

Caso precise de acesso temporário antes do WireGuard estar configurado:

```bash
sudo nano /etc/ssh/sshd_config
```

Adicione ou confirme:

```
GatewayPorts yes
AllowTcpForwarding yes
```

```bash
sudo systemctl restart sshd
```

## Passo 8 — Configurar serviço systemd

```bash
sudo nano /etc/systemd/system/carrinho.service
```

Cole:

```ini
[Unit]
Description=Carrinho - Receiver e Painel Web
After=network.target

[Service]
User=admlab
WorkingDirectory=/home/admlab/carrinho
ExecStart=/home/admlab/carrinho/venv/bin/python receiver.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable carrinho
```

Inicie após configurar o WireGuard e copiar os scripts:

```bash
sudo systemctl start carrinho
```

## Checklist

- [ ] Sistema atualizado
- [ ] nginx rodando e acessível via `http://IP_PUBLICO`
- [ ] Firewall configurado
- [ ] Ambiente Python com dependências instaladas
- [ ] Serviço systemd criado
