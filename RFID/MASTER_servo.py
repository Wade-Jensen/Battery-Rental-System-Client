#Import lib files
from __future__ import division
from libRFID import *
import Adafruit_PN532 as PN532
import Adafruit_PCA9685
import time
import sys
import os


#add SQL Lib topath
sys.path.insert(0, '/home/pi/M2M/Server')
from libSQL import *
#add Button Lib topath
sys.path.insert(0, '/home/pi/M2M/Hardware/Buttons')
from libButtons import *

#Program begins
#Setup I2C connection to servo motor
pwm = Adafruit_PCA9685.PCA9685()
#Set Servo Frequency
pwm.set_pwm_freq(50)
#Set Default Servo State (Stationary)
pwm.set_pwm(15, 0, 0)

#Configure the RFID Card Reader
pn532 = initialise_RFID(18, 25, 23, 24)
#Configure Buttons and LEDs
setupButtons()

#Clear the Screen
os.system('clear')

#Begin main program
while True:

    #Set all LEDs to be turned  off
    LED('NONE')

    print "Scan your card to get started!"

    #Wait for user to swipe card and read the CARD ID
    cardID = read(pn532)

    #Query the database using custom built Library
    data = queryCardID(cardID)

    #Indicate to user that card has been read correctly
    LED('GREEN')

    #Collect all variables
    fname = data[0]
    sname = data[1]
    credit = data[2]
    bottles = data[3]

    #Check if the user has enough credit and has not taken out too many bottles
    if (bottles <= 2)and(credit > 2):
    
        #Check the users account to ensure they have enough bottles and credit
        print "Hello %s %s" % (fname, sname)
        print "You have $%s in credit" % (credit)
        print "And you have %s bottles rented" % (bottles)
        

        print "\nPress RED to rent a bottle or \nBLACK to return a bottle"
        button = userInput()

        if (button == 'red'):
            print "Dispensing Bottle"
            #Remove Credit and add one bottle to the users account

            credit = credit - 2
            bottles = bottles + 1

            #Update the server
            updateData(cardID, credit, bottles)
            
            #Move motor one 'door' anti-clockwise
            pwm.set_pwm(15, 0, 327)
            time.sleep(1.5)
            pwm.set_pwm(15, 0, 0)
            time.sleep(0.1)

            #Flash the RED LED
            FLASH('RED')

        if (button == 'black'):
            print "Returning Bottle"
            
            #Return Credit and subtract one bottle to the users account
            credit = credit + 2
            bottles = bottles - 1

            #Update the server
            updateData(cardID, credit, bottles)

            #Move motor one 'door' clockwise
            pwm.set_pwm(15, 0, 312)
            time.sleep(1.15)
            pwm.set_pwm(15, 0, 0)
            time.sleep(0.1)


    elif (bottles > 2)and(credit <= 2):
        #Check the users account to ensure they have enough bottles and credit
        print "Hello %s %s" % (fname, sname)
        print "You only have $%s in credit, please top up to get Refreshed" % (credit)
        print "And you have %s bottles rented, please return a bottle to get another" % (bottles)

        print "\nPress BLACK to return a bottle"
        button = userInput()

        if (button == 'black'):
            print "Returning Bottle"
            
            #Return Credit and subtract one bottle to the users account
            credit = credit + 2
            bottles = bottles - 1

            #Update the server
            updateData(cardID, credit, bottles)

            #Move motor one 'door' clockwise
            pwm.set_pwm(15, 0, 312)
            time.sleep(1.15)
            pwm.set_pwm(15, 0, 0)
            time.sleep(0.1)

    elif (credit <= 2):
        #Check the users account to ensure they have enough bottles and credit
        print "Hello %s %s" % (fname, sname)
        print "You only have $%s in credit, please top up to get Refreshed" % (credit)
        print "And you have %s bottles rented" % (bottles)

    elif (bottles > 2):
         #Check the users account to ensure they have enough bottles and credit
        print "Hello %s %s" % (fname, sname)
        print "You have $%s in credit" % (credit)
        print "And you have %s bottles rented, please return a bottle to get another" % (bottles)

        print "\nPress BLACK to return a bottle"
        button = userInput()

        if (button == 'black'):
            print "Returning Bottle"
            
            #Return Credit and subtract one bottle to the users account
            credit = credit + 2
            bottles = bottles - 1

            #Update the server
            updateData(cardID, credit, bottles)

            #Move motor one 'door' clockwise
            pwm.set_pwm(15, 0, 312)
            time.sleep(1.15)
            pwm.set_pwm(15, 0, 0)
            time.sleep(0.1)

    #Provide customer with funny, yet informative message
    print "Have a Refresh-ing Day!"
    
    #Flash the GREEN LED
    FLASH('GREEN')
            
    #Wait then Clear the screen
    time.sleep(1)
    os.system('clear')
