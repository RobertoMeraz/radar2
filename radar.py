import RPi.GPIO as GPIO
import pygame
import math
import time
import colors
import sys
from target import *
from display import draw
from ultrasonicsensor import ultrasonicRead
from stepper import StepperMotor

print('Radar Start')

# Configuración PyGame
pygame.init()
pygame.font.init()
defaultFont = pygame.font.get_default_font()
fontRenderer = pygame.font.Font(defaultFont, 20)
radarDisplay = pygame.display.set_mode((1400, 800))
pygame.display.set_caption('Radar Screen')

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Inicializar motor paso a paso
stepper = StepperMotor()

# Configuración sensor HC-SR04
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Lista de objetivos
targets = {}

try:
    while True:
        # Rotar de 0 a 180 grados
        for angle in range(0, 181):
            distance = ultrasonicRead(GPIO, TRIG, ECHO)
            
            if distance != -1 and distance <= 50:
                targets[angle] = Target(angle, distance)
                
            draw(radarDisplay, targets, angle, distance, fontRenderer)
            stepper.move_to_angle(angle)
            time.sleep(0.01)
            
        # Rotar de 180 a 0 grados
        for angle in range(180, -1, -1):
            distance = ultrasonicRead(GPIO, TRIG, ECHO)
            
            if distance != -1 and distance <= 50:
                targets[angle] = Target(angle, distance)
                
            draw(radarDisplay, targets, angle, distance, fontRenderer)
            stepper.move_to_angle(angle)
            time.sleep(0.01)
            
        # Detectar si se cierra la ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
                
except KeyboardInterrupt:
    print('Radar Exit')
    stepper.cleanup()
    GPIO.cleanup()
    
except Exception as e:
    print(e)
    print('Radar Exit')
    stepper.cleanup()
    GPIO.cleanup()
    
pygame.quit()
sys.exit()