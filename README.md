# Jarvis AI — Desktop Voice Assistant

A fully offline AI-powered voice assistant for Ubuntu Linux.
Every command goes through a local LLM (Ollama) — no hardcoded rules, no internet required.

---

## Project Structure

```
vioce.ai/
├── frontend/
│   ├── index.html        # UI structure
│   ├── script.js         # Frontend logic
│   └── style.css         # UI styling
├── ai_fallback.py        # LLM brain — Ollama integration + action executor
├── app_launcher.py       # Smart app detection, fuzzy matching, WhatsApp automation
├── browser.py            # Browser & website control
├── commands.py           # Command router (passes all commands to LLM)
├── desktop_app.py        # PyWebView desktop window
├── main.py               # CLI voice loop entry point
├── server.py             # Flask API server
├── speak.py              # Text-to-speech (pyttsx3)
├── system_control.py     # Volume, brightness, screenshot, system info
├── voice.py              # Speech recognition (Google STT)
├── requirements.txt      # Python dependencies
└── README.md
```

---

## Languages Used

| Language   | Purpose                              |
|------------|--------------------------------------|
| Python     | Backend, AI, Voice, System Control   |
| JavaScript | Frontend logic                       |
| HTML       | UI structure                         |
| CSS        | UI styling                           |

---

## System Requirements

| Component | Minimum         |
|-----------|-----------------|
| CPU       | Core i5 6th Gen |
| RAM       | 8 GB            |
| OS        | Ubuntu 20.04+   |
| Python    | 3.10+           |
| Storage   | 2 GB free       |

---

## Setup

### Step 1 — System dependencies

```bash
sudo apt install portaudio19-dev xdotool wmctrl gnome-screenshot
```

### Step 2 — Create and activate virtual environment

```bash
cd /home/zain/Documents/vioce.ai
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3 — Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4 — Run the app

```bash
# Desktop app (PyWebView window)
python3 desktop_app.py

# Or CLI voice mode
python3 main.py
```

---

## Ollama — Local LLM Setup

Ollama runs AI models locally. No internet needed after initial setup.

### Step 1 — Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 2 — Start Ollama service

```bash
ollama serve
```

> Runs on: `http://localhost:11434`

### Step 3 — Pull the model

```bash
ollama pull qwen2.5-coder:0.5b
```

### Model Details

| Property     | Value                   |
|--------------|-------------------------|
| Model Name   | qwen2.5-coder:0.5b      |
| Provider     | Alibaba Cloud (Qwen)    |
| Size         | ~400 MB                 |
| RAM Required | ~1 GB                   |
| Speed        | Fast on i5 6th Gen      |
| Purpose      | Voice command → JSON    |
| API Port     | 11434                   |
| Runs Offline | Yes                     |

### Step 4 — Verify model

```bash
ollama run qwen2.5-coder:0.5b "say hello"
```

---

## How It Works

Every voice command goes directly to the LLM. No hardcoded matching.

```
User speaks / types command
           │
           ▼
     commands.py
           │
           ▼
     ai_fallback.py
           │
           ▼
  Ollama (qwen2.5-coder:0.5b)
           │
           ▼
  Returns structured JSON:
  {
    "reply":  "Opening PyCharm",
    "action": "open_app",
    "target": "pycharm"
  }
           │
      ┌────┴────┐
      ▼         ▼
  speak(reply)  _execute_action(action, target)
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
    app_launcher   browser   system_control
```

---

## Supported Languages

| Language    | Example Command                        |
|-------------|----------------------------------------|
| English     | open pycharm                           |
| Roman Urdu  | pycharm kholo / battery kitni hai      |
| Urdu/Hindi  | ٹرمینل کھولو                           |
| Mixed       | chrome open karo / volume up kar do    |

Jarvis replies in the **same language** as the input.

---

## All Supported Actions

### Apps
| Action       | Example                        |
|--------------|--------------------------------|
| `open_app`   | open pycharm / chrome kholo    |
| `close_app`  | close vlc                      |

### Terminal
| Action          | Example                        |
|-----------------|--------------------------------|
| `open_terminal` | open terminal / terminal kholo |
| `run_terminal`  | run python main.py             |

### Folders
| Action        | Example                          |
|---------------|----------------------------------|
| `open_folder` | open downloads / documents kholo |

Supported folders: `downloads`, `documents`, `desktop`, `pictures`, `videos`, `music`, `home`

### Files
| Action      | Example                         |
|-------------|---------------------------------|
| `open_file` | open report.pdf / open test.py  |
| `find_file` | find resume / invoice dhoondo   |

`find_file` searches: Documents, Downloads, Desktop, Pictures, Videos, Music

### Browser & Search
| Action          | Example                        |
|-----------------|--------------------------------|
| `open_website`  | open github / open gmail       |
| `google_search` | search flask tutorial          |
| `youtube_play`  | play arijit singh songs        |

### WhatsApp
| Action              | Example                                      |
|---------------------|----------------------------------------------|
| `whatsapp_open`     | open whatsapp                                |
| `whatsapp_message`  | send message to Ahmad saying Hello bhai      |

### Volume & Brightness
| Action            | Example             |
|-------------------|---------------------|
| `volume_up`       | volume up           |
| `volume_down`     | volume down         |
| `mute`            | mute                |
| `set_volume`      | set volume to 60    |
| `brightness_up`   | brightness up       |
| `brightness_down` | brightness down     |

### System Info
| Action        | Example              |
|---------------|----------------------|
| `get_battery` | check battery        |
| `get_time`    | what is the time     |
| `get_date`    | what is today's date |
| `get_ram`     | check ram            |
| `get_cpu`     | check cpu            |
| `get_wifi`    | wifi status          |
| `get_ip`      | what is my ip        |
| `get_disk`    | check disk space     |

### Screen & Windows
| Action         | Example           |
|----------------|-------------------|
| `screenshot`   | take screenshot   |
| `minimize`     | minimize window   |
| `maximize`     | maximize window   |
| `close_window` | close window      |
| `new_tab`      | new tab           |
| `close_tab`    | close tab         |
| `scroll_up`    | scroll up         |
| `scroll_down`  | scroll down       |
| `go_back`      | go back           |
| `go_forward`   | go forward        |
| `refresh`      | refresh page      |

### Keyboard
| Action       | Example      |
|--------------|--------------|
| `copy`       | copy         |
| `paste`      | paste        |
| `cut`        | cut          |
| `undo`       | undo         |
| `redo`       | redo         |
| `select_all` | select all   |
| `save`       | save file    |
| `type_text`  | type hello   |

### System Control
| Action        | Example        |
|---------------|----------------|
| `lock_screen` | lock screen    |
| `sleep`       | sleep          |
| `shutdown`    | shutdown       |
| `restart`     | restart        |
| `empty_trash` | empty trash    |

---

## Test Commands

### English
```
open pycharm
open terminal
open downloads
open documents
open desktop
find resume
find invoice.pdf
open report.pdf
take screenshot
check battery
check ram
volume up
brightness down
play lofi beats
search python tutorial
open github
open whatsapp
what is the time
lock screen
```

### Roman Urdu / Mixed
```
pycharm kholo
terminal kholo
downloads kholo
documents kholo
resume dhoondo
battery kitni hai
volume up karo
screenshot lo
chrome open karo
time batao
```

---

## Dependencies

```
SpeechRecognition    — voice input
pyttsx3              — text-to-speech
PyAudio              — microphone access
flask                — web server
flask-cors           — CORS for frontend
pywebview            — desktop window
thefuzz[speedup]     — fuzzy app name matching
requests             — Ollama API calls
```

---

## Troubleshooting

| Problem                        | Solution                                              |
|--------------------------------|-------------------------------------------------------|
| `No module named 'webview'`    | `pip install pywebview`                               |
| `Port 5000 already in use`     | Auto-detected, a free port is used automatically      |
| `Ollama not running`           | Run `ollama serve` in terminal                        |
| `Model not found`              | Run `ollama pull qwen2.5-coder:0.5b`                  |
| `Microphone not working`       | Check `pavucontrol` audio settings                    |
| `PyAudio install fails`        | `sudo apt install portaudio19-dev && pip install PyAudio` |
| `xdotool not found`            | `sudo apt install xdotool`                            |
| `wmctrl not found`             | `sudo apt install wmctrl`                             |
| `Screenshot is black`          | `sudo apt install gnome-screenshot`                   |
| `App falsely shown as running` | Fixed — now requires both process + visible window    |
| `UI shows "Done." always`      | Fixed — LLM reply is now captured and displayed       |

---

## Author

**Zain** — Jarvis AI Project
