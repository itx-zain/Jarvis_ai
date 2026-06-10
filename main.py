from voice import listen
from commands import execute_command
from speak import speak

WAKE_WORD = "jarvis"

speak("Jarvis is online. Say Jarvis to wake me up.")

while True:
    try:
        command = listen()

        if not command:
            continue

        # Wake word check
        if WAKE_WORD not in command:
            continue

        # Wake word hata kar sirf command lo
        command = command.replace(WAKE_WORD, "").strip()

        if not command:
            speak("Yes Zain, how can I help you?")
            command = listen()
            if not command:
                continue

        if "exit" in command or "goodbye" in command or "bye" in command:
            speak("Goodbye Zain! Have a great day.")
            break

        execute_command(command)

    except KeyboardInterrupt:
        speak("Shutting down Jarvis. Goodbye!")
        break
    except Exception as e:
        print("Error:", e)
        continue
