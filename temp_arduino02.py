import serial
import matplotlib.pyplot as plt
import time

arduino = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(2)

temperaturas = []
tiempos = []
start_time = time.time()

plt.ion()
fig, ax = plt.subplots()

while True:
    try:
        data = arduino.readline().decode().strip()
        if data:
            try:
                tempC = float(data)  # ahora cada línea es solo el valor de temp
                elapsed = time.time() - start_time

                temperaturas.append(tempC)
                tiempos.append(elapsed)

                ax.clear()
                ax.plot(tiempos, temperaturas, label="Temperatura (°C)")
                ax.set_xlabel("Tiempo (s)")
                ax.set_ylabel("°C")
                ax.set_title("Temperatura en tiempo real - LM35")
                ax.legend()

                plt.pause(0.1)
            except ValueError:
                # ignorar líneas que no sean números
                pass
    except KeyboardInterrupt:
        print("Saliendo...")
        break
