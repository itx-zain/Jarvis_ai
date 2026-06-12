"""
ai_fallback.py — Jarvis LLM Brain (Multi-Language Support)
Model: qwen2.5-coder:0.5b
Flow: Voice → Ollama → {reply, action, target} → Speak + Execute
"""

import json
import re
import os
import subprocess
import time
import requests
import speak as _speak_module
import system_control as sc
import browser as br
import weather
from app_launcher import smart_open, open_website, whatsapp_send_message
from action_registry import build_system_prompt, detect_intent_group


# ─── MULTI-COMMAND PARSER ───
_MULTI_SEPARATORS = [" and ", " then ", " also ", " phir ", " aur ", " fir ", ", "]


def parse_multi_command(command: str) -> list:
    """
    Split a command into multiple sub-commands based on separators.
    
    Examples:
        "open youtube and take screenshot" → ["open youtube", "take screenshot"]
        "open downloads aur open documents" → ["open downloads", "open documents"]
    """
    if not command or len(command.strip()) < 2:
        return [command]

    parts = [command]
    for sep in _MULTI_SEPARATORS:
        new_parts = []
        for part in parts:
            new_parts.extend([p.strip() for p in part.split(sep) if p.strip()])
        if len(new_parts) > len(parts):
            parts = new_parts
    
    # Filter out empty/invalid parts
    parts = [p for p in parts if p and len(p.strip()) > 1]
    return parts

def speak(text):
    """Proxy so server.py can patch _speak_module.speak at runtime."""
    _speak_module.speak(text)

# ─── CONFIG ───
OLLAMA_URL      = "http://localhost:11434/api/generate"
OLLAMA_MODEL    = "qwen2.5-coder:0.5b"
REQUEST_TIMEOUT = 30

# ─── PROJECT CONFIG ───
PROJECT_NAME = "voice.ai"
PROJECT_PATH = "/home/zain/Documents/vioce.ai"

# ─── APP MEMORY ───
LAST_OPENED_APP = ""

# ─── ACTION ALIASES ─── (normalize LLM synonyms before _execute_action)
ACTION_ALIASES = {
    # Terminal open variants
    "terminal_open":        "open_terminal",
    # Terminal close variants
    "close_terminal":       "close_terminal",   # handled natively
    "terminal_close":       "close_terminal",
    "kill_terminal":        "close_terminal",
    # Folder variants
    "open_directory":       "open_folder",
    "open_dir":             "open_folder",
    "open_folder_path":     "open_folder",
    # File search variants
    "search_file":          "find_file",
    "search_files":         "find_file",
    "file_search":          "find_file",
    # Window close variants
    "close_current_window": "close_window",
    "close_active_window":  "close_window",
    "window_close":         "close_window",
    # App close variants
    "kill_app":             "close_app",
    "force_close":          "close_app",
    # Misc
    "play_youtube":         "youtube_play",
    "search_google":        "google_search",
    "google":               "google_search",
}

# ─── OLLAMA ───
def _call_ollama(command: str) -> dict:
    group = detect_intent_group(command)
    prompt = build_system_prompt(group)
    print(f"[INTENT] {group}")
    print(f"[PROMPT TOKENS] ~{len(prompt.split())}")

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{prompt}\n\nInput: {command}\nOutput:",
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 150, "top_p": 0.9},
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        raw = r.json().get("response", "").strip()
        if not raw:
            return {"reply": "Sorry, no response from LLM", "action": "chat", "target": ""}
        json_match = re.search(r'\{.*?\}', raw, re.DOTALL)
        if not json_match:
            return {"reply": "Could not parse response", "action": "chat", "target": ""}
        result = json.loads(json_match.group())
        result.setdefault("reply", "Done")
        result.setdefault("action", "chat")
        result.setdefault("target", "")
        print(f"[ACTION] {result['action']}")
        return result
    except requests.exceptions.ConnectionError:
        return {"reply": "Ollama not running. Please start with: ollama serve", "action": "chat", "target": ""}
    except requests.exceptions.Timeout:
        return {"reply": "Request timed out", "action": "chat", "target": ""}
    except (json.JSONDecodeError, ValueError):
        return {"reply": "Invalid response format", "action": "chat", "target": ""}
    except requests.exceptions.RequestException as e:
        return {"reply": f"Network error: {e}", "action": "chat", "target": ""}


# ─── HELPERS ───
_FOLDER_MAP = {
    "downloads": "~/Downloads",
    "documents": "~/Documents",
    "pictures":  "~/Pictures",
    "videos":    "~/Videos",
    "music":     "~/Music",
    "desktop":   "~/Desktop",
    "home":      "~",
}

_SEARCH_DIRS = [
    "~/Documents", "~/Downloads", "~/Desktop",
    "~/Pictures", "~/Videos", "~/Music",
]

def _close_app(target: str) -> str:
    """Close app by friendly name using process map."""
    if not target:
        return "No app specified"
    sc.close_app(target)
    return f"Closed {target}"


def _close_terminal() -> str:
    """Terminate all running terminal emulator processes."""
    for proc in ["gnome-terminal", "x-terminal-emulator", "xterm", "konsole", "tilix", "terminator"]:
        subprocess.run(["pkill", "-TERM", "-f", proc],
                       capture_output=True)
    return "Terminal closed"


def _close_last_app() -> str:
    """Close the last app opened via open_app."""
    global LAST_OPENED_APP
    if not LAST_OPENED_APP:
        return "No recently opened app to close"
    sc.close_app(LAST_OPENED_APP)
    name = LAST_OPENED_APP
    LAST_OPENED_APP = ""
    return f"Closed {name}"


def _open_folder(target: str) -> str:
    path = os.path.expanduser(_FOLDER_MAP.get(target.lower(), target))
    if os.path.exists(path):
        subprocess.Popen(["xdg-open", path])
        return f"Opened {target} folder"
    return f"Folder '{target}' not found"


def _find_file(query: str) -> str:
    """Search common user dirs for a file matching query, open first match."""
    dirs = [os.path.expanduser(d) for d in _SEARCH_DIRS]
    results = []
    for d in dirs:
        if not os.path.isdir(d):
            continue
        r = subprocess.run(
            ["find", d, "-iname", f"*{query}*", "-maxdepth", "4"],
            capture_output=True, text=True, timeout=10
        )
        results.extend([l for l in r.stdout.splitlines() if l.strip()])
        if len(results) >= 5:
            break

    if not results:
        return f"File '{query}' not found"

    first = results[0]
    subprocess.Popen(["xdg-open", first])
    if len(results) == 1:
        return f"Found and opened: {first}"
    others = "\n".join(results[1:5])
    return f"Found and opened: {first}\nOther matches:\n{others}"


def _open_file(target: str) -> str:
    """Open a file by name — search if not an absolute path."""
    expanded = os.path.expanduser(target)
    if os.path.exists(expanded):
        subprocess.Popen(["xdg-open", expanded])
        return f"Opening {os.path.basename(target)}"
    # Search for it
    return _find_file(target)


def _run_terminal(target: str = "") -> str:
    if target:
        subprocess.Popen(
            ["gnome-terminal", "--", "bash", "-c", f"{target}; exec bash"]
        )
        return f"Running: {target}"
    subprocess.Popen(["gnome-terminal"])
    return "Terminal opened"


def _type_text(target: str) -> str:
    if target:
        os.system(f'xdotool type --clearmodifiers "{target}"')
        return f"Typed: {target}"
    return "No text provided"


# ─── PROJECT HELPERS ───
def _open_project() -> str:
    if os.path.isdir(PROJECT_PATH):
        subprocess.Popen(["nautilus", PROJECT_PATH])
        return f"Project opened: {PROJECT_PATH}"
    return f"Project path not found: {PROJECT_PATH}"


def _list_project_files() -> str:
    if not os.path.isdir(PROJECT_PATH):
        return f"Project path not found: {PROJECT_PATH}"
    files = sorted(
        f for f in os.listdir(PROJECT_PATH)
        if os.path.isfile(os.path.join(PROJECT_PATH, f))
    )
    total = len(files)
    shown = files[:50]
    listing = "\n".join(shown)
    suffix = f"\n... and {total - 50} more" if total > 50 else ""
    return f"Project: {PROJECT_NAME} — {total} files\n{listing}{suffix}"


def _open_project_file(target: str) -> str:
    # Walk project dir for a case-insensitive match
    for root, _, files in os.walk(PROJECT_PATH):
        for f in files:
            if f.lower() == target.lower() or target.lower() in f.lower():
                full = os.path.join(root, f)
                # Prefer VS Code, fallback to xdg-open
                editor = subprocess.getoutput("which code").strip()
                if editor:
                    subprocess.Popen([editor, full])
                else:
                    subprocess.Popen(["xdg-open", full])
                return f"Opening {f}"
    return f"File '{target}' not found in project"


def _run_project_file(target: str) -> str:
    for root, _, files in os.walk(PROJECT_PATH):
        for f in files:
            if f.lower() == target.lower():
                full = os.path.join(root, f)
                subprocess.Popen(
                    ["gnome-terminal", "--", "bash", "-c",
                     f"cd {PROJECT_PATH} && python3 {full}; exec bash"]
                )
                return f"Running {f}"
    return f"File '{target}' not found in project"


def _search_project(query: str) -> str:
    if not os.path.isdir(PROJECT_PATH):
        return f"Project path not found: {PROJECT_PATH}"
    # Support glob patterns like *.py
    name_pattern = query if query.startswith("*") else f"*{query}*"
    r = subprocess.run(
        ["find", PROJECT_PATH, "-iname", name_pattern, "-maxdepth", "4"],
        capture_output=True, text=True, timeout=10
    )
    results = [l.replace(PROJECT_PATH + "/", "") for l in r.stdout.splitlines() if l.strip()]
    if not results:
        return f"No files matching '{query}' found in project"
    return f"Found {len(results)} file(s):\n" + "\n".join(results[:20])


def _project_status() -> str:
    if not os.path.isdir(PROJECT_PATH):
        return f"Project path not found: {PROJECT_PATH}"
    all_files = [
        f for f in os.listdir(PROJECT_PATH)
        if os.path.isfile(os.path.join(PROJECT_PATH, f))
    ]
    py_files = [f for f in all_files if f.endswith(".py")]
    return (
        f"Project: {PROJECT_NAME}\n"
        f"Path: {PROJECT_PATH}\n"
        f"Files: {len(all_files)}\n"
        f"Python Files: {len(py_files)}"
    )


# ─── ACTION EXECUTOR ───
def _execute_action(action: str, target: str) -> str:
    # Normalize action through alias table first
    original_action = action
    action = ACTION_ALIASES.get(action, action)
    if action != original_action:
        print(f"[ALIAS] Original Action: {original_action} -> Normalized Action: {action}")

    # ── Apps ──
    if action == "open_app":
        global LAST_OPENED_APP
        result = smart_open(target)
        # Track last opened app on success
        if result and "not found" not in result.lower():
            LAST_OPENED_APP = target
        return result
    if action == "close_app":
        return _close_app(target)
    if action == "close_last_app":
        return _close_last_app()

    # ── Terminal ──
    if action in ("open_terminal", "run_terminal"):
        return _run_terminal(target)
    if action == "close_terminal":
        return _close_terminal()

    # ── Folders (Task 2) ──
    if action == "open_folder":
        return _open_folder(target)

    # ── Files (Task 3 & 4) ──
    if action == "find_file":
        return _find_file(target)
    if action == "open_file":
        return _open_file(target)

    # ── Websites ──
    if action == "open_website":
        return open_website(target)

    # ── Search ──
    if action == "google_search":
        br.google_search(target)
        return f"Searching {target} on Google"
    if action == "youtube_play":
        br.youtube_search_and_play(target)
        return f"Playing {target} on YouTube"

    # ── WhatsApp ──
    if action == "whatsapp_open":
        br.whatsapp_open()
        return "Opening WhatsApp"
    if action == "whatsapp_message":
        if ":" in target:
            contact, message = target.split(":", 1)
            return whatsapp_send_message(contact.strip(), message.strip())
        return "Invalid WhatsApp message format"

    # ── Volume ──
    if action == "volume_up":
        sc.volume_up();   return "Volume increased"
    if action == "volume_down":
        sc.volume_down(); return "Volume decreased"
    if action == "mute":
        sc.mute();        return "Audio muted/unmuted"
    if action == "set_volume":
        level = int(target) if target.isdigit() else 50
        sc.set_volume(level)
        return f"Volume set to {level}%"

    # ── Brightness ──
    if action == "brightness_up":
        return f"Brightness: {int(sc.increase_brightness() * 100)}%"
    if action == "brightness_down":
        return f"Brightness: {int(sc.decrease_brightness() * 100)}%"

    # ── System Info ──
    if action == "get_battery": return sc.get_battery()
    if action == "get_time":    return sc.get_time()
    if action == "get_date":    return sc.get_date()
    if action == "get_ram":     return sc.get_ram()
    if action == "get_cpu":     return f"CPU usage: {sc.get_cpu()}"
    if action == "get_wifi":    return sc.get_wifi()
    if action == "get_ip":      return sc.get_ip()
    if action == "get_disk":    return sc.get_disk()

    # ── Weather ──
    if action == "weather":
        result = weather.get_weather(target)
        return result

    # ── Screen & Windows ──
    if action == "screenshot":
        fname = sc.screenshot()
        return f"Screenshot saved: {fname}"
    if action == "minimize":     sc.minimize_window(); return "Window minimized"
    if action == "maximize":     sc.maximize_window(); return "Window maximized"
    if action == "close_window": sc.close_window();    return "Window closed"
    if action == "new_tab":      sc.new_tab();         return "New tab opened"
    if action == "close_tab":    sc.close_tab();       return "Tab closed"
    if action == "scroll_up":    sc.scroll_up();       return "Scrolled up"
    if action == "scroll_down":  sc.scroll_down();     return "Scrolled down"
    if action == "go_back":      sc.go_back();         return "Going back"
    if action == "go_forward":   sc.go_forward();      return "Going forward"
    if action == "refresh":      sc.refresh_page();    return "Page refreshed"

    # ── Keyboard ──
    if action == "copy":       sc.copy();       return "Copied"
    if action == "paste":      sc.paste();      return "Pasted"
    if action == "cut":        sc.cut();        return "Cut"
    if action == "undo":       sc.undo();       return "Undo"
    if action == "redo":       sc.redo();       return "Redo"
    if action == "select_all": sc.select_all(); return "Selected all"
    if action == "save":       sc.save_file();  return "Saved"

    # ── System Control ──
    if action == "lock_screen":  sc.lock_screen(); return "Screen locked"
    if action == "sleep":        sc.sleep_pc();    return "Going to sleep"
    if action == "shutdown":     sc.shutdown_pc(); return "Shutting down"
    if action == "restart":      sc.restart_pc();  return "Restarting"
    if action == "empty_trash":  sc.empty_trash(); return "Trash emptied"

    # ── Text ──
    if action == "type_text":
        return _type_text(target)

    # ── Project ──
    if action == "open_project":       return _open_project()
    if action == "list_project_files": return _list_project_files()
    if action == "open_project_file":  return _open_project_file(target)
    if action == "run_project_file":   return _run_project_file(target)
    if action == "search_project":     return _search_project(target)
    if action == "project_status":     return _project_status()

    # ── Chat ──
    if action == "chat":
        return ""

    print(f"[UNKNOWN] Original Action: {original_action} | Normalized Action: {action}")
    return f"Unknown action: {action}"


# ─── MAIN ENTRY POINT ───
def _process_single_command(command: str) -> str:
    """Process a single command through Ollama and return the action result."""
    llm_response = _call_ollama(command)
    reply = llm_response.get("reply", "Done")
    action = llm_response.get("action", "")
    target = llm_response.get("target", "")
    speak(reply)
    if action and action != "chat":
        try:
            result = _execute_action(action, target)
            if result and result.lower() != reply.lower():
                speak(result)
            return result or reply
        except Exception as e:
            print(f"Action execution error: {e}")
            speak("Sorry, I could not complete that action.")
            return "Error"
    return reply


def execute_llm_action(command: str) -> bool:
    # Check for multi-command
    parts = parse_multi_command(command)
    
    if len(parts) > 1:
        print(f"[MULTI COMMAND DETECTED]")
        for i, part in enumerate(parts, 1):
            print(f"Part {i}: {part}")
        
        all_replies = []
        for i, part in enumerate(parts, 1):
            print(f"[ACTION {i}] Processing: {part}")
            result = _process_single_command(part)
            all_replies.append(result)
            if i < len(parts):
                time.sleep(1)  # Delay between actions
        
        print(f"[MULTI COMMAND COMPLETED] {len(parts)} actions executed")
        return True
    
    # Single command - original behavior
    _process_single_command(command)
    return True
