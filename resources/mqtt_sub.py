import paho.mqtt.client as mqtt
from SmartParking import settings
import json, requests, os
import base64, binascii

#Proxy env variables need to be disabled for requests to work properly on VM server
os.environ['http_proxy']=''
os.environ['https_proxy']=''

def on_connect(client, userdata, rc):
    print 'Subscriving to MQTT...'
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
        r = requests.post('http://localhost:8000/resources/app_data/',
                          json={
                                 "applicationID": str(json_msg['applicationID']),
                                 "applicationName": str(json_msg['applicationName']),
                                 "nodeName": str(json_msg['nodeName']),
                                 "devEUI": str(json_msg['devEUI']),
                                 "data":str(json_msg['data']),
                                 "data_decoded":binascii.hexlify(base64.b64decode(json_msg['data'])),
                            })
        print 'data_decoded', binascii.hexlify(base64.b64decode(json_msg['data']))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(settings.MQTT_IP, settings.MQTT_PORT, 60)