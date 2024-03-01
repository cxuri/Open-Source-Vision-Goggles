import speech_recognition as sr
import pyttsx3
from conv import conversation
from db import read, modify

filename = "settings.json"
dataset = read(filename)

def say(text):
    engine.say(text)
    engine.runAndWait()

def reload_config():
    global dataset
    dataset = read(filename)

def settings(query):
    reload_config()
    current_volume = float(dataset["volume"])
    current_rate = int(dataset["speech-rate"])
    current_gender = int(dataset["gender"])

    if query == "raise the volume":
        if current_volume >= 1.0:
            say("Volume is already at maximum.")
        else:
            current_volume += 0.3
            modify(filename, "volume", str(current_volume))
            reload_config()
            say("Volume has increased by 30%.")
    elif query == "lower the volume":
        if current_volume <= 0.3:
            say("Volume is already at minimum.")
        else:
            current_volume -= 0.3
            modify(filename, "volume", str(current_volume))
            reload_config()
            say("Volume has decreased by 30%.")
    elif query == "raise the speech rate":
            if current_rate >= 180:
                say("Speech rate is at maximum!")
            else:
                current_rate += 20
                modify(filename, "speech-rate", str(current_rate))
                reload_config()
                say("Speech rate has increased by 20 percent")
    elif query == "lower the speech rate":
            if current_rate <= 60:
                say("speech rate is at minimum")
            else:
                current_rate -= 20
                modify(filename, "speech-rate", str(current_rate)) 
                reload_config()
                say("speech rate has decreased by 20 percent")
    elif query == "change voice":
            if(current_gender == 1):
                current_gender = 0
                modify(filename, "gender", str(current_gender))
                reload_config()
                say("Hi im your new voice")
            else:
                current_gender = 1
                modify(filename, "gender", str(current_gender))
                reload_config()
                say("Hi im your new voice")
    else:
        pass
            
# Initialize speech recognizer outside the voice function
recognizer = sr.Recognizer()

# Initialize speech engine
engine = pyttsx3.init()

# Capture audio from the microphone
def voice():
    while True:
        reload_config()

        rate = int(dataset["speech-rate"])
        gender = int(dataset["gender"])
        volume = float(dataset["volume"])

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[gender].id)
        engine.setProperty('volume', volume)
        engine.setProperty('rate', rate)    

        with sr.Microphone() as source:
            print("Please speak something...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio).lower().strip("?!.,;:'")
            print("You said:", text)

            settings(text)
            if text == 'exit':
                break
            else:
                reply = conversation(text)
                say(reply)

        except sr.UnknownValueError:
            say("Sorry, could not understand audio.")
        except sr.RequestError as e:
            say(f"Could not request results: {e}")
