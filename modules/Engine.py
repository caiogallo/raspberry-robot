import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Engine():    
    MAX_SPEED = 1
    MIN_SPEED = 0
    
    def __init__(self,pwmPin,pin1,pin2):
        
        self.pwmPin = pwmPin
        self.pin1 = pin1
        self.pin2 = pin2
        
        GPIO.setup(self.pwmPin,GPIO.OUT)
        GPIO.setup(self.pin1,GPIO.OUT)
        GPIO.setup(self.pin2,GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.pwmPin, 100);
        self.pwm.start(0);
        
    def move(self, speed = 0.5):
        if speed > self.MAX_SPEED:
            speed = self.MAX_SPEED
        elif speed < self.MIN_SPEED:
            speed = self.MIN_SPEED
            
        speed *= 100
        
        self.pwm.ChangeDutyCycle(speed)
        
        GPIO.output(self.pin1,GPIO.HIGH)
        GPIO.output(self.pin2,GPIO.LOW)
                
        
    def stop(self):
        self.pwm.ChangeDutyCycle(0)