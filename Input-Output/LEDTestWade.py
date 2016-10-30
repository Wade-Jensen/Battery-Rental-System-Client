#GPIO Test
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
print('Turn On and Off')

GPIO.setup(16,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

print('Battery 1')
GPIO.output(16,GPIO.HIGH)
time.sleep(0.5)
GPIO.output(16,GPIO.LOW)

print('Battery 2')
GPIO.output(20,GPIO.HIGH)
time.sleep(0.5)
GPIO.output(20,GPIO.LOW)

print('Battery 3')
GPIO.output(21,GPIO.HIGH)
time.sleep(0.5)
GPIO.output(21,GPIO.LOW)

time.sleep(3)




