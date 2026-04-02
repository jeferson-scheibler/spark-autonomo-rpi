import cv2
import socket

PORTA = 8080
DEVICE = 0

cap = cv2.VideoCapture(DEVICE, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 15)

if not cap.isOpened():
    print("Erro: nao foi possivel abrir a camera.")
    exit(1)

print(f"Camera aberta. Aguardando conexao na porta {PORTA}...")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', PORTA))
server.listen(1)

while True:
    conn, addr = server.accept()
    print(f"Conexao recebida de {addr}")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, jpg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            data = jpg.tobytes()
            header = (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n" +
                f"Content-Length: {len(data)}\r\n\r\n".encode()
            )
            try:
                conn.sendall(header + data + b"\r\n")
            except (BrokenPipeError, ConnectionResetError):
                print("Cliente desconectado.")
                break
    finally:
        conn.close()
