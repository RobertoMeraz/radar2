import time
import RPi.GPIO as GPIO

def ultrasonicRead(TRIG=23, ECHO=24):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    GPIO.output(TRIG, False)
    time.sleep(0.01)
    
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    timeout = time.time() + 0.04  # Timeout de 40ms
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()
    
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()
    
    if time.time() >= timeout:
        return -1  # Timeout
    
    pulse_duration = pulse_end - pulse_start
    distance = round((pulse_duration * 17150), 2)  # cm
    return distance if distance <= 50 else -1  # Límite de 50cm