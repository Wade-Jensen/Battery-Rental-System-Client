#GPIO Test
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(16,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
print('Turn On')
GPIO.output(16,GPIO.HIGH)
GPIO.output(20,GPIO.HIGH)
GPIO.output(21,GPIO.HIGH)

time.sleep(3)
print('Turn off')
GPIO.output(16,GPIO.LOW)
GPIO.output(20,GPIO.LOW)
GPIO.output(21,GPIO.LOW)
