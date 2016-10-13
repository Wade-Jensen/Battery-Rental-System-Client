#GPIO Test
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(21,GPIO.OUT)
print('Turn On')
GPIO.output(21,GPIO.HIGH)
