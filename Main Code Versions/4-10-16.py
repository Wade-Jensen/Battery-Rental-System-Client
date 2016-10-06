#This is a test program for reading a RFID card, detecting battery ID, machine ID and sending this data to a server for ENB345
# Author: Gerard Rallos

#Import Libraries:
from libRFID import *					#RFID Library
import Adafruit_PN532 as PN532			#RFID Breakout
from Subfact_ina219 import INA219		#Current Sensor Breakout
import time								#Time library - sleep function
import datetime							#Datetime library - for return/charge times

#General Parameters:
machineID = 'prototype'			#ID of this specific machine

#Battery Parameter Variables:
	#Note, assumption is that on program initialization, all batteries are connected (may or may not be charged)
	#If battery is connected, if battery is charged and once battery is charged, when was the battery returned and what was the batteries charge upon return (assuming current flow regulated)
batteryOneConnect = 1			#Is the battery connected
batteryOneCharged = 0			#Is the battery charged
batteryOneReturnStatus = 1		#Has the battery being returned yet (0 is not returned, 1 is returned and 2 is returned and charge level recorded)
batteryOneReturnTime = 0		#When was the battery returned
batteryOneReturnCharge = 0		#(Calculated) What charge was the battery returned with

batteryTwoConnect = 1
batteryTwoCharged = 0
batteryTwoReturnStatus = 1
batteryTwoReturnTime = 0
batteryTwoReturnCharge = 0

batteryThreeConnect = 1
batteryThreeCharged = 0
batteryThreeReturnStatus = 1
batteryThreeReturnTime = 0
batteryThreeReturnCharge = 0

batteryFourConnect = 1
batteryFourCharged = 0
batteryFourReturnStatus = 1
batteryFourReturnTime = 0
batteryFourReturnCharge = 0


#Initialize Current Sensors with correct addresses - Each battery has an associated sensor
inaOne = INA219()		#Base, 0x40
inaTwo = INA219()		#ETC....


#Initialize the Reader
pn532 = initialise_RFID(18, 25, 23, 24)		#Configure PN532 to the correct I/O pins on the breakout board (i.e. IO18,IO25 etc.)


#Main Loop
while True:
	cardScan = 0;		#Card is not currently scanned
	
	#Wait until a card is scanned
	while (cardScan != 1)		
		#Current Sensing:
			#Check all battery current draws
			batteryOneCurrent = inaOne.getCurrent_mA()
			
			#Check if battery has finished charging
			if(batteryOneCurrent < TEMP and batteryOneConnect == 1)		#If battery is connected and current draw is below threshold, it is assumed to have finished charging 
				batteryOneCharged = 1
				batteryOneChargeTime = datetime.datetime.now()
				if(batteryOneReturnStatus == 1)		#If battery one was previously returned
					batteryOneReturnCharge = 
					batteryOneReturnStatus = 2		#Charge level recorded
				
		#Card Scanning:
		cardID = 							#Check if card is scanned - Read Current Value (DONT USE READ SINCE IT WAITS UNTIL A CARD IS SCANNED)
		
		if()				#If a card is scanned
			cardScan = 1
			print "Card ID %s" % cardID			#Print Card ID
		else
			time.sleep(1)		#Pause for 1 second before next loop execution (reduce busy loading)
	
	#Determine if this is a return or a rental

	#If rental:
	
	#IF IT IS A RENTAL, THEY SCAN ID THEN PRESS A RENT OR RETURN BUTTON
	
		# Determine which battery is available (if any)
			#Note - only fully charged batteries currently allowed
	charge = batteryOneCharged + batteryTwoCharged + batteryThreeCharged + batteryFourCharged
	if(charge < 1)		#If no batteries are charged, return to beginning of loop
		print "No batteries currently charged, please try again later"
		continue
		
		
		
		# Record timestamp, Battery & Machine ID & Card Id, and concantenate together
	
		#Get JSON object from server to determine if its ok to release battery, read bool and release battery if so
		
	
	#If return:
	
		# Determine which battery has been returned & send an immediate acknowledgement to the server to indicate that the user has returned something
	if()		#TEMP - BATTERY 1 (MAY NOT BE AN IF STATEMENT, JUST TO GET RETURN LOGIC CORRECT)
		batteryOneReturnTime = datetime.datetime.now()
		batteryOneReturnID = cardID
		
		
		
		# Record timestamp, Battery & Machine ID & Card Id, and concantenate together
	
	#If we can get 
		# Get JSON object from server and write credit to user card

		
	#Send data to server
		#Make a dictionary of things to push to the server - if it was able to push it to the server, then remove it from the dictionary
		#If it was not able to push it to the server, then try again later






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
	


