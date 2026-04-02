import serial
import pynmea2
import socketio
import time

PORTA = "/dev/serial0"
BAUD = 9600
VM_URL = "http://10.0.0.1:5000"

sio = socketio.Client()

def conectar():
    while True:
        try:
            sio.connect(VM_URL)
            print(f"Conectado a VM em {VM_URL}")
            break
        except Exception:
            print("Aguardando VM... tentando em 3s")
            time.sleep(3)

conectar()

ser = serial.Serial(PORTA, baudrate=BAUD, timeout=1)
print("Enviando dados GPS...\n")

while True:
    try:
        linha = ser.readline().decode('ascii', errors='replace').strip()

        if linha.startswith('$GNRMC') or linha.startswith('$GPRMC'):
            try:
                msg = pynmea2.parse(linha)
                if msg.latitude and msg.longitude:
                    velocidade = round(float(msg.spd_over_grnd) * 1.852, 1) if msg.spd_over_grnd else 0
                    sio.emit('gps_data', {
                        'latitude': msg.latitude,
                        'longitude': msg.longitude,
                        'velocidade': velocidade
                    })
            except pynmea2.ParseError:
                pass

        if linha.startswith('$GNGGA') or linha.startswith('$GPGGA'):
            try:
                msg = pynmea2.parse(linha)
                if msg.latitude and msg.longitude:
                    sio.emit('gps_data', {
                        'latitude': msg.latitude,
                        'longitude': msg.longitude,
                        'satelites': int(msg.num_sats),
                        'altitude': float(msg.altitude)
                    })
            except pynmea2.ParseError:
                pass

    except KeyboardInterrupt:
        print("\nEncerrando.")
        sio.disconnect()
        ser.close()
        break
