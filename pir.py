#!/usr/bin/python3.9

import json
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import mqttlib
import time

mqttlib.on_connect()
mqttlib.connect()
mqttlib.identify


def on_message(client, userdata, message):
    print(str(message.payload))
    if (str(message.payload)) == "b'ON'":
		mqttlib.light_toggle("ON")
    if (str(message.payload)) == "b'OFF'":
		mqttlib.light_toggle("OFF")

c.connect("192.168.1.10", port=1883, keepalive=60,bind_address="")
c.loop_start()
c.subscribe("stat/room_2svitlight/PIR1") # This is your PIR sensor topic
while True:
    time.sleep(1)

c.loop_stop()

