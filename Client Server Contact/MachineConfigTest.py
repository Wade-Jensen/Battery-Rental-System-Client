#Url Contact
import urllib2
import json
import time
from collections import namedtuple

#Configure Name, Timestamp and number of batteries I can hold
name = 'Gerard'
ts = int(time.time())
batCap = 3

#Create URL string from information

contactString = "52.65.119.99:9000/test/name/%s/time/%s/capacity/%s" % (name,ts,batCap)
print(contactString)

#Contact URL and retrieve JSON object
req = urllib2.urlopen('52.65.119.99:9000/test/name/Gerard/time/1475406647/capacity/3')
res = req.read()
print('JSON Object')
print(res)

#Convert JSON into an object with attributes corresponding to dict keys.
x = json.loads(res,object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
print x.name, x.date, x.numBatteries
