import paho.mqtt.client as mqtt
c = mqtt.Client()

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

def identify():
	a = open('/usr/local/sbin/auth', 'r')
	content = a.read()
	u,p,x = content.split("\n")
	c.username_pw_set(username=u,password=p)

def light_toggle(arg):
	c.publish("cmnd/room_2svitlight/POWER", payload=arg)

def connect():
	c.connect("192.168.1.10", port=1883,)

