#!/usr/bin/python

#Import Library
from Subfact_ina219 import INA219

#Assign Current sensor as object ina (INA219 is initialization function, leaving it blank means it allocates to the default address, meaning 1 current sensor is connected)
ina = INA219()

#Get the bus voltage 
result = ina.getBusVoltage_V()

print "Shunt   : %.3f mV" % ina.getShuntVoltage_mV()
print "Bus     : %.3f V" % ina.getBusVoltage_V()
print "Current : %.3f mA" % ina.getCurrent_mA()


#Program flow for extending:
#Connect 4 current sensors for each battery, and determine which one has the highest % of charge, then return that charge level and battery number to the main function
#This will indicate to the user which battery to take, its current charge level, and send that information to the string which is sent to the main server
