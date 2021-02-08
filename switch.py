#!/usr/bin/python3.7
import mqttlib 

mqttlib.identify()
mqttlib.connect()
mqttlib.light_toggle("TOGGLE")
