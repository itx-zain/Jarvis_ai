#!/bin/bash
# Jarvis AI - PyInstaller Build Script
cd /home/zain/Documents/vioce.ai

pip install pyinstaller

pyinstaller \
  --onefile \
  --windowed \
  --name "JarvisAI" \
  --icon jarvis_icon.png \
  --add-data "frontend:frontend" \
  --add-data "server.py:." \
  --add-data "commands.py:." \
  --add-data "speak.py:." \
  --add-data "voice.py:." \
  --add-data "browser.py:." \
  --add-data "system_control.py:." \
  --add-data "ai.py:." \
  --hidden-import "webview" \
  --hidden-import "flask" \
  --hidden-import "flask_cors" \
  --hidden-import "speech_recognition" \
  --hidden-import "pyttsx3" \
  desktop_app.py

echo "Build complete! Binary is at: dist/JarvisAI"
