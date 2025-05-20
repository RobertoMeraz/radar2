import RPi.GPIO as GPIO
import time

class StepperMotor:
    def __init__(self, step_pin=17, dir_pin=27, enable_pin=22, steps_per_rev=200):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.enable_pin = enable_pin
        self.steps_per_rev = steps_per_rev
        self.current_angle = 0
        self.steps_per_degree = steps_per_rev / 360.0
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, GPIO.LOW)  # Activar motor
        
    def move_to_angle(self, angle):
        angle = max(0, min(180, angle))  # Limitar ángulo a 0-180°
        angle_diff = angle - self.current_angle
        steps = int(angle_diff * self.steps_per_degree)
        
        GPIO.output(self.dir_pin, GPIO.HIGH if steps > 0 else GPIO.LOW)
        steps = abs(steps)
        
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(0.001)
        
        self.current_angle = angle
    
    def cleanup(self):
        GPIO.output(self.enable_pin, GPIO.HIGH)  # Desactivar motor
        GPIO.cleanup()