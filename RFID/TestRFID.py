from libRFID import *
import Adafruit_PN532 as PN532
while True :
#Configure the Reader
    pn532 = initialise_RFID(18, 25, 23, 24)

    #Read Current Value
    r = read(pn532)

    #Print Current Value
    print "Card ID %s" % r
