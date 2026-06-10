import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 200
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 0.8

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                return ""

        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text.lower()

    except sr.UnknownValueError:
        print("Could not understand, try again")
        return ""
    except sr.RequestError as e:
        print("Network error:", e)
        return ""
    except Exception as e:
        print("Listen error:", e)
        return ""
