#!/usr/bin/python3.11
import paho.mqtt.client as mqtt
import sys
c = mqtt.Client()

c.username_pw_set(username="",password="")
c.connect("192.168.1.10", port=1883,)

if sys.argv[1] == "luc":
    c.publish("cmnd/room_2svitlight/POWER", payload="TOGGLE")
elif sys.argv[1] == "zaluzije":
    if sys.argv[2] == "jug":
        if sys.argv[3] == "dol":
            c.publish("cmnd/blinds_2south/Backlog", payload="ShutterClose1")
        elif sys.argv[3] == "gor":
            c.publish("cmnd/blinds_2south/Backlog", payload="ShutterOpen1")
        elif sys.argv[3] == "percent":
            c.publish("cmnd/blinds_2south/shutterposition1", payload=sys.argv[4])

    elif sys.argv[2] == "zahod":
        if sys.argv[3] == "dol":
            c.publish("cmnd/blinds_2west/Backlog", payload="ShutterClose1")
        elif sys.argv[3] == "gor":
            c.publish("cmnd/blinds_2west/Backlog", payload="ShutterOpen1")
        elif sys.argv[3] == "percent":
            c.publish("cmnd/blinds_2west/shutterposition1", payload=sys.argv[4])

    elif sys.argv[2] == "balkon":
        if sys.argv[3] == "dol":
            c.publish("cmnd/blinds_2balcony/Backlog", payload="ShutterClose1")
        elif sys.argv[3] == "gor":
            c.publish("cmnd/blinds_2balcony/Backlog", payload="ShutterOpen1")
        elif sys.argv[3] == "percent":
            c.publish("cmnd/blinds_2balcony/ShutterPosition1", payload=sys.argv[4])

    elif sys.argv[2] == "okna":
        if sys.argv[3] == "dol":
            c.publish("cmnd/blinds_2west/Backlog", payload="ShutterClose1")
            c.publish("cmnd/blinds_2south/Backlog", payload="ShutterClose1")
        if sys.argv[3] == "gor":
            c.publish("cmnd/blinds_2west/Backlog", payload="ShutterOpen1")
            c.publish("cmnd/blinds_2south/Backlog", payload="ShutterOpen1")

    elif sys.argv[2] == "use":
        if sys.argv[3] == "dol":
            c.publish("cmnd/blinds_2west/Backlog", payload="ShutterClose1")
            c.publish("cmnd/blinds_2south/Backlog", payload="ShutterClose1")
            c.publish("cmnd/blinds_2balcony/Backlog", payload="ShutterClose1")
        elif sys.argv[3] == "gor":
            c.publish("cmnd/blinds_2west/Backlog", payload="ShutterOpen1")
            c.publish("cmnd/blinds_2south/Backlog", payload="ShutterOpen1")
            c.publish("cmnd/blinds_2balcony/Backlog", payload="ShutterOpen1")
        elif sys.argv[3] == "percent":
            c.publish("cmnd/blinds_2west/ShutterPosition1", payload=sys.argv[4])
            c.publish("cmnd/blinds_2south/ShutterPosition1", payload=sys.argv[4])
            c.publish("cmnd/blinds_2balcony/ShutterPosition1", payload=sys.argv[4])
        elif sys.argv[3] == "dim":
            c.publish("cmnd/blinds_2west/ShutterPosition2", payload=sys.argv[4])
            c.publish("cmnd/blinds_2south/ShutterPosition2", payload=sys.argv[4])
            c.publish("cmnd/blinds_2balcony/ShutterPosition2", payload=sys.argv[4])

    elif sys.argv[2] == "50/50":
        c.publish("cmnd/blinds_2west/ShutterPosition2", payload="50")
        c.publish("cmnd/blinds_2south/ShutterPosition2", payload="50")
        c.publish("cmnd/blinds_2balcony/ShutterPosition2", payload="50")
