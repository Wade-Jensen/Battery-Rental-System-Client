import binascii
import sys
import Adafruit_PN532 as PN532

def initialise_RFID(CS, SCLK, MOSI, MISO):
    #creat pn532 of class PN532 
    pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

    # initialize comms with PN532
    pn532.begin()

    # set comms from PN532 to mifarecard
    pn532.SAM_configuration()

    return pn532

def read(pn532):

    # set uid to be nothing
    uid = pn532.read_passive_target()

    while uid is None:
        # check if there is a card
        uid = pn532.read_passive_target()
        # if no card try again

    ID = binascii.hexlify(uid)
    return ID
