import cv2
import multiprocessing
import speech_recognition as sr
import pyttsx3
from db import read, modify
from conv import conversation
import os
from datetime import datetime

queue = multiprocessing.Queue()

# Initialize settings
filename = "settings.json"
filepath = os.path.join(os.getcwd(), 'db', filename)
dataset = read(filepath)

# Initialize cascade classifiers
cascades = {
    "car": cv2.CascadeClassifier(cv2.data.haarcascades + 'cars.xml'),
    "bus": cv2.CascadeClassifier(cv2.data.haarcascades + 'Bus_front.xml'),
    "bike": cv2.CascadeClassifier(cv2.data.haarcascades + 'two_wheeler.xml'),
    "face": cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'),
    "smile": cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml'),
    "plate": cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml'),
    "ped": cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
}

# Initialize speech recognition
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak out text
def say(text):
    engine.say(text)
    engine.runAndWait()

# Function to reload settings from file
def reload_config():
    global dataset
    dataset = read(filepath)

# Function to handle settings changes
def settings(query):
    reload_config()
    temp = query
    current_volume = float(dataset["volume"])
    current_rate = int(dataset["speech-rate"])
    current_gender = int(dataset["gender"])

    if query == "raise the volume":
        if current_volume >= 1.0:
            say("Volume is already at maximum.")
        else:
            current_volume += 0.3
            modify(filepath, "volume", str(current_volume))
            say("Volume has increased by 30%.")
    elif query == "lower the volume":
        if current_volume <= 0.3:
            say("Volume is already at minimum.")
        else:
            current_volume -= 0.3
            modify(filepath, "volume", str(current_volume))
            say("Volume has decreased by 30%.")
    elif query == "raise the speech rate":
        if current_rate >= 180:
            say("Speech rate is at maximum!")
        else:
            current_rate += 20
            modify(filepath, "speech-rate", str(current_rate))
            say("Speech rate has increased by 20 percent")
    elif query == "lower the speech rate":
        if current_rate <= 60:
            say("Speech rate is at minimum")
        else:
            current_rate -= 20
            modify(filepath, "speech-rate", str(current_rate))
            say("Speech rate has decreased by 20 percent")
    elif query == "change voice":
        if current_gender == 1:
            current_gender = 0
            modify(filepath, "gender", str(current_gender))
            say("Hi, I'm your new voice.")
        else:
            current_gender = 1
            modify(filepath, "gender", str(current_gender))
            say("Hi, I'm your new voice.")
    else:
        pass

def cv(query, queue=None):
    result_cascades = queue.get()
    current_time = datetime.now()
    a = current_time.strftime("%Y-%m-%d %H:%M:%S")
    cars = result_cascades["cars"]
    bikes = result_cascades["bikes"]
    buses = result_cascades["buses"]
    peds = result_cascades["peds"]
    faces = result_cascades["faces"]
    smiles = result_cascades["smiles"]

    response = ""

    if query in ["what's around me", "what do you see"]:
        response = "I see"
        if cars > 0:
            response += f" {cars} cars,"
        if bikes > 0:
            response += f" {bikes} motorbikes,"
        if buses > 0:
            response += f" {buses} buses,"
        if peds > 0:
            response += f" {peds} pedestrians,"
        if faces > 0:
            response += f" {faces} faces,"
        if smiles > 0:
            response += f" and {smiles} smiles."
        if response == "I see":
            response += " nothing of interest around me."
        else:
            response = response.rstrip(',') + " around me."
    elif query in ["whats the time", "tell me the time", "time now"]:
        response = a
    elif query == "How many cars are there":
        response = f"I detect {cars} cars nearby."

    elif query == "How many motorbikes are there":
        response = f"I detect {bikes} motorbikes nearby."

    elif query == "How many buses are there":
        response = f"I detect {buses} buses nearby."

    elif query == "How many pedestrians are there":
        response = f"I detect {peds} pedestrians nearby."

    elif query == "How many faces are there":
        response = f"I detect {faces} faces nearby."

    elif query == "How many smiles are there":
        response = f"I detect {smiles} smiles nearby."

    else:
        response = "Sorry, I didn't understand that."

    say(response)

# Function to listen for voice commands
def voice(queue=None):
    while True:
        try:
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

            print("Recognizing...")
            text = recognizer.recognize_google(audio).lower().strip("?!.,;:'''")
            print("You said:", text)

            settings(text)
            if queue is not None:
                cv(text , queue)
            else:
                cv(text)
            res = conversation(text)
            say(res)

        except sr.UnknownValueError:
            say("Sorry, could not understand audio.")
        except sr.RequestError as e:
            say(f"Could not request results: {e}")

# Function to draw rectangles and labels on the image
def put(img, x, y, w, h, color, thick, text):
    cv2.rectangle(img, (x, y), (x+w, y+h), color, thick)
    cv2.putText(img, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

# Function to check if two rectangles are colliding
def is_colliding(rect1, rect2):
    if len(rect1) < 4 or len(rect2) < 4:
        return False
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    if (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2) or \
            (x2 < x1 + w1 and x2 + w2 > x1 and y2 < y1 + h1 and y2 + h2 > y1):
        return True
    else:
        return False
 

# Function to check if rect1 is within rect2
def check(rect1, rect2):
    if len(rect1) < 4 or len(rect2) < 4:
        return False
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    if x1 >= x2 and y1 >= y2 and x1 + w1 <= x2 + w2 and y1 + h1 <= y2 + h2:
        print("true")
        return True
    else:
        print("false")
        return False

# Main loop for video capture and face detection
def main_loop(queue=None):
    url = input("enter stream url:")
    cap = cv2.VideoCapture(url)

    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        global result_cascades
        result_cascades = {
            "faces": 0,
            "smiles": 0,
            "plates": 0,
            "cars": 0,
            "bikes": 0,
            "buses": 0,
            "peds": 0,
        }

        faces = cascades["face"].detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        smiles = cascades["smile"].detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        plates = cascades["plate"].detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        cars = cascades["car"].detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        bikes = cascades["bike"].detectMultiScale(gray, 1.08, 2, minSize=(30, 30))
        buses = cascades["bus"].detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        peds = cascades["ped"].detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

        if faces is not None:
            for (x, y, w, h) in faces:
                result_cascades["faces"] += 1
                put(img, x, y, w, h, (147, 20, 255), 2, "face")  # Red for faces in BGR
                if smiles is not None:
                    for (x1, y1, w1, h1) in smiles:
                        if check((x1, y1, w1, h1), (x, y, w, h)):
                            put(img, x1, y1, w1, h1, (150, 50, 0), 2, "smile")  # Custom color for smiles
                            result_cascades["smiles"] += 1
                            if result_cascades["smiles"] > result_cascades["faces"]:
                                result_cascades["smiles"] = result_cascades["faces"]

        if bikes is not None:
            for (xb, yb, wb, hb) in bikes:
                if faces is not None and len(faces) > 0:
                    for (x, y, w, h) in faces:
                        if not check((xb, yb, wb, hb), (x, y, w, h)):
                            put(img, xb, yb, wb, hb, (0, 0, 255), 2, "Vehicle")  # Red for vehicles in BGR
                            result_cascades["bikes"] += 1
                else:
                    put(img, xb, yb, wb, hb, (0, 0, 255), 2, "Vehicle")
                    result_cascades["bikes"] += 1

        if peds is not None:
            for (xp, yp, wp, hp) in peds:
                if faces is not None and len(faces) > 0:
                    for (x, y, w, h) in faces:
                        if not check((xp, yp, wp, hp), (x, y, w, h)):
                            put(img, xp, yp, wp, hp, (0, 0, 100), 2, "Pedestrian")  # Red for pedestrians in BGR
                            result_cascades["peds"] += 1
                else:
                    put(img, xp, yp, wp, hp, (0, 0, 100), 2, "Pedestrian")
                    result_cascades["peds"] += 1

        if cars is not None:
            for (xc, yc, wc, hc) in cars:
                if faces is not None and len(faces) > 0:
                    for (x, y, w, h) in faces:
                        if not check((xc, yc, wc, hc), (x, y, w, h)) and not is_colliding((xc, yc, wc, hc), (x, y, w, h)):
                            put(img, xc, yc, wc, hc, (0, 0, 255), 2, "Car")
                            result_cascades["cars"] += 1
                else:
                    put(img, xc, yc, wc, hc, (0, 0, 255), 2, "Car")
                    result_cascades["cars"] += 1

        if buses is not None:
            for (xbu, ybu, wbu, hbu) in buses:
                if faces is not None and len(faces) > 0:
                    for (x, y, w, h) in faces:
                        if not check((xbu, ybu, wbu, hbu), (x, y, w, h)) and not is_colliding((xbu, ybu, wbu, hbu), (x, y, w, h)):
                            put(img, xbu, ybu, wbu, hbu, (0, 0, 255), 2, "Bus")
                            result_cascades["buses"] += 1
                else:
                    put(img, xbu, ybu, wbu, hbu, (0, 0, 255), 2, "Bus")
                    result_cascades["buses"] += 1

        if plates is not None:
            for (xp, yp, wp, hp) in plates:
                if faces is not None and len(faces) > 0:
                    for (x, y, w, h) in faces:
                        if not check((xp, yp, wp, hp), (x, y, w, h)) and not is_colliding((xp, yp, wp, hp), (x, y, w, h)):
                            put(img, xp, yp, wp, hp, (0, 255, 255), 2, "Plate")
                            result_cascades["plates"] += 1

        cv2.imshow('Face Detection', img)
        queue.put(result_cascades)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    # Start voice and main loop processes
    voice_p = multiprocessing.Process(target=voice, args=(queue,))
    main_p = multiprocessing.Process(target=main_loop, args=(queue,))

    voice_p.start()
    main_p.start()

    voice_p.join()
    main_p.join()
