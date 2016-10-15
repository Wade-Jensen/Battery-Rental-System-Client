#This is a test program for reading a RFID card, detecting battery ID, machine ID and sending this data to a server for ENB345
#Written for Python 2, August-October 2016
# Author: Gerard Rallos

#Import Libraries:
from libRFID import *					#RFID Library
import Adafruit_PN532 as PN532			#RFID Breakout
from Subfact_ina219 import INA219		#Current Sensor Breakout
import time								#Time library - sleep function
import datetime							#Datetime library - for return/charge times
import urllib2							#URL Library for python 2
import json								#JSON library
from collections import namedtuple		#For decoding JSON objects into dictionaries
import RPi.GPIO as GPIO					#GPIO Pins


#Initialize Current Sensors with correct addresses - Each battery has an associated sensor
inaOne = INA219()		#Base, 0x40
inaTwo = INA219()		#ETC....
inaThree = INA219()


#Initialize the Reader
pn532 = initialise_RFID(18, 25, 23, 24)		#Configure PN532 to the correct I/O pins on the breakout board (i.e. IO18,IO25 etc.)

#Initial Setup
setup = 1
while setup:
	#Check if server can be contacted (TRY CATCH BLOCK)
	
	
	
	
		setup = 0
		print "Setup Complete"
	
	else :

#Initial variable declaration
batRent = 0
batReturn = 0

batteryOneCurrent = 0
batteryTwoCurrent = 0
batteryThreeCurrent = 0

batteryOneCharged = 0
batteryTwoCharged = 0
batteryThreeCharged = 0

batteryOneConnected = #DEFINE THIS ABOVE IN THE INITIAL SETUP WHEN I POLL THE SERVER

SLOT_ONE_LED = 16		#Battery One LED Output
SLOT_TWO_LED = 20		#Battery Two LED Output
SLOT_THREE_LED = 21		#Battery Three LED Output

RENTAL_BUTTON = 17		#Rental Switch Input
RETURN_BUTTON = 27		#Return Switch Input

#Initialize IO Pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SLOT_ONE_LED,GPIO.OUT)
GPIO.setup(SLOT_TWO_LED,GPIO.OUT)
GPIO.setup(SLOT_THREE_LED,GPIO.OUT)
GPIO.setup(RENTAL_BUTTON,GPIO.IN)
GPIO.setup(RETURN_BUTTON,GPIO.IN)

#Main Loop
while True:
	cardScan = 0		#Card is not currently scanned
	
	#Wait until a card is scanned
	while (cardScan != 1):
		#Current Sensing:
			#Check all battery current draws
			batteryOneCurrent = inaOne.getCurrent_mA()
			batteryTwoCurrent = inaTwo.getCurrent_mA()
			batteryThreeCurrent = inaThree.getCurrent_mA()
			
			#Check if battery has finished charging and it was previously rented (below 5mA is assumed to be charged, provided there is a battery currently connected)
			if() :
				batteryOneCharged = 1
			if() :
				batteryTwoCharged = 1
			if() :
				batteryThreeCharged = 1

		#Sending data to server (every 30 seconds)
			#Check server heartbeat (if it can be reached)
			
				#Send backlog data to server if any exists
				
				#Send battery current draw
				
				#Send if battery is fully charged or not? (maybe don't need to, will see)
				
		#Card Scanning:
		cardID = 							#Check if card is scanned - Read Current Value (DONT USE READ SINCE IT WAITS UNTIL A CARD IS SCANNED)
		
		if() :				#If a card is scanned
			cardScan = 1
			print "Card ID %s" % cardID			#Print Card ID (TESTING)
			print "Please leave card on scanner until rental/return process is finished"
		else :
			time.sleep(1)		#Pause for 1 second before next loop execution (reduce busy loading)
	
	#Rental/Return Process
		#Check if user intends to rent or return
		print "Please press 'Rent' or 'Return' for your desired service"
		buttonPress = 1
		batRent = 0
		batReturn = 0
		
		while buttonPress:
			if(GPIO.input(RENTAL_BUTTON))
				batRent = 1
				buttonPress = 0
			elif(GPIO.input(RETURN_BUTTON))
				batReturn = 1
				buttonPress = 0
			time.sleep(0.1)
	
		buttonPress = 1
		#Try and catch block for server contact
	
	#Rentals:
	if(batRent) :
		print "This is a battery rental"
		#If I can contact server (TRY CATCH BLOCK)
		if ():		#CHANGE IF TO A TRY AND CATCH BLOCK
			#Determine which battery is free			
			if (batteryOneCharged):											#Proceed through list of batteries
				allocatedBattery = 1
				batOneAlloc = 1
				
			elif (batteryTwoCharged):
				allocatedBattery = 2
				batTwoAlloc = 1
			
			elif (batteryThreeCharged):
				allocatedBattery = 3
				batThreeAlloc = 1
			
			else :
				print "No batteries charged, please try another machine"	#If no batteries are charged
				continue			
		
			batTime = int(time.time())		#Time battery was rented
			
			#Send information to server
			rentalURL = "http://SOMETHING" %(MACHINE ID, RENTED BATTERY, TIMESTAMP, (NOT IN ORDER))
			print (rentalURL)		#TESTING
			
			#Contact URL and retrieve JSON object
			req = urllib2.urlopen(rentalURL)
			res = req.read()
			print "JSON OBJECT"		#TESTING
			print (res)

			#Convert JSON into an object with attributes corresponding to dict keys.
			x = json.loads(res,object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
			print x.SOMETHING		
		
			#Check if user is permitted to rent battery
			if ():
			
			else :
				print "Insufficienct credit or user otherwise not permitted to rent battery - please remove card"
				continue
			
			#Rent battery out to user
				#SET LED INDICATING BATTERY, TELL USER TO REMOVE CARD AND BATTERY, UPDATE WHICH BATTERY IS REMOVED AND TIMESTAMP IT
			
		#If I cannot contact server
		else :
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
				# Note that 16 bytes are returned, so only show the first 1 bytes for the block.
				tempString = data[0:(data.find(b'\x00'))]
				userCredit = int(tempString)						#Current credit on card (in cents)
				print "Current Credit: $%s" %(userCredit / 100)
				read = 0;
			
			if (userCredit > 0):		#If user has enough credit, do battery rental process and instead of contacting server, append to backlog list
			
			else :		#Else if credit is insufficient, reject user and continue
				print "Insufficient credit, please remove card"
				time.sleep(5)
				continue
				
				
	#Returns:
	elif(batReturn) :
		print "This is a battery return"
		
		#ACTUALLY IN TERMS OF BATTERY RETURN THE ONLY POINT I NEED TO CONTACT SERVER IS AT THE END WHEN I SEND DATA AT THIS POINT - I CAN DO THE RETURN PROCESS FIRST
		#If I can contact server
		
		
		#If I cannot contact server
	
	print "Execution finished"	#TESTING




# 4/10/16
# get when the battery was rented, and when it was returned for first iteration - we charge for time in this instance
# We have a heartbeat that constantly sends battery current draw to server - handle client side if its charged or not, and on this if statement, tell server battery is charged
	#Write code to contact server first, then after this is done, write code that is not serverside
	#On rental:
		# IF SERVER IS CONTACTABLE: User scans card and presses rent button
		# IF SERVER IS NOT CONTACTABLE: User scans card, reads the credit (is it $0 or is it not $0)
		# Determine which battery is free,record rental timestamp, send to server, read is it ok to rent, etc.
		# If I cant contact server on rental, just assume its ok to rent if they have some form of credit, and append to list of pending transactions
	
	#On return:
		# User scans card and presses return
		# Records surge current to determine which battery was returned
		# IF SERVER IS CONTACTABLE: timestamp and send data to server, get info from server, get user to tap again, write credit to card
		# IF SERVER IS NOT CONTACTABLE: Create object to hold server data, try and catch block for sending info to server (dictionary or something) or something like that (append to list of transactions)
	


