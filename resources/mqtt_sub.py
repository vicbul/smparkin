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

    print 'rxPacketsReceived:', json_msg["rxPacketsReceived"]

    # Sending data in json format to django rest API
    r = requests.post('http://localhost:8000/resources/mqttsub/', json=json_msg)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(settings.MQTT_IP, settings.MQTT_PORT, 60)