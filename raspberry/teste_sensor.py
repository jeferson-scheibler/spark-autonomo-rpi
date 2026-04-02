import RPi.GPIO as GPIO
import time

# RCWL-0516 - sensor de presenca por micro-ondas
SENSOR_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

print("Testando RCWL-0516... Ctrl+C para parar.\n")

try:
    estado_anterior = 0
    while True:
        estado = GPIO.input(SENSOR_PIN)
        if estado != estado_anterior:
            if estado == 1:
                print("Presenca detectada!")
            else:
                print("Sem presenca.")
            estado_anterior = estado
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nEncerrando.")
    GPIO.cleanup()
