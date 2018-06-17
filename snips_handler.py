# encoding: utf-8
from __future__ import unicode_literals

import datetime
import json
import subprocess

import paho.mqtt.client as mqtt

fromtimestamp = datetime.datetime.fromtimestamp

# MQTT client to connect to the bus
mqtt_client = mqtt.Client()
HOST = "localhost"
PORT = 1883
HOTWORD_DETECTED = "hermes/hotword/default/detected"
HOTWORDS_ON = {"lumos"}
HOTWORDS_OFF = {"nocte"}


# Subscribe to the important messages
def on_connect(client, userdata, flags, rc):
    mqtt_client.subscribe(HOTWORD_DETECTED)


# Process a message as it arrives
def on_message(client, userdata, msg):
    if not msg.topic == HOTWORD_DETECTED:
        return

    payload = json.loads(msg.payload)
    model_id = payload["modelId"]
    if model_id in HOTWORDS_ON:
        subprocess.call(["/home/pi/lights_commands/chacon_send", "2", "12325261", "1", "on"])
    elif model_id in HOTWORDS_OFF:
        subprocess.call(["/home/pi/lights_commands/chacon_send", "2", "12325261", "1", "off"])
    else:
        print("Unmapped hotword model_id: %s" % model_id)


if __name__ == '__main__':
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(HOST, PORT)
    mqtt_client.loop_forever()
