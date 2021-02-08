import speech_recognition as sr
import mqttlib

sr.Microphone.list_microphone_names()
mqttlib.identify()
mqttlib.connect()

#for index, name in enumerate(sr.Microphone.list_microphone_names()):
#    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

r = sr.Recognizer()

with sr.Microphone() as source:
	print("Speak your word:")
	audio = r.listen(source)
	r.adjust_for_ambient_noise(source)
	r.energy_threshold = 4000 
	r.dynamic_energy_threshold = True
while True:
	try:
		text = r.recognize_google(audio)
		print('You said: {}'.format(text))
		if("light" in text):
			mqttlib.light_toggle("TOGGLE")

	except:
		print('not working')
