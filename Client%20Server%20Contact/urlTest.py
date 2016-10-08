#Url Contact
import urllib2
import json
from collections import namedtuple

#Contact URL and retrieve JSON object
req = urllib2.urlopen('http://ip.jsontest.com/')
res = req.read()
print('JSON Object')
print(res)

#Convert JSON into an object with attributes corresponding to dict keys.
x = json.loads(res,object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
print x.ip
