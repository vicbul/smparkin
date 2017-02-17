import base64, ast, json, socket, re
from txthings import coap
from ipaddress import ip_address
from iotdm import iotdm_api
from resources.references import shortToLongDict

x = 'AQIDBAUGBwgJCg=='
y = base64.b64encode('esto es una prueba')
print y

print base64.b64decode(x)

y = '{"sur":"/makazmie/django_sub","nev":{"rep":{"m2m:cnt":{"ct":"20170204T103036","st":0,"ty":3,"cbs":0,"ri":"7","lt":"20170204T103036","pi":"2","rn":"test","et":"29991231T111111","cni":0}},"net":"6"}}'
e = '{"error":"Resource target URI not found: /makazmie/test"}'
ae = '{"m2m:ae":{"rr":true,"ct":"20170205T151954","poa":[""],"aei":"testapp","ty":2,"ri":"7","lt":"20170205T151954","pi":"/makazmie/2","api":"","rn":"testapp","apn":"","et":"29991231T111111"}}'

test = 'XXXXXXXXX{"stat":{"time":"2017-02-16 20:02:16 CET","lati":50.04372,"long":19.96764,"alti":20,"rxnb":0,"rxok":0,"rxfw":0,"ackr":0.0,"dwnb":0,"txnb":0}}'

print test.rsplit('{"',1)[1]