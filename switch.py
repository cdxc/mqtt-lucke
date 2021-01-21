#!/usr/bin/python3.9

import paho.mqtt.client as mqtt
import time

# Prebere podatke za prijavo iz "auth" datoteke
a = open('auth', 'r')
content = a.read()
u,p,x = content.split("\n")


# Preveri povezavo
def on_connect(client, userdata, flags, rc):
        print("Povezava je izpostavljena: "+str(rc))


# Defines
c = mqtt.Client()
c.username_pw_set(username=u,password=p)
c.on_connect=on_connect

# Prizge 
c.connect("192.168.1.10", port=1883)
c.publish("cmnd/room_2svitlight/POWER", payload='TOGGLE')
