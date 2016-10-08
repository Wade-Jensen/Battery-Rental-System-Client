#This is a test program for reading a RFID card, detecting battery ID, machine ID and sending this data to a server for ENB345
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


#Initialize Current Sensors with correct addresses - Each battery has an associated sensor
inaOne = INA219()		#Base, 0x40
inaTwo = INA219()		#ETC....
inaThree = INA219()


#Initialize the Reader
pn532 = initialise_RFID(18, 25, 23, 24)		#Configure PN532 to the correct I/O pins on the breakout board (i.e. IO18,IO25 etc.)

#Initial Setup


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

#Main Loop
while True:
	cardScan = 0;		#Card is not currently scanned
	
	#Wait until a card is scanned
	while (cardScan != 1)		
		#Current Sensing:
			#Check all battery current draws
			batteryOneCurrent = inaOne.getCurrent_mA()
			batteryTwoCurrent = inaTwo.getCurrent_mA()
			batteryThreeCurrent = inaThree.getCurrent_mA()
			
			#Check if battery has finished charging (below 5mA is assumed to be charged, provided there is a battery currently connected)
			if()
				batteryOneCharged = 1
			if()
				batteryTwoCharged = 1
			if()
				batteryThreeCharged = 1
				
		#Card Scanning:
		cardID = 							#Check if card is scanned - Read Current Value (DONT USE READ SINCE IT WAITS UNTIL A CARD IS SCANNED)
		
		if()				#If a card is scanned
			cardScan = 1
			print "Card ID %s" % cardID			#Print Card ID (DEBUGGING PURPOSES)
			print "Please leave card on scanner until rental/return process is finished"
		else
			time.sleep(1)		#Pause for 1 second before next loop execution (reduce busy loading)
	
	#Rental/Return Process
		#Check if user intends to rent or return
		print "Please press 'Rent' or 'Return' for your desired service"
		while
	
		#Try and catch block for server contact
	
	#Rentals:
	if(batRent)
		print "This is a battery rental"
		#If I can contact server
		if()
			#Determine which battery is free
			
		
		
		
		
		#Else If I cannot contact server
		else
		
	#Returns:
	elif(batReturn)
		print "This is a battery return"
	
	print "Execution finished"




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
	


