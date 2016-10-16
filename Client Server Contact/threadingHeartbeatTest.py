#Url Contact
import urllib2
import json
import threading
from collections import namedtuple

def serverPing ( urlString ):		#Accepts a string
	try:
		req = urllib2.urlopen(urlString, timeout = 1)	#Ping server

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
	threading.Timer(5.0, serverHeartbeat).start()
	serverContact = serverPing ('http://ip.jsontest.comx/')
	
	if(serverContact) :
		print 'Threading Sucessful, server can be reached'
		
	else :
		print 'Threading Sucessful, server cannot be reached'
		
		
serverHeartbeat()
	
	
	
	
	
