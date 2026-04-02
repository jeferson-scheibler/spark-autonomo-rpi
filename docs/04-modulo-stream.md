# 04 — Módulo de Stream de Vídeo

Captura o vídeo da webcam na Raspberry Pi e transmite via WireGuard para a VM, que serve o stream no painel web.

## Arquitetura

```
Raspberry Pi (/dev/video0)
  └── stream_sender.py (OpenCV → socket TCP :8080)
        └── WireGuard (10.0.0.1 → 10.0.0.2)
              └── receiver.py na VM (lê o stream)
                    └── nginx (:80) → navegador
```

## Hardware

- Webcam Logitech C930e (USB)
- Adaptador micro USB OTG (necessário no Zero 2 W)

## Webcam testada

A câmera suporta os seguintes formatos confirmados via `v4l2-ctl`:

- **MJPG** (Motion-JPEG) — usado pelo projeto
- **YUYV** — disponível mas não utilizado

Resolução padrão do projeto: `320x240 @ 15fps` (balanceado para o Zero 2 W).

## Na Raspberry — stream_sender.py

Arquivo localizado em `raspberry/stream_sender.py`.

Execute:

```bash
cd ~/carrinho
source venv/bin/activate
python stream_sender.py
```

O script abre a câmera com OpenCV, captura frames em MJPEG, codifica como JPEG e serve via socket TCP na porta 8080. Aguarda conexão da VM.

## Na VM — receiver.py

O receiver conecta no IP da Raspberry via WireGuard (`10.0.0.2:8080`), lê os frames, aplica detecção de objetos e serve o resultado via Flask.

A rota `/stream` serve o MJPEG processado. O nginx faz proxy dessa rota para o navegador na porta 80.

## Configuração do nginx

Arquivo localizado em `vm/nginx/carrinho.conf`.

A rota `/stream` faz proxy para `http://127.0.0.1:5000/stream` (Flask).

## Ajustes de performance

Se o stream estiver lento, edite `stream_sender.py` na Raspberry e reduza:

```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 15)
```

E reduza a qualidade JPEG:

```python
_, jpg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
```

## Checklist

- [ ] Webcam reconhecida em `/dev/video0`
- [ ] `stream_sender.py` rodando na Raspberry sem erro
- [ ] `receiver.py` conectando em `10.0.0.2:8080`
- [ ] Stream visível em `http://IP_PUBLICO`
