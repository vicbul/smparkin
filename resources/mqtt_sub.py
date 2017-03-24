import paho.mqtt.client as mqtt
from SmartParking import settings
import json, requests, os, signal
import base64, binascii
# from resources.models import *

#Proxy env variables need to be disabled for requests to work properly on VM server
os.environ['http_proxy']=''
os.environ['https_proxy']=''

def on_connect(client, userdata, rc):
    print 'Subscribing to MQTT...'
    client.subscribe("gateway/#")
    client.subscribe("application/#")

def on_message(client, userdata, msg):
    print 'Topic:', msg.topic, '/ QoS:', msg.qos, '/ Retain:', msg.retain
    print 'Payload:', msg.payload
    json_msg = json.loads(msg.payload)

    # Sending data in json format to django rest API. Splitting between stats and rxinfo
    if msg.topic.find('gateway') != -1:
        if msg.topic.find('/stats') != -1:
            r = requests.post('http://localhost:8000/resources/gateway_stats/', json=json_msg)
        elif msg.topic.find('/rx') != -1:
            r = requests.post('http://localhost:8000/resources/gateway_rx/',
                              json={
                                  "rxInfo": str(json_msg['rxInfo']),
                                  "phyPayload":str(json_msg['phyPayload'])
                              })
    elif msg.topic.find('application') != -1:
        if msg.topic.find('/rx') != -1:
            decoded_data = base64.b64decode(json_msg['data'])
            r = requests.post('http://localhost:8000/resources/app_data/',
                              json={
                                     "applicationID": str(json_msg['applicationID']),
                                     "applicationName": str(json_msg['applicationName']),
                                     "nodeName": str(json_msg['nodeName']),
                                     "devEUI": str(json_msg['devEUI']),
                                     "data":str(json_msg['data']),
                                     # "data_decoded":binascii.hexlify(base64.b64decode(json_msg['data'])),
                                     "data_decoded":decoded_data,
                                })
            print 'data_decoded', binascii.hexlify(base64.b64decode(json_msg['data']))

            # if not APP.objects.get(resourceID = str(json_msg['applicationID'])):
            app = requests.post('http://localhost:8000/resources/app/',
                              json={
                                     "resourceID": str(json_msg['applicationID']),
                                     "name": str(json_msg['applicationName']),
                              })

            # if not APP.objects.get(resourceID = str(json_msg['devEUI'])):
            mu = requests.post('http://localhost:8000/resources/container/',
                              json={
                                     "resourceID": str(json_msg['devEUI']),
                                     "name": str(json_msg['nodeName']),
                                     "parent": str(json_msg['applicationID']),
                              })

            sensors_amount = int(decoded_data[0:2])
            sensors_status = [int(s) for s in decoded_data[2:]]
            i = 1
            for s in sensors_status:
                sensor_cnt = requests.post('http://localhost:8000/resources/container/',
                                  json={
                                         "resourceID": str(json_msg['devEUI'])+'_'+str(i),
                                         "name": "sensor_"+str(i),
                                         "parent": str(json_msg['devEUI']),
                                  })
                rx_cnt = requests.post('http://localhost:8000/resources/container/',
                                  json={
                                         "resourceID": str(json_msg['devEUI'])+'_'+str(i)+"_rx",
                                         "name": "rx",
                                         "parent": str(json_msg['devEUI'])+'_'+str(i),
                                  })

                tx_cnt = requests.post('http://localhost:8000/resources/container/',
                                  json={
                                         "resourceID": str(json_msg['devEUI'])+'_'+str(i)+"_tx",
                                         "name": "tx",
                                         "parent": str(json_msg['devEUI'])+'_'+str(i),
                                  })


                sensor_cin = requests.post('http://localhost:8000/resources/cin/',
                                  json={
                                         "name": "cin",
                                         "parent": str(json_msg['devEUI'])+'_'+str(i)+"_rx",
                                         "content": s,
                                  })
                i += 1

def connect():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    def handler(signum, frame):
        print 'Signal handler called with signal', signum
        raise IOError("Couldn't connect to MQTT server!")
        # print "Couldn't connect!"

    # Set the signal handler and a 5-second alarm
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(5)

    # This open() may hang indefinitely
    c = client.connect(settings.MQTT_IP, settings.MQTT_PORT, 60)
    print c
    signal.alarm(0)          # Disable the alarm

    # client.connect(settings.MQTT_IP, settings.MQTT_PORT, 5)
    print 'Starting MQTT loop'
    client.loop_start()