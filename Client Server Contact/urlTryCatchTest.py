#Url Contact
import urllib2
import socket
import json
from collections import namedtuple

#Contact URL and retrieve JSON object
try:
	#req = urllib2.urlopen('http://ip.jsontest.comx/', timeout = 1)	#Create a request object using a bad URL(NOT SURE IF I NEED TO INCLUDE TIMEOUT OR SHOULD ADJUST IT)
	#req = urllib2.urlopen('http://httpstat.us/404', timeout = 1)    #Create 404 Error
	req = urllib2.urlopen('http://10.255.255.1/', timeout = 1)    #Create 408 Request Timeout Error	(Will still be caught by urllib2.URLERROR)
	#handle = urllib2.urlopen(req)									#Open to return a handle on the urllib2
	
except urllib2.HTTPError, e:		#Catch HTTP Error
	print 'Failed - Error Code: %s' %e.code
	
	if e.code == 404:		#Catch 404 Error
		#We can do something
		print '404 Error'
	else :
		#We can do something else
		print 'Not 404 Error'
		
	#return False

except urllib2.URLError as e:
    print type(e)    #not catch
    print 'Error in URL Address'
	
except socket.timeout as e:
    print type(e)    #catched
    print 'timeout error'
    raise MyException("There was an error: %r" % e)	
	
else:		#I think this is if everything went smoothly
	res = req.read()
	print('JSON Object')
	print(res)

	#Convert JSON into an object with attributes corresponding to dict keys.
	x = json.loads(res,object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
	print x.ip
