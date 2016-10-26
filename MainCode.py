#This is a test program for reading a RFID card, detecting battery ID, machine ID and sending this data to a server for ENB345
#Written for Python 2, August-October 2016
#DEVELOPMENT BUILD 1.0
# Author: Gerard Rallos

#Import Libraries:
from libRFID import *					#RFID Library
import Adafruit_PN532 as PN532			#RFID Breakout
from Subfact_ina219 import INA219		#Current Sensor Breakout
import time								#Time library - sleep function
import datetime							#Datetime library - for return/charge times
import urllib2							#URL Library for python 2
import json								#JSON library
import threading						#Threading for server heartbeat
from collections import namedtuple		#For decoding JSON objects into dictionaries
from collections import deque			#For backlog data storage
import RPi.GPIO as GPIO					#GPIO Pins

#Initialize Current Sensors with correct addresses - Each battery has an associated sensor
inaOne = INA219(0x40)		#Base, 0x40
inaTwo = INA219(0x41)		#A0 Bridge
inaThree = INA219(0x44)		#A1 Bridge

#Initialize the Reader
pn532 = initialise_RFID(18, 25, 23, 24)		#Configure PN532 to the correct I/O pins on the breakout board (i.e. IO18,IO25 etc.)

#Define Functions:
def serverPing ( urlString ):		#Accepts a string
	try:
		request = urllib2.urlopen(urlString, timeout = 1)	#Ping server

	except urllib2.HTTPError, e:		#Catch HTTP Error
		print 'Failed - Error Code: %s' %e.code
		contact = 0
		
	except urllib2.URLError as e:		#URL Error Catch
		print type(e)    
		print 'Error in URL Address'			
		contact = 0
		
	else :
		contact = 1						#If no error is caught, server can be contacted
	
	return contact

def serverHeartbeat () :
	threading.Timer(30.0, serverHeartbeat).start()
	serverContact = serverPing ('URL')

	#Get Battery Current Draw:
	#Send battery current draw even if battery is not connected
	batteryOneCurrentHeart = inaOne.getCurrent_mA()
	batteryTwoCurrentHeart = inaTwo.getCurrent_mA()
	batteryThreeCurrentHeart = inaThree.getCurrent_mA()			
	
	if(serverContact) :
		#Send backlog data to server if any exists
		numBacklog = len(backlogData)
		if(len(backlogData)) :
			for x in range(0,numBacklog) :
				request = urllib2.urlopen(backlogData.pop(), timeout = 1)	#Send backlog data
				
				
	#else :
	
		#APPEND CURRENT DRAW TO BACKLOG DATA (MAY HAVE TO CONSIDER LIMITATIONS IF I HAVE HOURS OF BACKLOG DATA - MAYBE ONLY SEND BATCHES OF IT AT A TIME)

		
		
		
#Initial Setup
#Machine Specific Configuration
numSlots = 3
machineLocation = 'QUTGP'

setup = 1
while setup:
	serverConnection = serverPing ('http://52.63.34.239:9000/api/alive')		#Check if server can be contacted
	if (serverConnection) :
	
		setupURL = "http://52.63.34.239:9000/api/startmachine/numSlots/%s/textlocation/%s" % (numSlots,machineLocation)
		initialRequest = urllib2.urlopen(setupURL, timeout = 1)
		initialRes = initialRequest.read()
		
		initalConfig = json.loads(initialRes,object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
		
		machineID = initalConfig.id					#Machine ID
		numBatteries = initalConfig.numBatteries	#Number of batteries in machine
		print  "Machine ID: %s,  Connected Batteries: %s" % initalConfig.id, initalConfig.numBatteries
	
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

#Initialize empty backlog deque
backlogData = deque()

#Initialize server heartbeat thread
serverHeartbeat()

#Main Loop
while True:
	cardScan = 0		#Card is not currently scanned
	
	#Turn off all LED's for battery slots
	GPIO.output(SLOT_ONE_LED_LED,GPIO.LOW)	
	GPIO.output(SLOT_TWO_LED_LED_LED,GPIO.LOW)	
	GPIO.output(SLOT_THREE_LED_LED_LED,GPIO.LOW)	
	
	#Wait until a card is scanned
	while (cardScan != 1):
		#Current Sensing:
			#Check all battery current draws
			batteryOneCurrent = inaOne.getCurrent_mA()
			batteryTwoCurrent = inaTwo.getCurrent_mA()
			batteryThreeCurrent = inaThree.getCurrent_mA()
			
			#Check if battery has finished charging and it was previously rented (below 5mA is assumed to be charged, provided there is a battery currently connected)
			if() :	#ALSO SEND A MESSAGE FOR WHEN THE BATTERY IS FULLY CHARGES
				batteryOneCharged = 1
				serverConnection = serverPing ('http://52.63.34.239:9000/api/alive')		#Check if server can be contacted
				fullTime = int(time.time())
				chargeString = "http://52.63.34.239:9000/api/fullcharge/machineId/%s/time/%s/machineSlot/%s" % (MACHINE ID, fullTime, 1)
				if(serverConnection)
					fullCharge = urllib2.urlopen(returnURL)
				else
				backlogData.append(chargeString)
				
			if() :
				batteryTwoCharged = 1
				serverConnection = serverPing ('http://52.63.34.239:9000/api/alive')		#Check if server can be contacted
				fullTime = int(time.time())
				chargeString = "http://52.63.34.239:9000/api/fullcharge/machineId/%s/time/%s/machineSlot/%s" % (MACHINE ID, fullTime, 2)
				if(serverConnection)
					fullCharge = urllib2.urlopen(returnURL)
				else
				backlogData.append(chargeString)				
			if() :
				batteryThreeCharged = 1
				serverConnection = serverPing ('http://52.63.34.239:9000/api/alive')		#Check if server can be contacted
				fullTime = int(time.time())
				chargeString = "http://52.63.34.239:9000/api/fullcharge/machineId/%s/time/%s/machineSlot/%s" % (MACHINE ID, fullTime, 3)
				if(serverConnection)
					fullCharge = urllib2.urlopen(returnURL)
				else
				backlogData.append(chargeString)				
	
		#Card Scanning:
		cardID = pn532.read_passive_target()							#Check if card is scanned
		
		if cardID is None:				
			time.sleep(1)		#Pause for 1 second before next loop execution (reduce busy loading)
			continue
									
		cardScan = 1
		print "Card ID %s" % cardID			#Print Card ID (TESTING)
		print "Please leave card on scanner until rental/return process is finished"
	
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
		
	#Rentals:
	if (batRent) :
		serverConnection = serverPing ('http://52.63.34.239:9000/api/alive')	#Check if server can be contacted
		print "This is a battery rental"
		if (serverConnection) :												#If I can contact server
			#Determine which battery is free			
			if (batteryOneCharged):											#Proceed through list of batteries
				allocatedBattery = 1			
			elif (batteryTwoCharged):
				allocatedBattery = 2		
			elif (batteryThreeCharged):
				allocatedBattery = 3	
			else :
				print "No batteries charged, please try another machine"	#If no batteries are charged
				continue			
		
			batTime = int(time.time())		#Time battery was rented
			
			#Send information to server
			rentalURL = "http://52.63.34.239:9000/api/requestbattery/machineId/%s/machineSlot/%s/cardId/%s/time/%s" % (MACHINE ID, allocatedBattery, cardID, batTime)
			print (rentalURL)		#TESTING
			
			#Contact URL and retrieve JSON object
			rentalRequest = urllib2.urlopen(rentalURL)
			rentalRes = rentalRequest.read()
			print "JSON OBJECT"		#TESTING
			print (rentalRes)

			#Convert JSON into an object with attributes corresponding to dict keys.
			rentalJson = json.loads(res,object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
			print rentalJson
		
			#Check if user is permitted to rent battery
			if (rentalJson.isUserBalancePositive == 'true') :
				#Rent battery out to user
					#SET LED INDICATING BATTERY, TELL USER TO REMOVE CARD AND BATTERY, UPDATE WHICH BATTERY IS REMOVED
				if(allocatedBattery == 1) :
					GPIO.output(SLOT_ONE_LED_LED,GPIO.HIGH)
					batOneAlloc = 1

				elif(allocatedBattery == 2) :
					GPIO.output(SLOT_TWO_LED_LED_LED,GPIO.HIGH)
					batTwoAlloc = 1					
					
				elif(allocatedBattery == 3) :
					GPIO.output(SLOT_THREE_LED_LED_LED,GPIO.HIGH)	
					batThreeAlloc = 1
							
				print "Your battery is indicated by the light, please remove battery and remove your card, thank you!"
			else :
				print "Insufficienct credit or user otherwise not permitted to rent battery - please remove card"
				continue
			
		else :															#If I cannot contact server
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
				tempString = data[0:(data.find(b'\x00'))]			#Remove empty bits from data string
				userCredit = int(tempString)						#Current credit on card (in cents)
				print "Current Credit: $%s" %(userCredit / 100)
				read = 0;
			
			if (userCredit > 0) :		#If user has enough credit, do battery rental process and instead of contacting server, append to backlog list
				#Determine which battery to rent out
				if (batteryOneCharged):											#Proceed through list of batteries
					allocatedBattery = 1
					batOneAlloc = 1
					GPIO.output(SLOT_ONE_LED_LED,GPIO.HIGH)	
		
				elif (batteryTwoCharged):
					allocatedBattery = 2
					batTwoAlloc = 1
					GPIO.output(SLOT_TWO_LED_LED,GPIO.HIGH)		
					
				elif (batteryThreeCharged):
					allocatedBattery = 3
					batThreeAlloc = 1
					GPIO.output(SLOT_THREE_LED_LED,GPIO.HIGH)		
					
				else :
					print "No batteries charged, please try another machine"	#If no batteries are charged
					continue			
			
				#Create string to insert into deque backlog
				batTime = int(time.time())		#Time battery was rented
				rentalURL = "http://52.63.34.239:9000/api/requestbattery/machineId/%s/machineSlot/%s/cardId/%s/time/%s" % (MACHINE ID, allocatedBattery, cardID, batTime)
				backlogData.append(rentalURL)
				print (rentalURL)		#TESTING				
					
			else :		#Else if credit is insufficient, reject user and continue
				print "Insufficient credit, please remove card"
				time.sleep(5)
				continue
				
				
	#Returns:
	elif (batReturn) :
		print "This is a battery return - please put battery into empty slot then press return again"
		
		#ACTUALLY IN TERMS OF BATTERY RETURN THE ONLY POINT I NEED TO CONTACT SERVER IS AT THE END WHEN I SEND DATA AT THIS POINT - I CAN DO THE RETURN PROCESS FIRST
		while (GPIO.input(RETURN_BUTTON)) :	#MAY NEED TO MAKE THIS MORE EFFICIENT - LIKE CHECKING FOR BUTTON PRESSES FIRST
		#Find which battery is returned by recording surge current
			if ( batOneAlloc and (inaOne.getCurrent_mA() > 5)) :
				returnedBattery = 1
				batOneAlloc = 0
				
			elif ( batTwoAllocAlloc and (inaTwo.getCurrent_mA() > 5)) :
				returnedBattery = 2
				batTwoAlloc = 0		
			
			elif ( batThreeAllocAlloc and (inaThree.getCurrent_mA() > 5)) : 
				returnedBattery = 3
				batThreeAlloc = 0		
		
		batTime = int(time.time())		#Time battery was returned
		
		returnURL = "http://52.63.34.239:9000/api/returnbattery/machineId/%s/machineSlot/%s/cardId/%s/time/%s" % (MACHINE ID, returnedBattery, cardID, batTime)		#Create the return url
		serverConnection = serverPing ('52.63.139.51/api/alive' )									#Check if server can be contacted		
		
		#If I can contact server
		if (serverConnection) :		

			#Contact URL and retrieve JSON object
			returnRequest = urllib2.urlopen(returnURL)
			resReturn = returnRequest.read()
			
			print "JSON OBJECT"		#TESTING
			print (res)

			#Convert JSON into an object with attributes corresponding to dict keys.
			returnJson = json.loads(res,object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
			print returnJson				
			
			#Write credit to card
			credit = str(returnJson.balance)
			#Authenticate Block 1
			if not pn532.mifare_classic_authenticate_block(uid, 1, PN532.MIFARE_CMD_AUTH_B,
																				   [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
				print('Error! Failed to authenticate block 1 with the card.')
				continue

			#Data array size must by 16 bytes
			data = bytearray(16)
			dataWrite = bytes(credit, 'utf-8')
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
			print (returnURL)		#TESTING	
		
		
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
	

#20/10/16:
	#ON RETURN, THIS IS WHEN I UPDATE THE CARD CREDIT
	#I SEND YOU THE MACHINE LOCATION ON STARTUP (AS A STRING - "QUT GP" or "QUT KG") AND I GET BACK THE DATA TO SET PARAMETERS REGARDLESS OF WHETHER IM A NEW MACHINE OR NOT
	# - PACKET CONTAINS MACHINE ID AND WHAT BATTERIES ARE IN THERE IN WHICH SLOTS