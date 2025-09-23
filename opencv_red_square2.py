import cv2
import numpy as np
import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(3) # Wait to arduino

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera NOT OPEN!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red range
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Yellow range
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)


    # Encontrar contornos rojos
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar contornos amarillos
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    red_detected = False
    yellow_detected = False

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 9000:  # solo regiones grandes
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (250, 2, 2), 5)  # rectángulo rojo
            red_detected = True
    
    for cnt in contours_yellow:
        area = cv2.contourArea(cnt)
        if area > 9000:  # solo regiones grandes
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 100), 5)  # rectángulo 
            yellow_detected = True

    if red_detected:
        arduino.write(b'1')
    else:
        arduino.write(b'0')

    if yellow_detected:
        arduino.write(b'2')
    else:
        arduino.write(b'3')

    cv2.imshow("Camara", frame)
    cv2.imshow("Rojo detectado", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()