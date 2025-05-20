import time

def ultrasonicRead(GPIO, TRIG, ECHO):
    # Estabilización del sensor
    GPIO.output(TRIG, False)
    time.sleep(0.01)
    
    # Enviar pulso
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10µs
    GPIO.output(TRIG, False)
    
    start_time = time.time()
    timeout = start_time + 0.04  # Timeout de 40ms
    
    # Esperar eco (tiempo de inicio)
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        start_time = time.time()
    
    # Esperar fin de eco
    end_time = time.time()
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        end_time = time.time()
    
    # Calcular distancia
    if time.time() >= timeout:
        return -1  # Timeout
    
    duration = end_time - start_time
    distance = (34300 * duration) / 2
    
    return round(distance, 2) if distance <= 50 else -1