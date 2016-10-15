#Url Contact
import urllib2
import socket
import json
from collections import namedtuple

#Contact URL and retrieve JSON object
try:
	req = urllib2.urlopen('http://ip.jsontest.com/', timeout = 1)	#Create a request object (NOT SURE IF I NEED TO INCLUDE TIMEOUT OR SHOULD ADJUST IT)
	handle = urllib2.urlopen(req)									#Open to return a handle on the urllib2
	
except urllib2.HTTPError, e:		#Catch HTTP Error
	print 'Failed - Error Code: %s' %e.code
	
	if e.code == 404		#Catch 404 Error
		#We can do something
	else
		#We can do something else
		
	return false

except urllib2.URLError as e:
    print type(e)    #not catch
	
except socket.timeout as e:
    print type(e)    #catched
    raise MyException("There was an error: %r" % e)	
	
else:		#I think this is if everything went smoothly
	res = req.read()
	print('JSON Object')
	print(res)

	#Convert JSON into an object with attributes corresponding to dict keys.
	x = json.loads(res,object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
	print x.ip
