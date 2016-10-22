#!/usr/bin/python

#Import Library
from Subfact_ina219 import INA219
import os
import time

#Assign Current sensor as object ina (INA219 is initialization function, leaving it blank means it allocates to the default address, meaning 1 current sensor is connected)
inaOne = INA219(0x40)
inaTwo = INA219(0x41)
inaThree = INA219(0x44)

while True:
    #result = ina.getBusVoltage_V()

    print "Shunt   : %.3f mV" % inaOne.getShuntVoltage_mV()
    print "Bus     : %.3f V" % inaOne.getBusVoltage_V()
    print "Current : %.3f mA" % inaOne.getCurrent_mA()
	
    print "Shunt   : %.3f mV" % inaTwo.getShuntVoltage_mV()
    print "Bus     : %.3f V" % inaTwo.getBusVoltage_V()
    print "Current : %.3f mA" % inaTwo.getCurrent_mA()	
	
    print "Shunt   : %.3f mV" % inaThree.getShuntVoltage_mV()
    print "Bus     : %.3f V" % inaThree.getBusVoltage_V()
    print "Current : %.3f mA" % inaThree.getCurrent_mA()	
	
    time.sleep(0.5)
    clear = lambda: os.system('clear')
    clear()
    
#Program flow for extending:
#Connect 4 current sensors for each battery, and determine which one has the highest % of charge, then return that charge level and battery number to the main function
#This will indicate to the user which battery to take, its current charge level, and send that information to the string which is sent to the main server
