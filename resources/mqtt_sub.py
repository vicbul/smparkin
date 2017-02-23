import paho.mqtt.client as mqtt
from SmartParking import settings
import json, requests, os

#Proxy env variables need to be disabled for requests to work properly on VM server
os.environ['http_proxy']=''
os.environ['https_proxy']=''

def on_connect(client, userdata, rc):
    print 'Subscriving to MQTT...'
    client.subscribe("gateway/#")

def on_message(client, userdata, msg):
    print 'Topic:', msg.topic, '/ QoS:', msg.qos, '/ Retain:', msg.retain
    print 'Payload:', msg.payload
    json_msg = json.loads(msg.payload)

    # Sending data in json format to django rest API
    if msg.topic.find('/stats') != -1:
        r = requests.post('http://localhost:8000/resources/gateway_stats/', json=json_msg)
    elif msg.topic.find('/rx') != -1:
        r = requests.post('http://localhost:8000/resources/gateway_rx/', json={"rxInfo": str(json_msg['rxInfo']), "phyPayload":str(json_msg['phyPayload'])})

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(settings.MQTT_IP, settings.MQTT_PORT, 60)