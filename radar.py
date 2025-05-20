import RPi.GPIO as GPIO
import pygame
import time
from stepper import StepperMotor
from ultrasonicsensor import ultrasonicRead

# Configuración PyGame
pygame.init()
screen = pygame.display.set_mode((1400, 800))
font = pygame.font.SysFont('Arial', 20)

# Configuración GPIO y hardware
stepper = StepperMotor()
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        for angle in range(0, 181, 5):  # Escaneo de 0° a 180°
            distance = ultrasonicRead(TRIG, ECHO)
            stepper.move_to_angle(angle)
            
            # Dibujar en pantalla (simplificado)
            screen.fill((0, 0, 0))
            text = font.render(f"Ángulo: {angle}° - Distancia: {distance} cm", True, (255, 255, 255))
            screen.blit(text, (50, 50))
            pygame.display.flip()
            
            time.sleep(0.05)
            
except KeyboardInterrupt:
    stepper.cleanup()
    GPIO.cleanup()
    pygame.quit()