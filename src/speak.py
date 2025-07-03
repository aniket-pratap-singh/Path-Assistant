import pyttsx3

engine = pyttsx3.init()
last_message = None

def speak(text):
    global last_message
    if text != last_message:
        engine.say(text)
        engine.runAndWait()  # Still blocking
        last_message = text
