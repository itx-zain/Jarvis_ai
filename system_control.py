import os
import subprocess
import datetime
import urllib.parse

def run(cmd):
    return subprocess.getoutput(cmd)

# ─── APPS OPEN ───
def open_chrome():       os.system("google-chrome &")
def open_vscode():       os.system("code &")
def open_notepad():      os.system("gedit &")
def open_file_manager(): os.system("nautilus &")
def open_terminal():     os.system("gnome-terminal &")
def open_vlc():          os.system("vlc &")
def open_rhythmbox():    os.system("rhythmbox &")
def open_calculator():   os.system("gnome-calculator &")
def open_settings():     os.system("gnome-control-center &")
def open_camera():       os.system("cheese &")
def open_calendar():     os.system("gnome-calendar &")
def open_maps():         os.system("google-chrome https://maps.google.com &")
def open_zoom():         os.system("zoom &")
def open_telegram():     os.system("telegram-desktop &")
def open_discord():      os.system("discord &")
def open_youtube():      os.system("google-chrome https://www.youtube.com &")
def open_google():       os.system("google-chrome https://www.google.com &")
def open_whatsapp():     os.system("google-chrome https://web.whatsapp.com &")
def open_facebook():     os.system("google-chrome https://www.facebook.com &")
def open_instagram():    os.system("google-chrome https://www.instagram.com &")
def open_gmail():        os.system("google-chrome https://mail.google.com &")
def open_github():       os.system("google-chrome https://www.github.com &")
def open_spotify():      os.system("google-chrome https://open.spotify.com &")
def open_netflix():      os.system("google-chrome https://www.netflix.com &")
def open_chatgpt():      os.system("google-chrome https://chat.openai.com &")

def search_google(query):
    os.system(f'google-chrome "https://www.google.com/search?q={urllib.parse.quote(query)}" &')

def search_youtube(query):
    os.system(f'google-chrome "https://www.youtube.com/results?search_query={urllib.parse.quote(query)}" &')

# ─── CLOSE APPS ───
_CLOSE_PROCESS_MAP = {
    "chrome":          "google-chrome",
    "google chrome":   "google-chrome",
    "vscode":          "code",
    "vs code":         "code",
    "visual studio":   "code",
    "pycharm":         "pycharm",
    "telegram":        "telegram-desktop",
    "postman":         "postman",
    "discord":         "discord",
    "vlc":             "vlc",
    "spotify":         "spotify",
    "zoom":            "zoom",
    "slack":           "slack",
    "gimp":            "gimp",
    "obs":             "obs",
    "skype":           "skype",
    "thunderbird":     "thunderbird",
    "firefox":         "firefox",
    "nautilus":        "nautilus",
    "steam":           "steam",
    "whatsapp":        "google-chrome",
    "terminal":        "gnome-terminal",
    "gnome-terminal":  "gnome-terminal",
    "xterm":           "xterm",
    "konsole":         "konsole",
    "tilix":           "tilix",
    "terminator":      "terminator",
}

def close_app(name):
    name = name.lower().strip()
    proc = _CLOSE_PROCESS_MAP.get(name, name)
    # Try graceful SIGTERM first, then force kill
    result = subprocess.getoutput(f"pkill -TERM -f '{proc}' 2>/dev/null")
    return result

def close_window():
    os.system("xdotool getactivewindow windowclose")

def force_close():
    os.system("xdotool getactivewindow key alt+F4")

# ─── WINDOW CONTROL ───
def minimize_window():
    os.system("xdotool getactivewindow windowminimize")

def maximize_window():
    os.system("xdotool getactivewindow windowmaximize")

def minimize_all():
    os.system("xdotool key super+d")

def switch_window():
    os.system("xdotool key alt+Tab")

def next_tab():
    os.system("xdotool key ctrl+Tab")

def prev_tab():
    os.system("xdotool key ctrl+shift+Tab")

def new_tab():
    """Open a new tab. Detects active browser window first."""
    _BROWSERS = {"chrome", "chromium", "firefox", "brave", "microsoft-edge", "edge"}

    # Get active window name via xdotool
    active = run("xdotool getactivewindow getwindowname 2>/dev/null").lower()
    browser_active = any(b in active for b in _BROWSERS)

    if browser_active:
        os.system("xdotool key ctrl+t")
        return "Browser detected. Opening new tab."

    # No browser active — open Chrome, wait, then new tab
    subprocess.Popen(["google-chrome"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import time; time.sleep(2)
    os.system("xdotool key ctrl+t")
    return "No browser found. Opening Chrome and creating new tab."

def close_tab():
    os.system("xdotool key ctrl+w")

def zoom_in():
    os.system("xdotool key ctrl+plus")

def zoom_out():
    os.system("xdotool key ctrl+minus")

def zoom_reset():
    os.system("xdotool key ctrl+0")

# ─── VOLUME ───
def volume_up():    os.system("pactl set-sink-volume @DEFAULT_SINK@ +10%")
def volume_down():  os.system("pactl set-sink-volume @DEFAULT_SINK@ -10%")
def mute():         os.system("pactl set-sink-mute @DEFAULT_SINK@ toggle")

def set_volume(level):
    os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")

def get_volume():
    out = run("pactl get-sink-volume @DEFAULT_SINK@")
    try:
        return out.split('/')[1].strip()
    except:
        return "unknown"

# ─── BRIGHTNESS ───
def get_display():
    return run("xrandr | grep ' connected' | awk '{print $1}' | head -1")

def get_brightness():
    val = run("xrandr --verbose | grep -i brightness | head -1 | awk '{print $2}'")
    try:
        return float(val)
    except:
        return 0.8

def set_brightness(val):
    display = get_display()
    val = max(0.1, min(1.0, val))
    os.system(f"xrandr --output {display} --brightness {round(val, 1)}")
    return val

def increase_brightness():
    return set_brightness(get_brightness() + 0.1)

def decrease_brightness():
    return set_brightness(get_brightness() - 0.1)

# ─── SCREENSHOT & RECORDING ───
def screenshot():
    filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    # gnome-screenshot works natively on both X11 and Wayland (GNOME)
    # scrot only works on X11; on Wayland it captures a black screen
    r = subprocess.run(
        ['gnome-screenshot', f'--file={filename}'],
        capture_output=True, timeout=10
    )
    if r.returncode == 0 and os.path.exists(filename) and os.path.getsize(filename) > 1000:
        return filename
    # Fallback: scrot (X11 only)
    subprocess.run(['scrot', filename], capture_output=True, timeout=10)
    if os.path.exists(filename) and os.path.getsize(filename) > 1000:
        return filename
    return filename

def screenshot_area():
    os.system("gnome-screenshot -a &")
    return "Select area for screenshot"

# ─── KEYBOARD SHORTCUTS ───
def copy():      os.system("xdotool key ctrl+c")
def paste():     os.system("xdotool key ctrl+v")
def cut():       os.system("xdotool key ctrl+x")
def undo():      os.system("xdotool key ctrl+z")
def redo():      os.system("xdotool key ctrl+y")
def select_all():os.system("xdotool key ctrl+a")
def save_file(): os.system("xdotool key ctrl+s")
def find_text(): os.system("xdotool key ctrl+f")
def new_window():os.system("xdotool key ctrl+n")

# ─── SCROLL & NAVIGATION ───
def scroll_up():
    if os.system("xdotool click 4 2>/dev/null") != 0:
        os.system("xdotool key Page_Up")

def scroll_down():
    if os.system("xdotool click 5 2>/dev/null") != 0:
        os.system("xdotool key Page_Down")
def go_top():       os.system("xdotool key ctrl+Home")
def go_bottom():    os.system("xdotool key ctrl+End")
def go_back():      os.system("xdotool key alt+Left")
def go_forward():   os.system("xdotool key alt+Right")
def refresh_page(): os.system("xdotool key F5")

# ─── SYSTEM INFO ───
def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime("%A, %B %d, %Y")

def get_battery():
    level = run("cat /sys/class/power_supply/BAT0/capacity 2>/dev/null")
    status = run("cat /sys/class/power_supply/BAT0/status 2>/dev/null")
    if level:
        return f"{level} percent, {status}"
    return "Battery info not available"

def get_ram():
    out = run("free -h | grep Mem")
    parts = out.split()
    if len(parts) >= 4:
        return f"Total {parts[1]}, Used {parts[2]}, Free {parts[3]}"
    return "RAM info not available"

def get_cpu():
    out = run("top -bn1 | grep 'Cpu(s)'")
    try:
        return out.split()[1] + " percent"
    except:
        return "CPU info not available"

def get_disk():
    out = run("df -h / | tail -1")
    parts = out.split()
    if len(parts) >= 4:
        return f"Total {parts[1]}, Used {parts[2]}, Free {parts[3]}"
    return "Disk info not available"

def get_wifi():
    out = run("iwgetid -r 2>/dev/null")
    return f"Connected to {out}" if out.strip() else "Not connected to WiFi"

def get_ip():
    out = run("hostname -I | awk '{print $1}'")
    return out.strip() if out else "IP not found"

def get_running_apps():
    out = run("wmctrl -l 2>/dev/null | awk '{$1=$2=$3=\"\"; print $0}' | sed 's/^ *//' | sort -u")
    return out.strip() if out else "No windows found"

def get_laptop_name():
    name = run("hostname")
    user = run("whoami")
    return f"Laptop name is {name}, user is {user}"

# ─── SYSTEM CONTROL ───
def shutdown_pc():  os.system("shutdown now")
def restart_pc():   os.system("reboot")
def lock_screen():  os.system("gnome-screensaver-command -l 2>/dev/null || xdg-screensaver lock 2>/dev/null")
def sleep_pc():     os.system("systemctl suspend")

def empty_trash():
    os.system("gio trash --empty")
    return "Trash emptied"

def show_notification(title, msg):
    os.system(f'notify-send "{title}" "{msg}"')

def type_text(text):
    os.system(f'xdotool type "{text}"')

def press_enter():
    os.system("xdotool key Return")

def press_escape():
    os.system("xdotool key Escape")
