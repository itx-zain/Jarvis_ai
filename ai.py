"""
ai.py — Local LLM chat using Ollama (qwen2.5-coder:0.5b)
OpenAI removed — fully offline now.
"""

from speak import speak
from ai_fallback import execute_llm_action

def ai_chat(command: str) -> None:
    if not command:
        return

    if any(w in command for w in ["hello", "hi", "hey"]):
        speak("Hello Zain! How can I help you?")
        return

    if "how are you" in command:
        speak("I am great, always ready to help!")
        return

    if any(w in command for w in ["your name", "who are you"]):
        speak("I am Jarvis, your personal AI assistant.")
        return

    if any(w in command for w in ["what can you do", "help"]):
        speak("I can open apps, search Google and YouTube, control volume, check battery, RAM, CPU, WiFi, and much more.")
        return

    # Use local LLM fallback
    success = execute_llm_action(command)
    if not success:
        speak("Sorry Zain, I could not understand that command.")
