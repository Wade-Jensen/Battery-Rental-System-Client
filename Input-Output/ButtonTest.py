#GPIO Test
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(27,GPIO.IN)
GPIO.setup(17,GPIO.IN)

while True:
    print "Red Button Value: %s" % GPIO.input(27)
    print "Green Button Value: %s " % GPIO.input(17)
    print " "
    
    time.sleep(2)
