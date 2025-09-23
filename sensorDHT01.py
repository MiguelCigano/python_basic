import serial
import matplotlib.pyplot as plt
import time
import re

# Intentar diferentes puertos comunes
puertos = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyUSB0', '/dev/ttyUSB1']
arduino = None

for puerto in puertos:
    try:
        arduino = serial.Serial(puerto, 9600, timeout=1)
        print(f"Conectado a {puerto}")
        break
    except:
        print(f"No se pudo conectar a {puerto}")
        continue

if arduino is None:
    print("No se pudo conectar a ningún puerto")
    exit()

time.sleep(2)

# Limpiar buffer serial
arduino.flushInput()

valores = []
tiempos = []
start_time = time.time()

plt.ion()
fig, ax = plt.subplots(figsize=(10, 6))

try:
    while True:
        try:
            if arduino.in_waiting > 0:
                data = arduino.readline().decode().strip()
                # print(f"Raw data: '{data}'")  # Debug completo
                
                if data:
                    try:
                        # Intentar convertir directamente
                        valor = float(data)
                        # print(f"Valor convertido: {valor}")
                        
                    except ValueError:
                        # Si falla, extraer número del texto
                        print("Intentando extraer número...")
                        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", data)
                        if numbers:
                            valor = float(numbers[0])
                            print(f"Valor extraído: {valor}")
                        else:
                            print("No se encontraron números")
                            continue
                    
                    elapsed = time.time() - start_time
                    valores.append(valor)
                    tiempos.append(elapsed)

                    # Mantener sólo los últimos 100 puntos
                    if len(valores) > 100:
                        valores.pop(0)
                        tiempos.pop(0)

                    ax.clear()
                    ax.plot(tiempos, valores, 'r-', linewidth=2)
                    ax.set_xlabel("Tiempo (s)", fontsize=12)
                    ax.set_ylabel("Temperatura (°C)", fontsize=12)
                    ax.set_title("Temperatura en Tiempo Real", fontsize=14)
                    ax.grid(True)
                    
                    # Ajustar escalas dinámicamente
                    if len(valores) > 1:
                        ax.set_ylim(min(valores)-1, max(valores)+1)
                    
                    plt.tight_layout()
                    plt.pause(0.01)
                        
        except serial.SerialException as e:
            print(f"Error serial: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

except KeyboardInterrupt:
    print("Saliendo...")
finally:
    if arduino:
        arduino.close()
    plt.ioff()
    plt.show()