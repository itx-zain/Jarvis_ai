import os
import re
import time
import subprocess
import urllib.parse
from thefuzz import process

# ─── APP ALIASES ───
APP_ALIASES = {
    "vs code": "code", "vscode": "code", "visual studio code": "code",
    "chrome": "google-chrome", "google chrome": "google-chrome",
    "firefox": "firefox", "mozilla": "firefox",
    "telegram": "telegram-desktop",
    "discord": "discord",
    "vlc": "vlc", "media player": "vlc",
    "zoom": "zoom",
    "spotify": "spotify",
    "slack": "slack",
    "gimp": "gimp",
    "obs": "obs", "obs studio": "obs",
    "steam": "steam",
    "terminal": "gnome-terminal", "console": "gnome-terminal",
    "file manager": "nautilus", "files": "nautilus", "nautilus": "nautilus",
    "calculator": "gnome-calculator", "calc": "gnome-calculator",
    "settings": "gnome-control-center",
    "notepad": "gedit", "text editor": "gedit", "gedit": "gedit",
    "camera": "cheese",
    "rhythmbox": "rhythmbox",
    "calendar": "gnome-calendar",
    "postman": "postman",
    "android studio": "android-studio",
    "pycharm": "pycharm",
    "intellij": "idea",
    "whatsapp": "google-chrome --app=https://web.whatsapp.com",
    "skype": "skype",
    "libreoffice": "libreoffice",
    "libreoffice writer": "libreoffice --writer",
    "libreoffice calc": "libreoffice --calc",
    "blender": "blender",
    "inkscape": "inkscape",
    "kdenlive": "kdenlive",
    "virtualbox": "virtualbox",
    "dbeaver": "dbeaver",
    "mysql workbench": "mysql-workbench",
    "thunderbird": "thunderbird",
    "transmission": "transmission-gtk",
    "nautilus": "nautilus",
}

# ─── WEBSITE MAP ───
WEBSITE_MAP = {
    "youtube":       "https://www.youtube.com",
    "google":        "https://www.google.com",
    "chatgpt":       "https://chat.openai.com",
    "chat gpt":      "https://chat.openai.com",
    "facebook":      "https://www.facebook.com",
    "instagram":     "https://www.instagram.com",
    "github":        "https://www.github.com",
    "gmail":         "https://mail.google.com",
    "whatsapp web":  "https://web.whatsapp.com",
    "twitter":       "https://www.twitter.com",
    "x":             "https://www.twitter.com",
    "linkedin":      "https://www.linkedin.com",
    "netflix":       "https://www.netflix.com",
    "spotify":       "https://open.spotify.com",
    "reddit":        "https://www.reddit.com",
    "maps":          "https://maps.google.com",
    "google maps":   "https://maps.google.com",
    "zoom":          "https://zoom.us",
    "stackoverflow": "https://stackoverflow.com",
    "amazon":        "https://www.amazon.com",
    "wikipedia":     "https://www.wikipedia.org",
    "drive":         "https://drive.google.com",
    "google drive":  "https://drive.google.com",
    "meet":          "https://meet.google.com",
    "google meet":   "https://meet.google.com",
    "docs":          "https://docs.google.com",
    "sheets":        "https://sheets.google.com",
    "canva":         "https://www.canva.com",
    "notion":        "https://www.notion.so",
    "trello":        "https://www.trello.com",
}


# ─── DEEP SYSTEM APP SCAN ───
def get_installed_apps():
    apps = {}

    # 1. .desktop files — all locations including Flatpak & Snap
    desktop_dirs = [
        "/usr/share/applications",
        "/usr/local/share/applications",
        os.path.expanduser("~/.local/share/applications"),
        "/var/lib/flatpak/exports/share/applications",
        os.path.expanduser("~/.local/share/flatpak/exports/share/applications"),
        "/snap/bin",  # snap apps listed separately below
    ]
    for d in desktop_dirs:
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if not f.endswith(".desktop"):
                continue
            path = os.path.join(d, f)
            name, exec_cmd, no_display = None, None, False
            try:
                with open(path, "r", errors="ignore") as fp:
                    for line in fp:
                        line = line.strip()
                        if line.startswith("Name=") and name is None:
                            name = line[5:].strip().lower()
                        if line.startswith("Exec=") and exec_cmd is None:
                            raw = line[5:].strip()
                            # Remove field codes and flags
                            raw = re.sub(r'%[a-zA-Z]', '', raw).strip()
                            exec_cmd = raw
                        if line == "NoDisplay=true":
                            no_display = True
            except Exception:
                continue
            if name and exec_cmd and not no_display:
                apps[name] = exec_cmd

    # 2. Snap apps
    snap_bin = "/snap/bin"
    if os.path.isdir(snap_bin):
        for f in os.listdir(snap_bin):
            fp = os.path.join(snap_bin, f)
            if os.access(fp, os.X_OK):
                apps[f.lower()] = fp

    # 3. PATH executables (filtered — only real apps, not system tools)
    skip_prefixes = ("python", "perl", "ruby", "java", "gcc", "g++", "ld", "ar",
                     "nm", "as", "strip", "objdump", "objcopy", "ranlib", "size",
                     "sh", "bash", "zsh", "fish", "dash", "ksh", "csh", "tcsh",
                     "grep", "awk", "sed", "find", "sort", "uniq", "cut", "tr",
                     "ls", "cp", "mv", "rm", "mkdir", "chmod", "chown", "ln",
                     "cat", "echo", "printf", "test", "true", "false", "kill",
                     "ps", "top", "df", "du", "mount", "umount", "fsck", "mkfs",
                     "apt", "dpkg", "snap", "flatpak", "pip", "npm", "node",
                     "git", "svn", "make", "cmake", "ninja", "pkg-config")
    try:
        bins = subprocess.getoutput(
            "find /usr/bin /usr/local/bin ~/.local/bin /snap/bin -maxdepth 1 -executable -type f 2>/dev/null"
        ).splitlines()
        for b in bins:
            b = b.strip()
            bname = os.path.basename(b).lower()
            if bname and not any(bname.startswith(p) for p in skip_prefixes):
                if bname not in apps:
                    apps[bname] = b
    except Exception:
        pass

    return apps


_apps_cache = None

def _get_apps():
    global _apps_cache
    if _apps_cache is None:
        _apps_cache = get_installed_apps()
    return _apps_cache

def refresh_apps_cache():
    global _apps_cache
    _apps_cache = get_installed_apps()
    return len(_apps_cache)


# ─── RUNNING APP DETECTION ───
def is_app_running(app_name):
    """
    Returns (process_found, window_found).
    Both must be True to consider app truly visible/running.
    """
    app_name = app_name.lower().strip()
    process_map = {
        "chrome": "chrome", "google chrome": "chrome",
        "firefox": "firefox",
        "vs code": "code", "vscode": "code",
        "telegram": "telegram",
        "discord": "discord",
        "spotify": "spotify",
        "vlc": "vlc",
        "zoom": "zoom",
        "slack": "slack",
        "steam": "steam",
        "gimp": "gimp",
        "obs": "obs",
        "skype": "skype",
        "thunderbird": "thunderbird",
    }
    proc = process_map.get(app_name, app_name.split()[0])
    proc_result = subprocess.getoutput(f"pgrep -x '{proc}' 2>/dev/null || pgrep -f '{proc}' 2>/dev/null | head -1")
    process_found = bool(proc_result.strip())

    # Check for a visible window matching the app name
    win_out = subprocess.getoutput("wmctrl -l 2>/dev/null")
    window_found = any(app_name.split()[0] in line.lower() for line in win_out.splitlines())

    print(f"[APP] Process Found: {process_found} | Window Found: {window_found}")
    return process_found, window_found

def get_running_window_titles():
    """Get list of currently open window titles."""
    out = subprocess.getoutput("wmctrl -l 2>/dev/null | awk '{$1=$2=$3=\"\"; print $0}' | sed 's/^ *//'")
    return [line.strip() for line in out.splitlines() if line.strip()]


# ─── WHATSAPP AUTO MESSAGE ───
def whatsapp_send_message(contact_name, message=""):
    """
    Open WhatsApp Web and auto-search contact, type and send message.
    Uses xdotool to automate the interaction.
    """
    import urllib.parse

    if message:
        # Use wa.me deep link for direct message (works if WhatsApp is logged in via browser)
        encoded_msg = urllib.parse.quote(message)
        # Open WhatsApp Web search
        os.system(f'google-chrome "https://web.whatsapp.com" &')
        time.sleep(4)

        # Focus chrome window
        os.system("xdotool search --name 'WhatsApp' windowactivate --sync 2>/dev/null || "
                  "xdotool search --name 'Chrome' windowactivate --sync 2>/dev/null")
        time.sleep(1)

        # Click search box (Ctrl+Alt+/) and type contact name
        os.system("xdotool key ctrl+alt+slash 2>/dev/null")
        time.sleep(0.8)
        os.system(f'xdotool type --clearmodifiers "{contact_name}"')
        time.sleep(2)

        # Press Enter to open chat
        os.system("xdotool key Return")
        time.sleep(1.5)

        # Type the message
        os.system(f'xdotool type --clearmodifiers "{message}"')
        time.sleep(0.5)

        # Send message
        os.system("xdotool key Return")
        return f"Sent '{message}' to {contact_name} on WhatsApp"
    else:
        # Just open WhatsApp and search contact
        os.system(f'google-chrome "https://web.whatsapp.com" &')
        time.sleep(3)
        os.system("xdotool search --name 'WhatsApp' windowactivate --sync 2>/dev/null || "
                  "xdotool search --name 'Chrome' windowactivate --sync 2>/dev/null")
        time.sleep(0.8)
        os.system("xdotool key ctrl+alt+slash 2>/dev/null")
        time.sleep(0.8)
        os.system(f'xdotool type --clearmodifiers "{contact_name}"')
        return f"Opened WhatsApp and searched for {contact_name}"


# ─── CORE LAUNCHERS ───
def launch_app(query):
    """Fuzzy match query against installed apps and launch it."""
    query = query.lower().strip()
    apps = _get_apps()
    if not apps:
        return False, "No apps found on system"

    match, score = process.extractOne(query, apps.keys())
    if score >= 60:
        cmd = apps[match]
        process_found, window_found = is_app_running(match)
        if process_found and window_found:
            os.system(f"wmctrl -a '{match}' 2>/dev/null")
            print(f"[APP] Action: Bringing {match} to focus")
            return True, f"{match} is already open, bringing to focus"
        else:
            # Process exists but no visible window, or not running at all — launch
            print(f"[APP] Action: Launching {match}")
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True, f"Opening {match}"
    return False, f"App '{query}' not found"


def open_website(query):
    """Open a known website or fallback to Google search."""
    query = query.lower().strip()

    if query in WEBSITE_MAP:
        url = WEBSITE_MAP[query]
        subprocess.Popen(f'google-chrome "{url}"', shell=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Opening {query}"

    match, score = process.extractOne(query, WEBSITE_MAP.keys())
    if score >= 72:
        url = WEBSITE_MAP[match]
        subprocess.Popen(f'google-chrome "{url}"', shell=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Opening {match}"

    if re.match(r'^[\w\-]+\.(com|org|net|io|co|app|dev|ai|edu|gov)$', query):
        subprocess.Popen(f'google-chrome "https://{query}"', shell=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Opening {query}"

    encoded = urllib.parse.quote(query)
    subprocess.Popen(f'google-chrome "https://www.google.com/search?q={encoded}"',
                     shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return f"Searching {query} on Google"


def smart_open(query):
    """
    Smart open priority:
    1. Exact alias match
    2. Fuzzy alias match (>=82)
    3. Exact website match
    4. Fuzzy website match (>=75)
    5. Installed app fuzzy match (>=62)
    6. Google search fallback
    """
    query = query.lower().strip()
    if not query:
        return "Please specify what to open"

    # 1. Exact alias
    if query in APP_ALIASES:
        cmd = APP_ALIASES[query]
        process_found, window_found = is_app_running(query)
        if process_found and window_found:
            os.system(f"wmctrl -a '{query}' 2>/dev/null")
            print(f"[APP] Action: Bringing {query} to focus")
            return f"{query} is already open, bringing to focus"
        print(f"[APP] Action: Launching {query}")
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Opening {query}"

    # 2. Fuzzy alias
    alias_match, alias_score = process.extractOne(query, APP_ALIASES.keys())
    if alias_score >= 82:
        cmd = APP_ALIASES[alias_match]
        process_found, window_found = is_app_running(alias_match)
        if process_found and window_found:
            os.system(f"wmctrl -a '{alias_match}' 2>/dev/null")
            print(f"[APP] Action: Bringing {alias_match} to focus")
            return f"{alias_match} is already open, bringing to focus"
        print(f"[APP] Action: Launching {alias_match}")
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Opening {alias_match}"

    # 3. Exact website
    if query in WEBSITE_MAP:
        return open_website(query)

    # 4. Fuzzy website
    web_match, web_score = process.extractOne(query, WEBSITE_MAP.keys())
    if web_score >= 75:
        return open_website(web_match)

    # 5. Installed app
    success, msg = launch_app(query)
    if success:
        return msg

    # 6. Google search fallback
    encoded = urllib.parse.quote(query)
    subprocess.Popen(f'google-chrome "https://www.google.com/search?q={encoded}"',
                     shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return f"Could not find '{query}', searching on Google"

