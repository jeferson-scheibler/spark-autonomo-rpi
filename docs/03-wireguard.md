# 03 — Configuração do WireGuard

O WireGuard cria uma VPN leve entre a Raspberry Pi e a VM, permitindo comunicação direta sem depender de túnel SSH. É fundamental para o stream de vídeo e dados GPS fluírem com baixa latência.

## Endereços da VPN

| Dispositivo | IP na VPN |
|---|---|
| VM | 10.0.0.1 |
| Raspberry Pi | 10.0.0.2 |

## Na VM — gerar chaves e configurar

```bash
wg genkey | tee /tmp/vm_privkey | wg pubkey > /tmp/vm_pubkey
cat /tmp/vm_privkey   # anote a chave privada
cat /tmp/vm_pubkey    # anote a chave pública
```

Crie o arquivo de configuração:

```bash
sudo nano /etc/wireguard/wg0.conf
```

Cole (substituindo os valores):

```ini
[Interface]
PrivateKey = COLE_VM_PRIVKEY_AQUI
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = COLE_RASP_PUBKEY_AQUI
AllowedIPs = 10.0.0.2/32
```

## Na Raspberry — gerar chaves e configurar

```bash
wg genkey | tee /tmp/rasp_privkey | wg pubkey > /tmp/rasp_pubkey
cat /tmp/rasp_privkey   # anote a chave privada
cat /tmp/rasp_pubkey    # anote a chave pública
```

Crie o arquivo de configuração:

```bash
sudo nano /etc/wireguard/wg0.conf
```

Cole (substituindo os valores):

```ini
[Interface]
PrivateKey = COLE_RASP_PRIVKEY_AQUI
Address = 10.0.0.2/24

[Peer]
PublicKey = COLE_VM_PUBKEY_AQUI
Endpoint = IP_PUBLICO_DA_VM:51820
AllowedIPs = 10.0.0.1/32
PersistentKeepalive = 25
```

## Cruzar as chaves

- No `wg0.conf` da VM: preencha `COLE_RASP_PUBKEY_AQUI` com a chave pública da Raspberry
- No `wg0.conf` da Raspberry: preencha `COLE_VM_PUBKEY_AQUI` com a chave pública da VM

## Subir o WireGuard

Nos dois dispositivos:

```bash
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0
```

## Testar o túnel

Na Raspberry:

```bash
ping 10.0.0.1 -c 4
```

Na VM:

```bash
ping 10.0.0.2 -c 4
```

Ambos devem responder com latência baixa (geralmente abaixo de 5ms).

## Checklist

- [ ] Chaves geradas nos dois dispositivos
- [ ] Chaves cruzadas corretamente nos arquivos de configuração
- [ ] WireGuard iniciado e habilitado nos dois lados
- [ ] Ping funcionando nos dois sentidos
