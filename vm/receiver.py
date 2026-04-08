import os
os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

import cv2
from flask import Flask, Response
from flask_socketio import SocketIO, emit
from ultralytics import YOLO
from gesture_recognition import processar_gestos

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

RASPBERRY_IP = "10.0.0.2"
RASPBERRY_PORTA = 8080

modelo = YOLO("yolov8n.pt")

CORES = {
    "pessoa":   (0, 255, 0),
    "celular":  (255, 165, 0),
    "garrafa":  (0, 165, 255),
    "cadeira":  (255, 0, 255),
    "notebook": (255, 255, 0),
    "objeto":   (200, 200, 200),
}

ultimo_gesto = None

def detectar(frame):
    pessoa_detectada = False
    resultados = modelo(frame, verbose=False, conf=0.5)[0]
    for box in resultados.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = modelo.names[cls_id]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cor = CORES.get(label, CORES["objeto"])
        cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)
        cv2.putText(frame, f"{label} {conf:.0%}", (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, cor, 2)
        if label == "pessoa":
            pessoa_detectada = True
    return frame, pessoa_detectada

def conectar_camera():
    return cv2.VideoCapture(f"http://{RASPBERRY_IP}:{RASPBERRY_PORTA}")

def gerar_frames():
    global ultimo_gesto
    cap = conectar_camera()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Reconectando...")
            cap.release()
            cap = conectar_camera()
            continue

        # Detecção de objetos
        frame, pessoa_detectada = detectar(frame)

        # Reconhecimento de gestos
        frame, gesto = processar_gestos(frame)

        # Emite eventos via SocketIO
        if gesto and gesto != ultimo_gesto:
            ultimo_gesto = gesto
            socketio.emit('gesto', {'comando': gesto})
            print(f"Gesto detectado: {gesto}")

        if pessoa_detectada:
            socketio.emit('alerta', {'tipo': 'pessoa_detectada'})

        _, jpg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            jpg.tobytes() +
            b"\r\n"
        )

@app.route("/stream")
def stream():
    return Response(gerar_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/")
def index():
    return open("/var/www/carrinho/index.html").read()

@socketio.on('gps_data')
def receber_gps(data):
    emit('gps', data, broadcast=True)

if __name__ == "__main__":
    print(f"Conectando a Raspberry em {RASPBERRY_IP}:{RASPBERRY_PORTA}...")
    print("Deteccao de objetos + reconhecimento de gestos ativos.")
    print("Acesse http://IP_PUBLICO no navegador.")
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
