#!/usr/bin/python

#Import Library
from Subfact_ina219 import INA219
import os
import time

#Assign Current sensor as object ina (INA219 is initialization function, leaving it blank means it allocates to the default address, meaning 1 current sensor is connected)
ina = INA219()
test = 1
#Get the bus voltage
while True:
    #result = ina.getBusVoltage_V()

    print "Shunt   : %f mV" % ina.getShuntVoltage_mV()
    print "Bus     : %f V" % ina.getBusVoltage_V()
    print "Current : %f mA" % ina.getCurrent_mA()

    if(test and ina.getCurrent_mA > 10) :
        print "TRIGGER"
    
    time.sleep(0.5)
    clear = lambda: os.system('clear')
    clear()
    
#Program flow for extending:
#Connect 4 current sensors for each battery, and determine which one has the highest % of charge, then return that charge level and battery number to the main function
#This will indicate to the user which battery to take, its current charge level, and send that information to the string which is sent to the main server
