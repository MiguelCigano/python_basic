import cv2
import numpy as np
import serial
import time

# Configura el puerto Serial (cambia por tu puerto)
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # Espera que Arduino se inicialice

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se puede abrir la cámara")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a espacio HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rango de rojo (ajusta si es necesario)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Máscara
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Ver si hay rojo suficiente
    if cv2.countNonZero(mask) > 500:  # ajusta el número según tu cámara
        arduino.write(b'1')  # Enciende LED
    else:
        arduino.write(b'0')  # Apaga LED

    cv2.imshow("Camara", frame)
    cv2.imshow("Rojo detectado", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
