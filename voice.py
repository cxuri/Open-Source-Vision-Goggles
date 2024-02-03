import pyttsx3


rate = 130

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', rate)
engine.say("Hello master sreyas, how was your day")
engine.runAndWait()
