from SmartParking import settings
import json, base64, random, time
import paho.mqtt.client as mqtt

def random_data():
    # digits 0 - 1 = number of sensors connected
    # digits 2 - 11 = state of the sensor: 0 (free), 1 (occupied), 2 (out of service)
    # i.e.: 101000211001
    status = ['10']
    for i in range(0,10):
        value = random.randrange(0, 3)
        status.append(str(value))
    data = ''.join(status)
    return base64.b64encode(data)

#this is a simulation of the decripted payload post to MQTT application/appID/node/nodeEUI/rx topic
def simulator():
    MU_number = str(random.randrange(1,11))
    simulated_payload = {
                          "applicationID": "0",
                          "applicationName": "simulator",
                          "nodeName": "MU_"+MU_number,
                          "devEUI": "000202080000000"+MU_number if int(MU_number) < 10 else "00020208000000"+MU_number, # "0002020800000000"
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
                            "adr": True, # true for json
                            "codeRate": "4/5"
                          },
                          "fCnt": 92,
                          "fPort": 1,
                          "data": random_data() # "AQIDBAUGBwgJCg=="
                        }
    return simulated_payload

client = mqtt.Client()
client.connect(settings.MQTT_IP, settings.MQTT_PORT, 60)

for i in range(0,2):
    simulated_instance = simulator()
    print simulated_instance
    payload = json.dumps(simulated_instance)
    client.publish(topic='application/'+simulated_instance['applicationID']+'/node/'+simulated_instance['devEUI']+'/rx',
                   payload=payload)
    time.sleep(5)

client.disconnect()