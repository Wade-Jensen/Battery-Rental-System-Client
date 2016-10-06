from libRFID import *
import Adafruit_PN532 as PN532

#Configure the Reader
pn532 = initialise_RFID(18, 25, 23, 24)
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
        print('Failed to authenticate block 1!')
        continue
    # Read block 1 data.
    data = pn532.mifare_classic_read_block(1)
    if data is None:
        print('Failed to read block 1!')
        continue
    # Note that 16 bytes are returned, so only show the first 1 bytes for the block.
    print('Read block 1: 0x{0}'.format(binascii.hexlify(data[:1])))
	read = 0;
	print('Exiting Read Loop 1 \n')

	


#Write to Memory Block 1
while write:
	print('Place the card to be written on the PN532...')
	
	#Authenticate Block 1
	if not pn532.mifare_classic_authenticate_block(uid, 1, PN532.MIFARE_CMD_AUTH_B,
                                               CARD_KEY):
		print('Error! Failed to authenticate block 1 with the card.')
		continue
		
	dataWrite = 42
	data = bytearray(16)
	data[0:4] = b'MCPI'  # Header 'MCPI'
	data[4]   = dataWrite & 0xFF
	data[5] = 1
	data[6] = 0xFF
	
	# Write the card.
	if not pn532.mifare_classic_write_block(1, data):
		print('Error! Failed to write to the card.')
		continue
		
	print('Wrote card successfully!')	
	print('Exiting Write Loop 1 \n')
	write = 0


read = 1
#Read from Memory Block 1
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
        print('Failed to authenticate block 1!')
        continue
    # Read block 1 data.
    data = pn532.mifare_classic_read_block(1)
    if data is None:
        print('Failed to read block 1!')
        continue
    # Note that 16 bytes are returned, so only show the first 1 bytes for the block.
    print('Read block 1: 0x{0}'.format(binascii.hexlify(data[:1])))
	read = 0;
	print('Exiting Read Loop 2 \n')