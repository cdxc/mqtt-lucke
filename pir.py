#!/usr/bin/python3.9

import json
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time

# Reads credidentals from auth
a = open('/usr/local/sbin/auth', 'r')
content = a.read()
u,p,x = content.split("\n")

def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))


def on_message(client, userdata, message):
    print(str(message.payload))
    if (str(message.payload)) == "b'ON'":
        c.publish("cmnd/room_2svitlight/POWER", payload='ON') # 
    if (str(message.payload)) == "b'OFF'":                    # This is your light switch topic
        c.publish("cmnd/room_2svitlight/POWER", payload='OFF')#


# Defines
c = mqtt.Client()
c.username_pw_set(username=u,password=p)
c.on_connect=on_connect
c.on_message=on_message

c.connect("192.168.1.10", port=1883, keepalive=60,bind_address="")
c.loop_start()
c.subscribe("stat/room_2svitlight/PIR1") # This is your PIR sensor topic
while True:
    time.sleep(1)

c.loop_stop()

