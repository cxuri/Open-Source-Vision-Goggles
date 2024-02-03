import speech_recognition as sr
import pyttsx3
import datetime 

rate = 140
text =''
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1)
engine.setProperty('rate', rate)

# Create a recognizer instance
recognizer = sr.Recognizer()

# Capture audio from the microphone
while True:
    with sr.Microphone() as source:
        print("Please speak something...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        # Listen for audio input
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Use Google Speech Recognition to recognize the audio
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        engine.say("Sorry, could not understand audio.")
    except sr.RequestError as e:
        engine.say("Could not request results; {0}".format(e))



    if text == "what is my name":
        print('hi')
        text =''
        engine.say("your name is Curry")

    elif text == "tell me about myself":
        engine.say('Hello mister curry, you are the command and control of this device, how can i assist you today, sir')
        text =''
    elif text == "tell me a joke":
        engine.say('Your life')
        text =''
    elif text == "who is the God":
        engine.say('For me , God is the creator of everything. so ill say my god is Master daaneesh and sreyas')
        text =''
    elif text == 'tell me the time':
        engine.say((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
        text =''
    elif text == 'who is your founder':
        engine.say('well i was programmed by master curry and sreyas')
        text =''
    elif text == 'who are the founders of this project':
        engine.say('master curry, master sreyas and a useless DAAABLO')
        text =''
    elif text == 'tell me about yourself':
        engine.say('My name is katy and im your personal assistant. version alpha. and im going to be in your open source vision goggles. thank you for having me ')
        text =''
    elif text == 'stop':
        engine.say('Ok sir im going to sleep.')
        text =''
        exit()

    engine.runAndWait()



