import pyttsx3

def init_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'english (great britain)' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    return engine

engine = init_engine()

def speak(text):
    global engine
    print("Jarvis:", text)
    try:
        engine.say(str(text))
        engine.runAndWait()
    except Exception:
        try:
            engine = init_engine()
            engine.say(str(text))
            engine.runAndWait()
        except Exception as e:
            print("Speak error:", e)
