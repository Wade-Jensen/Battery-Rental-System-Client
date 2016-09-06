#Import lib files
from libRFID import *
import Adafruit_PN532 as PN532
import time

import sys
#add SQL Lib topath
sys.path.insert(0, '/home/pi/M2M/Server')
from libSQL import *
#add Button Lib topath
sys.path.insert(0, '/home/pi/M2M/Hardware/Buttons')
from libButtons import *

#Program begins
#Configure the Reader
pn532 = initialise_RFID(18, 25, 23, 24)
#Configure Buttons
setupButtons()

while True:

    #Read Current Value
    cardID = read(pn532)

    data = queryCardID(cardID)

    fname = data[0]
    sname = data[1]
    credit = data[2]
    bottles = data[3]

    #Print Current Value
    print "Hello %s %s" % (fname, sname)
    print "You have $%s in credit" % (credit)
    print "And you have %s bottles rented" % (bottles)


    print "Press RED to rent a bottle or Black to return a bottle"

    button = userInput()

    if (button == 'red'):
        print "Dispensing Bottle"     

    if (button == 'black'):
        print "Place bottle on platform then press red button, press back button to cancel"
        button1 = userInput()
        
        if (button1 == 'red'):
            print "Motor now moves (returns bottle)"

    print "End"

