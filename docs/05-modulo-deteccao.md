# 05 — Módulo de Detecção de Objetos

Detecção de objetos em tempo real sobre o stream de vídeo usando YOLOv8. Roda inteiramente na VM para não sobrecarregar a Raspberry Pi Zero 2 W.

## Arquitetura

```
Frame recebido da Raspberry
  └── YOLOv8n (inferência na VM)
        └── Bounding boxes desenhados no frame
              └── Frame processado servido via /stream
```

## Modelo utilizado

**YOLOv8n** (nano) — versão mais leve do YOLOv8, ideal para inferência em tempo real em hardware sem GPU dedicada.

- Tamanho do modelo: ~6MB
- Download automático no primeiro uso
- Threshold de confiança: 50% (configurável)

## Instalação na VM

```bash
cd ~/carrinho
source venv/bin/activate
pip install ultralytics
```

Baixe o modelo antecipadamente:

```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

## Classes detectadas

O modelo detecta 80 classes do dataset COCO. As principais para o projeto:

| ID | Classe |
|---|---|
| 0 | pessoa |
| 67 | celular |
| 39 | garrafa |
| 56 | cadeira |
| 63 | notebook |

Todas as outras classes são detectadas com o nome original em inglês.

## Cores dos bounding boxes

| Classe | Cor (BGR) |
|---|---|
| pessoa | verde (0, 255, 0) |
| celular | laranja (255, 165, 0) |
| garrafa | azul claro (0, 165, 255) |
| cadeira | magenta (255, 0, 255) |
| notebook | amarelo (255, 255, 0) |
| outros | cinza (200, 200, 200) |

## Ajustar o threshold de confiança

No `receiver.py`, altere o parâmetro `conf`:

```python
resultados = modelo(frame, verbose=False, conf=0.5)[0]
```

Valores menores detectam mais objetos mas com mais falsos positivos. Recomendado entre `0.4` e `0.6`.

## Performance esperada

Em VM com 2 vCPUs e 2GB RAM, o YOLOv8n processa aproximadamente 5 a 10 FPS sobre frames de 320x240. Para melhorar:

- Reduza a resolução do stream na Raspberry
- Aumente os recursos da VM
- Use GPU na VM (requer configuração adicional do CUDA)

## Checklist

- [ ] `ultralytics` instalado na VM
- [ ] Modelo `yolov8n.pt` baixado
- [ ] Detecções aparecendo no stream com bounding boxes
- [ ] Labels e porcentagem de confiança visíveis
