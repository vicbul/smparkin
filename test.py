import base64, ast, json, socket, re, requests, array, binascii, datetime
from django.utils import timezone
from txthings import coap
from ipaddress import ip_address
from iotdm import iotdm_api
from resources.references import shortToLongDict
# from crypto.Cipher import AES
from lora.crypto import loramac_decrypt

x = 'AQIDBAUGBwgJCg=='
y = base64.b64encode('esto es una prueba')
print y

print base64.b64decode(x)

y = '{"sur":"/makazmie/django_sub","nev":{"rep":{"m2m:cnt":{"ct":"20170204T103036","st":0,"ty":3,"cbs":0,"ri":"7","lt":"20170204T103036","pi":"2","rn":"test","et":"29991231T111111","cni":0}},"net":"6"}}'
e = '{"error":"Resource target URI not found: /makazmie/test"}'
ae = '{"m2m:ae":{"rr":true,"ct":"20170205T151954","poa":[""],"aei":"testapp","ty":2,"ri":"7","lt":"20170205T151954","pi":"/makazmie/2","api":"","rn":"testapp","apn":"","et":"29991231T111111"}}'

test = 'XXXXXXX{"stat":{"time":"2017-02-16 20:02:16 CET","lati":50.04372,"long":19.96764,"alti":20,"rxnb":0,"rxok":0,"rxfw":0,"ackr":0.0,"dwnb":0,"txnb":0}}'

# x = requests.post('http://localhost:8000/resources/status',json=eval('{"stat":'+test.rsplit('{"stat":')[1].replace(' CET','')))

v = "/blabla/asfdg/rx"


Payload_stats = '''{"mac":"aa55c07bbc9e0ab0",
                 "time":"2017-02-22T19:54:36+01:00",
                 "latitude":50.04372,
                 "longitude":19.96764,
                 "altitude":20,
                 "rxPacketsReceived":0,
                 "rxPacketsReceivedOK":0,
                 "txPacketsReceived":0,
                 "txPacketsEmitted":0,
                 "customData":null}'''

Payload_rx = '''{"rxInfo":
                  {"mac":"aa55c07bbc9e0ab0",
                   "time":"0001-01-01T00:00:00Z",
                   "timestamp":44761715,
                   "frequency":868100000,
                   "channel":0,
                   "rfChain":0,
                   "crcStatus":-1,
                   "codeRate":"4/7",
                   "rssi":-102,
                   "loRaSNR":-10,
                   "size":5,
                   "dataRate":{"modulation":"LORA",
                               "spreadFactor":7,
                               "bandwidth":125}
                   },
              "phyPayload":"QAgHBgUAEgAD1E+aHI9SpIjP0+JqDZ7ZFJUnCw=="}'''

payload_decripted = '''{
                      "applicationID": "1",
                      "applicationName": "smparking",
                      "nodeName": "test_sensor_1",
                      "devEUI": "0002020800000000",
                      "rxInfo": [
                        {
                          "mac": "aa55c07bbc9e0ab0",
                          "rssi": -65,
                          "loRaSNR": 10.2
                        }
                      ],
                      "txInfo": {
                        "frequency": 868300000,
                        "dataRate": {
                          "modulation": "LORA",
                          "bandwidth": 125,
                          "spreadFactor": 7
                        },
                        "adr": true,
                        "codeRate": "4/5"
                      },
                      "fCnt": 92,
                      "fPort": 1,
                      "data": "AQIDBAUGBwgJCg=="
                    }'''


x = datetime.datetime.now()
print x.strftime('%d-%b-%Y %H:%M:%S')
print x.