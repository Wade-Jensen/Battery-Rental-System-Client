#This is a test program for reading a RFID card, detecting battery ID, machine ID and sending this data to a server for ENB345
#Written for Python 2, August-October 2016
#DEVELOPMENT BUILD 1.0
# Author: Gerard Rallos

#Import Libraries:
from libRFID import *                   #RFID Library
import Adafruit_PN532 as PN532          #RFID Breakout
from Subfact_ina219 import INA219       #Current Sensor Breakout
import time                             #Time library - sleep function
import datetime                         #Datetime library - for return/charge times
import urllib2                          #URL Library for python 2
import json                             #JSON library
import threading                        #Threading for server heartbeat
from collections import namedtuple      #For decoding JSON objects into dictionaries
from collections import deque           #For backlog data storage
from random import randint				#Heartbeat random number
import RPi.GPIO as GPIO                 #GPIO Pins

#Initialize Current Sensors with correct addresses - Each battery has an associated sensor
inaOne = INA219(0x40)       #Base, 0x40
inaTwo = INA219(0x40)       #A0 Bridge 0x41
inaThree = INA219(0x40)     #A1 Bridge 0x44

timeoutTimer = 30

serverIP = 'http://52.63.34.239:9000'

#Initialize the Reader
pn532 = initialise_RFID(18, 25, 23, 24)     #Configure PN532 to the correct I/O pins on the breakout board (i.e. IO18,IO25 etc.)

#Define Functions:
def serverPing ( urlString ):       #Accepts a string
    try:
        request = urllib2.urlopen(urlString, timeout = timeoutTimer)   #Ping server

    except urllib2.HTTPError, e:        #Catch HTTP Error
        print 'Failed - Error Code: %s' %e.code
        contact = 0
        
    except urllib2.URLError as e:       #URL Error Catch
        print type(e)    
        print 'Error in URL Address'            
        contact = 0
        
    else :
        contact = 1                     #If no error is caught, server can be contacted
    
    return contact

def serverHeartbeat () :
    threading.Timer(30.0, serverHeartbeat).start()
    serverContact = serverPing(serverIP + '/api/alive')
    print 'Heartbeat'

    #Get Battery Current Draw:
    #Send battery current draw for connected batteries
    if (~batOneAlloc):
        batteryOneCurrentHeart = inaOne.getCurrent_mA()
    else :
        batteryOneCurrentHeart = 0
    
    if (~batTwoAlloc):
        batteryTwoCurrentHeart = inaTwo.getCurrent_mA()
    else :
        batteryTwoCurrentHeart = 0
    
    if (~batThreeAlloc) :
        batteryThreeCurrentHeart = inaThree.getCurrent_mA() 
    else :
        batteryThreeCurrentHeart = 0
    
    heartTime = int(time.time())
    numRand = randint(0, 100)
    
    heartbeatURL = serverIP + "/api/requestbattery/machineId/%s/time/%s/rngId/%s/chargeCurrent0/%s/chargeCurrent1/%s/chargeCurrent2/%s/chargeCurrent3/%s" % (machineID, heartTime, numRand, batteryOneCurrentHeart, batteryTwoCurrentHeart, batteryThreeCurrentHeart, 0)
    
    if(serverContact) :
        #Send backlog data to server if any exists
        numBacklog = len(backlogData)
        if(len(backlogData)) :
            for x in range(0,numBacklog) :
                request = urllib2.urlopen(backlogData.pop(), timeout = timeoutTimer)   #Send backlog data
                
        #Send current heartbeat data 
        heartRequest = urllib2.urlopen(heartbeatURL, timeout = timeoutTimer)    #Send heartbeat data
        
    else :  
        #Append heartbeat to backlog
        backlogData.append(heartbeatURL)
        
        
        
#Initial Setup
#Machine Specific Configuration
numSlots = 3
machineLocation = 'QUT%20KG'

setup = 1
while setup:
    serverConnection = serverPing (serverIP + '/api/alive')        #Check if server can be contacted
    if (serverConnection) :
    
        setupURL = serverIP + "/api/startmachine/numSlots/%s/textlocation/%s" % (numSlots,machineLocation)
        initialRequest = urllib2.urlopen(setupURL, timeout = timeoutTimer)
        initialRes = initialRequest.read()
        
        initialConfig = json.loads(initialRes,object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        
        machineID = initialConfig.id                 #Machine ID
        numBatteries = initialConfig.numBatteries    #Number of batteries in machine
        print initialConfig
        print initialConfig.id, 
        print initialConfig.numBatteries
    
        setup = 0
        print 'Setup Complete'  
    else :
        print  'Failed to Contact Server, trying again in 5 seconds'
        time.sleep(5)
    
#Initial variable declaration
batRent = 0
batReturn = 0

batteryOneCurrent = 0
batteryTwoCurrent = 0
batteryThreeCurrent = 0

#TESTING - SET BATTERY 1 TO 1 FOR NOW
batteryOneCharged = 0
batteryTwoCharged = 0
batteryThreeCharged = 0

#TESTING - SET ALLOC ONE TO 1 TO 1 FOR NOW
batOneAlloc = 1
batTwoAlloc = 0
batThreeAlloc = 0

SLOT_ONE_LED = 16       #Battery One LED Output
SLOT_TWO_LED = 20       #Battery Two LED Output
SLOT_THREE_LED = 21     #Battery Three LED Output

RENTAL_BUTTON = 17      #Rental Switch Input
RETURN_BUTTON = 27      #Return Switch Input

#Initialize IO Pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SLOT_ONE_LED,GPIO.OUT)
GPIO.setup(SLOT_TWO_LED,GPIO.OUT)
GPIO.setup(SLOT_THREE_LED,GPIO.OUT)
GPIO.setup(RENTAL_BUTTON,GPIO.IN)
GPIO.setup(RETURN_BUTTON,GPIO.IN)

#Initialize empty backlog deque
backlogData = deque()

#Initialize server heartbeat thread
serverHeartbeat()

#Main Loop
while True:
    cardScan = 0        #Card is not currently scanned
    
    #Turn off all LED's for battery slots
    GPIO.output(SLOT_ONE_LED,GPIO.LOW)  
    GPIO.output(SLOT_TWO_LED,GPIO.LOW)  
    GPIO.output(SLOT_THREE_LED,GPIO.LOW)    
    
    print "Please scan your ID card"
	
    #Wait until a card is scanned
    while (cardScan != 1):
        #Current Sensing:
            #Check all battery current draws
            batteryOneCurrent = inaOne.getCurrent_mA()
            batteryTwoCurrent = inaTwo.getCurrent_mA()
            batteryThreeCurrent = inaThree.getCurrent_mA()
            
            #Check if battery has finished charging and it was previously rented (below 5mA is assumed to be charged, provided there is a battery currently connected)
            if(batteryOneCurrent < 5 & batOneAlloc == 0) :  #ALSO SEND A MESSAGE FOR WHEN THE BATTERY IS FULLY CHARGES
                batteryOneCharged = 1
                serverConnection = serverPing (serverIP + '/api/alive')        #Check if server can be contacted
                fullTime = int(time.time())
                chargeString = serverIP + "/api/fullcharge/machineId/%s/time/%s/machineSlot/%s" % (machineID, fullTime, 1)
                if(serverConnection) :
                    fullCharge = urllib2.urlopen(returnURL)
                else :
                    backlogData.append(chargeString)
                
            if(batteryTwoCurrent < 5 & batTwoAlloc == 0) :
                batteryTwoCharged = 1
                serverConnection = serverPing (serverIP + '/api/alive')        #Check if server can be contacted
                fullTime = int(time.time())
                chargeString = serverIP + "/api/fullcharge/machineId/%s/time/%s/machineSlot/%s" % (machineID, fullTime, 2)
                if(serverConnection) :
                    fullCharge = urllib2.urlopen(returnURL)
                else :
                    backlogData.append(chargeString)                
            if(batteryThreeCurrent < 5 & batThreeAlloc == 0) :
                batteryThreeCharged = 1
                serverConnection = serverPing (serverIP + '/api/alive')        #Check if server can be contacted
                fullTime = int(time.time())
                chargeString = serverIP + "/api/fullcharge/machineId/%s/time/%s/machineSlot/%s" % (machineID, fullTime, 3)
                if(serverConnection):
                    fullCharge = urllib2.urlopen(returnURL)
                else :
                    backlogData.append(chargeString)                
    
        #Card Scanning:
            cardID = pn532.read_passive_target()    #Check if card is scanned
                # Authenticate block 1 for reading with default key (0xFFFFFFFFFFFF).
            if cardID is None:              
                time.sleep(1)       #Pause for 1 second before next loop execution (reduce busy loading)
                continue				
				
            if not pn532.mifare_classic_authenticate_block(cardID, 1, PN532.MIFARE_CMD_AUTH_B,
                                                           [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
                print('Failed to authenticate card')
                continue
				
            cardScan = 1
            print "Card ID %s" % cardID         #Print Card ID 
            print "Please leave card on scanner until rental/return process is finished"
    
    #Rental/Return Process
    #Check if user intends to rent or return
    print "Please press 'Rent' or 'Return' for your desired service"
    buttonPress = 1
    batRent = 0
    batReturn = 0
        
    while buttonPress:
        if(GPIO.input(RENTAL_BUTTON)) :
            batRent = 1
            buttonPress = 0
        elif(GPIO.input(RETURN_BUTTON)) :
            batReturn = 1
            buttonPress = 0
        time.sleep(0.1)
    
    buttonPress = 1
    print batRent
    print batReturn
        
    #Rentals:
    if (batRent) :
        serverConnection = serverPing (serverIP + '/api/alive')    #Check if server can be contacted
        print "This is a battery rental"
        if (serverConnection) :                                             #If I can contact server
            #Determine which battery is free            
            if (batteryOneCharged):                                         #Proceed through list of batteries
                allocatedBattery = 1            
            elif (batteryTwoCharged):
                allocatedBattery = 2        
            elif (batteryThreeCharged):
                allocatedBattery = 3    
            else :
                print "No batteries charged, please try another machine"    #If no batteries are charged
                continue            
        
            batTime = int(time.time())      #Time battery was rented
            
            #Send information to server
            rentalURL = serverIP + "/api/requestbattery/machineId/%s/machineSlot/%s/cardId/%s/time/%s" % (machineID, allocatedBattery, cardID, batTime)
            print (rentalURL)       #TESTING
            
            #Contact URL and retrieve JSON object
            rentalRequest = urllib2.urlopen(rentalURL)
            rentalRes = rentalRequest.read()

            #Convert JSON into an object with attributes corresponding to dict keys.
            rentalJson = json.loads(rentalRes,object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            print rentalJson
        
            #Check if user is permitted to rent battery
            if (rentalJson.releaseBattery) :
                #Rent battery out to user
                #Set LED to indicate which battery the user should rent
                if(allocatedBattery == 1) :
                    GPIO.output(SLOT_ONE_LED,GPIO.HIGH)
                    batOneAlloc = 1
                    batteryOneCharged = 0

                elif(allocatedBattery == 2) :
                    GPIO.output(SLOT_TWO_LED,GPIO.HIGH)
                    batTwoAlloc = 1  
                    batteryTwoCharged = 0
                    
                elif(allocatedBattery == 3) :
                    GPIO.output(SLOT_THREE_LED,GPIO.HIGH)   
                    batThreeAlloc = 1
                    batteryThreeCharged = 0
                            
                print "Your battery is indicated by the light, please remove battery and remove your card, thank you!"
            else :
                print "Insufficienct credit or user otherwise not permitted to rent battery - please remove card"
                time.sleep(5)
                continue
            
        else :                                                          #If I cannot contact server
            #Read users current credit from card
            read = 1
            while read:
                # Check if a card is available to read.
                uid = pn532.read_passive_target()
                # Try again if no card is available.
                if uid is None:
                    continue
                print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
                # Authenticate block 1 for reading with default key (0xFFFFFFFFFFFF).
                if not pn532.mifare_classic_authenticate_block(uid, 1, PN532.MIFARE_CMD_AUTH_B,
                                                               [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
                    print('Failed to authenticate card')
                    continue
                # Read block 1 data.
                data = pn532.mifare_classic_read_block(1)
                if data is None:
                    print('Failed to read card credit')
                    continue
                tempString = data[0:(data.find(b'\x00'))]           #Remove empty bits from data string
                userCredit = int(tempString)                        #Current credit on card (in cents)
                print "Current Credit: $%s" %(userCredit / 100)
                read = 0;
            
            if (userCredit > 0) :       #If user has enough credit, do battery rental process and instead of contacting server, append to backlog list
                #Determine which battery to rent out
                if (batteryOneCharged):                                         #Proceed through list of batteries
                    allocatedBattery = 1
                    batOneAlloc = 1
                    batteryOneCharged = 0
                    GPIO.output(SLOT_ONE_LED,GPIO.HIGH) 
        
                elif (batteryTwoCharged):
                    allocatedBattery = 2
                    batTwoAlloc = 1
                    batteryTwoCharged = 0
                    GPIO.output(SLOT_TWO_LED,GPIO.HIGH)     
                    
                elif (batteryThreeCharged):
                    allocatedBattery = 3
                    batThreeAlloc = 1
                    batteryThreeCharged = 0
                    GPIO.output(SLOT_THREE_LED,GPIO.HIGH)       
                    
                else :
                    print "No batteries charged, please try another machine"    #If no batteries are charged
                    continue
                
                print "Your battery is indicated by the light, please remove battery and remove your card, thank you!"
                
                #Create string to insert into deque backlog
                batTime = int(time.time())      #Time battery was rented
                rentalURL = serverIP + "/api/requestbattery/machineId/%s/machineSlot/%s/cardId/%s/time/%s" % (machineID, (allocatedBattery - 1), cardID, batTime)
                backlogData.append(rentalURL)            
                    
            else :      #Else if credit is insufficient, reject user and continue
                print "Insufficient credit, please remove card"
                time.sleep(5)
                continue
                
                
    #Returns:
    elif (batReturn) :
        print "This is a battery return - please put battery into empty slot"
        returnNot = 1
        breakCount = 0
        timeoutVar = 0

        while (returnNot) :

        #Find which battery is returned by recording surge current
            if ( batOneAlloc and (inaOne.getCurrent_mA() > 5)) :
                returnedBattery = 1
                batOneAlloc = 0
                returnNot = 0
                
            elif ( batTwoAlloc and (inaTwo.getCurrent_mA() > 5)) :
                returnedBattery = 2
                batTwoAlloc = 0
                returnNot = 0
            
            elif ( batThreeAlloc and (inaThree.getCurrent_mA() > 5)) : 
                returnedBattery = 3
                batThreeAlloc = 0
                returnNot = 0

            if (breakCount > 100) :  #A manual timeout if a battery is not returned within approx. 10 seconds
                returnNot = 0
                timeoutVar = 1
                

            time.sleep(0.1)
            breakCount = breakCount + 1

        if (timeoutVar) :       #If the return process timed out, return to the initial loop
            print "Return process timed out, please try again"
            continue
        
        batTime = int(time.time())      #Time battery was returned
        
        returnURL = serverIP + "/api/returnbattery/machineId/%s/machineSlot/%s/cardId/%s/time/%s" % (machineID, (returnedBattery - 1), cardID, batTime)      #Create the return url
        serverConnection = serverPing (serverIP + '/api/alive' )                                   #Check if server can be contacted       
        
        #If I can contact server
        if (serverConnection) :     

            #Contact URL and retrieve JSON object
            print "Contacting Server"
            returnRequest = urllib2.urlopen(returnURL)
            resReturn = returnRequest.read()

            #Convert JSON into an object with attributes corresponding to dict keys.
            returnJson = json.loads(resReturn,object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                            
            
            #Write credit to card
            credit = str(returnJson.credit)
            #Authenticate Block 1
            if not pn532.mifare_classic_authenticate_block(cardID, 1, PN532.MIFARE_CMD_AUTH_B,
                                                                                   [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
                print('Error! Failed to authenticate block 1 with the card.')
                continue

            #Data array size must by 16 bytes
            data = bytearray(16)
            dataWrite = bytes(credit)
            data[0:len(dataWrite)] = dataWrite
            print(len(data))

            # Write the card.
            if not pn532.mifare_classic_write_block(1, data):
                print('Error! Failed to write to the card.')
                continue
                
            print('Wrote card successfully!')   
            print('Exiting Write Loop 1 \n')        
        #If I cannot contact server 
        else :
            backlogData.append(returnURL)

        if (returnedBattery == 1) :     
            GPIO.output(SLOT_ONE_LED, GPIO.HIGH)
        elif (returnedBattery == 2) :
            GPIO.output(SLOT_TWO_LED, GPIO.HIGH)
        elif (returnedBattery == 3) :
            GPIO.output(SLOT_THREE_LED, GPIO.HIGH)
            
        print "Battery sucessfully returned, thank you and please remove your card!"
        
    time.sleep(5)

