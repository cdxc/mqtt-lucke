import speech_recognition as sr

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

r = sr.Recognizer()

with sr.Microphone() as source:
	print("Speak your word:")
	audio = r.listen(source)
	try:
		text = r.ibm(audio)
		print('You said: {}'.format(text))
	except:
		print('not working')

