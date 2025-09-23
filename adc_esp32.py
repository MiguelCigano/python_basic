import serial
import matplotlib.pyplot as plt
import time

arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

valores = []
tiempos = []
start_time = time.time()

plt.ion()
fig, ax = plt.subplots()

while True:
    try:
        data = arduino.readline().decode().strip()
        print("Recibido: ", data)
        if data:
            try:
                valor = float(data)
                elapsed = time.time() - start_time

                valores.append(valor)
                tiempos.append(elapsed)

                ax.clear()
                ax.plot(tiempos, valores, label="Valor ADC")
                ax.set_xlabel("Tiempo (s)")
                ax.set_ylabel("ADC (0-4095)")
                ax.set_title("Lectura")
                ax.legend()

                plt.pause(0.05)
                
            except ValueError:
                pass
    except KeyboardInterrupt:
        print("Saliendo...")
        break
