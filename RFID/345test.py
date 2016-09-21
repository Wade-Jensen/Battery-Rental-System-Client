#This is a test program for reading a RFID card, detecting battery ID, machine ID and sending this data to a server for ENB345
# Author: Gerard Rallos

from libRFID import *
import Adafruit_PN532 as PN532

#Configure the Reader
pn532 = initialise_RFID(18, 25, 23, 24)		#Configure PN532 to the correct I/O pins on the breakout board (i.e. IO18,IO25 etc.)

#Main Loop
while True:


#Wait until a card is scanned
cardID = read(pn532)				#Read Current Value
print "Card ID %s" % cardID			#Print Current Value


#Determine if this is a return or a rental

	#If rental:
	
	
		# Determine which battery is available
			#Note - default to the battery with the most charge
		

		
		# Record charge level, Battery & Machine ID & Card Id, and concantenate together
	
	
	#If return:
	
		# Determine which battery has been returned
		
		
		
		# Determine charge level of battery
		
		
		
		# Record charge level, Battery & Machine ID & Card Id, and concantenate together
	
	
	

#Send data to server






print "Execution finished"



