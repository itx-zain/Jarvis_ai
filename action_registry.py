"""
action_registry.py — Single source of truth for all Jarvis actions.
Provides action groups, intent keywords, and dynamic prompt builder.
"""

# ─── ACTION GROUPS ───
# Each entry: "action_name": {"desc": str, "examples": [str, ...]}

APP_ACTIONS = {
    "open_app": {

        "desc": "Open a desktop application",
        "examples": [
            
            "open pycharm -> {\"reply\":\"Opening PyCharm\",\"action\":\"open_app\",\"target\":\"pycharm\"}",
            "chrome kholo -> {\"reply\":\"Chrome khol raha hun\",\"action\":\"open_app\",\"target\":\"chrome\"}",
        ],

    },
    "close_app": {
        "desc": "Close a named application",
        "examples": [
            "close chrome -> {\"reply\":\"Closing Chrome\",\"action\":\"close_app\",\"target\":\"chrome\"}",
            "pycharm band karo -> {\"reply\":\"PyCharm band kar raha hun\",\"action\":\"close_app\",\"target\":\"pycharm\"}",
        ],
    },
    "close_last_app": {
        "desc": "Close the last opened app",
        "examples": [
            "close it -> {\"reply\":\"Closing last app\",\"action\":\"close_last_app\",\"target\":\"\"}",
            "band karo -> {\"reply\":\"Band kar raha hun\",\"action\":\"close_last_app\",\"target\":\"\"}",
        ],
    },
}

TERMINAL_ACTIONS = {
    "open_terminal": {
        "desc": "Open a terminal window",
        "examples": [
            "open terminal -> {\"reply\":\"Opening terminal\",\"action\":\"open_terminal\",\"target\":\"\"}",
            "terminal kholo -> {\"reply\":\"Terminal khol raha hun\",\"action\":\"open_terminal\",\"target\":\"\"}",
        ],
    },
    "run_terminal": {
        "desc": "Run a command in terminal",
        "examples": [
            "run python main.py -> {\"reply\":\"Running command\",\"action\":\"run_terminal\",\"target\":\"python main.py\"}",
        ],
    },
    "close_terminal": {
        "desc": "Close terminal window",
        "examples": [
            "close terminal -> {\"reply\":\"Closing terminal\",\"action\":\"close_terminal\",\"target\":\"\"}",
            "terminal band karo -> {\"reply\":\"Terminal band kar raha hun\",\"action\":\"close_terminal\",\"target\":\"\"}",
        ],
    },
}

FOLDER_ACTIONS = {
    "open_folder": {
        "desc": "Open a system folder (downloads, documents, desktop, pictures, videos, music, home)",
        "examples": [
            "open downloads -> {\"reply\":\"Opening Downloads\",\"action\":\"open_folder\",\"target\":\"downloads\"}",
            "documents kholo -> {\"reply\":\"Documents khol raha hun\",\"action\":\"open_folder\",\"target\":\"documents\"}",
            "open desktop -> {\"reply\":\"Opening Desktop\",\"action\":\"open_folder\",\"target\":\"desktop\"}",
        ],
    },
}

FILE_ACTIONS = {
    "open_file": {
        "desc": "Open a specific file by name",
        "examples": [
            "open report.pdf -> {\"reply\":\"Opening report.pdf\",\"action\":\"open_file\",\"target\":\"report.pdf\"}",
            "open test.py -> {\"reply\":\"Opening test.py\",\"action\":\"open_file\",\"target\":\"test.py\"}",
        ],
    },
    "find_file": {
        "desc": "Search for a file across common user directories",
        "examples": [
            "find resume -> {\"reply\":\"Searching for resume\",\"action\":\"find_file\",\"target\":\"resume\"}",
            "resume dhoondo -> {\"reply\":\"Resume dhoond raha hun\",\"action\":\"find_file\",\"target\":\"resume\"}",
        ],
    },
}

BROWSER_ACTIONS = {
    "open_website": {
        "desc": "Open a website or URL",
        "examples": [
            "open github -> {\"reply\":\"Opening GitHub\",\"action\":\"open_website\",\"target\":\"github\"}",
        ],
    },
    "google_search": {
        "desc": "Search on Google",
        "examples": [
            "search python tutorial -> {\"reply\":\"Searching on Google\",\"action\":\"google_search\",\"target\":\"python tutorial\"}",
        ],
    },
    "youtube_play": {
        "desc": "Play something on YouTube",
        "examples": [
            "play lofi beats -> {\"reply\":\"Playing on YouTube\",\"action\":\"youtube_play\",\"target\":\"lofi beats\"}",
        ],
    },
    "whatsapp_open": {
        "desc": "Open WhatsApp Web",
        "examples": [
            "open whatsapp -> {\"reply\":\"Opening WhatsApp\",\"action\":\"whatsapp_open\",\"target\":\"\"}",
        ],
    },
    "whatsapp_message": {
        "desc": "Send a WhatsApp message (target format: contact:message)",
        "examples": [
            "send message to Ahmad Raza Software House saying hello -> {\"reply\":\"Sending message\",\"action\":\"whatsapp_message\",\"target\":\"Ahmad:hello\"}",
        ],
    },
}

SYSTEM_ACTIONS = {
    "get_battery":  {"desc": "Check battery level",    "examples": ["check battery -> {\"reply\":\"Checking battery\",\"action\":\"get_battery\",\"target\":\"\"}", "battery kitni hai -> {\"reply\":\"Battery check kar raha hun\",\"action\":\"get_battery\",\"target\":\"\"}"]},
    "get_time":     {"desc": "Get current time",       "examples": ["what is the time -> {\"reply\":\"Checking time\",\"action\":\"get_time\",\"target\":\"\"}", "time batao -> {\"reply\":\"Waqt bata raha hun\",\"action\":\"get_time\",\"target\":\"\"}"]},
    "get_date":     {"desc": "Get current date",       "examples": ["what is today's date -> {\"reply\":\"Checking date\",\"action\":\"get_date\",\"target\":\"\"}"]},
    "get_ram":      {"desc": "Check RAM usage",        "examples": ["check ram -> {\"reply\":\"Checking RAM\",\"action\":\"get_ram\",\"target\":\"\"}"]},
    "get_cpu":      {"desc": "Check CPU usage",        "examples": ["check cpu -> {\"reply\":\"Checking CPU\",\"action\":\"get_cpu\",\"target\":\"\"}"]},
    "get_wifi":     {"desc": "Check WiFi status",      "examples": ["wifi status -> {\"reply\":\"Checking WiFi\",\"action\":\"get_wifi\",\"target\":\"\"}"]},
    "get_ip":       {"desc": "Get IP address",         "examples": ["what is my ip -> {\"reply\":\"Getting IP\",\"action\":\"get_ip\",\"target\":\"\"}"]},
    "get_disk":     {"desc": "Check disk space",       "examples": ["check disk -> {\"reply\":\"Checking disk\",\"action\":\"get_disk\",\"target\":\"\"}"]},
    "screenshot":   {"desc": "Take a screenshot",      "examples": ["take screenshot -> {\"reply\":\"Taking screenshot\",\"action\":\"screenshot\",\"target\":\"\"}", "screenshot lo -> {\"reply\":\"Screenshot le raha hun\",\"action\":\"screenshot\",\"target\":\"\"}"]},
    "volume_up":    {"desc": "Increase volume",        "examples": ["volume up -> {\"reply\":\"Volume increased\",\"action\":\"volume_up\",\"target\":\"\"}", "volume up karo -> {\"reply\":\"Volume barha raha hun\",\"action\":\"volume_up\",\"target\":\"\"}"]},
    "volume_down":  {"desc": "Decrease volume",        "examples": ["volume down -> {\"reply\":\"Volume decreased\",\"action\":\"volume_down\",\"target\":\"\"}"]},
    "mute":         {"desc": "Toggle mute",            "examples": ["mute -> {\"reply\":\"Muted\",\"action\":\"mute\",\"target\":\"\"}"]},
    "set_volume":   {"desc": "Set volume to a level",  "examples": ["set volume to 60 -> {\"reply\":\"Setting volume\",\"action\":\"set_volume\",\"target\":\"60\"}"]},
    "brightness_up":   {"desc": "Increase brightness", "examples": ["brightness up -> {\"reply\":\"Brightness increased\",\"action\":\"brightness_up\",\"target\":\"\"}"]},
    "brightness_down": {"desc": "Decrease brightness", "examples": ["brightness down -> {\"reply\":\"Brightness decreased\",\"action\":\"brightness_down\",\"target\":\"\"}"]},
    "lock_screen":  {"desc": "Lock the screen",        "examples": ["lock screen -> {\"reply\":\"Locking screen\",\"action\":\"lock_screen\",\"target\":\"\"}"]},
    "sleep":        {"desc": "Put system to sleep",    "examples": ["sleep -> {\"reply\":\"Going to sleep\",\"action\":\"sleep\",\"target\":\"\"}"]},
    "shutdown":     {"desc": "Shutdown the system",    "examples": ["shutdown -> {\"reply\":\"Shutting down\",\"action\":\"shutdown\",\"target\":\"\"}"]},
    "restart":      {"desc": "Restart the system",     "examples": ["restart -> {\"reply\":\"Restarting\",\"action\":\"restart\",\"target\":\"\"}"]},
    "empty_trash":  {"desc": "Empty the trash",        "examples": ["empty trash -> {\"reply\":\"Emptying trash\",\"action\":\"empty_trash\",\"target\":\"\"}"]},
    "weather":      {"desc": "Get weather for a city (or current location if no city)", "examples": [
        "weather -> {\"reply\":\"Checking current weather\",\"action\":\"weather\",\"target\":\"\"}",
        "weather in london -> {\"reply\":\"Checking weather in London\",\"action\":\"weather\",\"target\":\"london\"}",
        "paris ka mausam batao -> {\"reply\":\"Paris ka mausam check kar raha hun\",\"action\":\"weather\",\"target\":\"paris\"}",
        "tokyo weather -> {\"reply\":\"Checking weather in Tokyo\",\"action\":\"weather\",\"target\":\"tokyo\"}",
        "berlin temperature -> {\"reply\":\"Checking temperature in Berlin\",\"action\":\"weather\",\"target\":\"berlin\"}",
        "new york weather -> {\"reply\":\"Checking weather in New York\",\"action\":\"weather\",\"target\":\"new york\"}",
        "mausam kaisa hai -> {\"reply\":\"Mausam check kar raha hun\",\"action\":\"weather\",\"target\":\"\"}",
        "today weather -> {\"reply\":\"Today's weather check kar raha hun\",\"action\":\"weather\",\"target\":\"\"}",
    ]},
}

WINDOW_ACTIONS = {
    "minimize":      {"desc": "Minimize active window",  "examples": ["minimize -> {\"reply\":\"Window minimized\",\"action\":\"minimize\",\"target\":\"\"}"]},
    "maximize":      {"desc": "Maximize active window",  "examples": ["maximize -> {\"reply\":\"Window maximized\",\"action\":\"maximize\",\"target\":\"\"}"]},
    "close_window":  {"desc": "Close active window",     "examples": ["close window -> {\"reply\":\"Closing window\",\"action\":\"close_window\",\"target\":\"\"}", "current window close karo -> {\"reply\":\"Window band kar raha hun\",\"action\":\"close_window\",\"target\":\"\"}"]},
    "new_tab":       {"desc": "Open new browser tab",   "examples": ["new tab -> {\"reply\":\"New tab opened\",\"action\":\"new_tab\",\"target\":\"\"}"]},
    "close_tab":     {"desc": "Close current tab",      "examples": ["close tab -> {\"reply\":\"Tab closed\",\"action\":\"close_tab\",\"target\":\"\"}"]},
    "scroll_up":     {"desc": "Scroll up",              "examples": ["scroll up -> {\"reply\":\"Scrolling up\",\"action\":\"scroll_up\",\"target\":\"\"}"]},
    "scroll_down":   {"desc": "Scroll down",            "examples": ["scroll down -> {\"reply\":\"Scrolling down\",\"action\":\"scroll_down\",\"target\":\"\"}"]},
    "go_back":       {"desc": "Go back in browser",     "examples": ["go back -> {\"reply\":\"Going back\",\"action\":\"go_back\",\"target\":\"\"}"]},
    "go_forward":    {"desc": "Go forward in browser",  "examples": ["go forward -> {\"reply\":\"Going forward\",\"action\":\"go_forward\",\"target\":\"\"}"]},
    "refresh":       {"desc": "Refresh current page",   "examples": ["refresh -> {\"reply\":\"Refreshing\",\"action\":\"refresh\",\"target\":\"\"}"]},
    "copy":          {"desc": "Copy selection",         "examples": ["copy -> {\"reply\":\"Copied\",\"action\":\"copy\",\"target\":\"\"}"]},
    "paste":         {"desc": "Paste clipboard",        "examples": ["paste -> {\"reply\":\"Pasted\",\"action\":\"paste\",\"target\":\"\"}"]},
    "cut":           {"desc": "Cut selection",          "examples": ["cut -> {\"reply\":\"Cut\",\"action\":\"cut\",\"target\":\"\"}"]},
    "undo":          {"desc": "Undo last action",       "examples": ["undo -> {\"reply\":\"Undo\",\"action\":\"undo\",\"target\":\"\"}"]},
    "redo":          {"desc": "Redo last action",       "examples": ["redo -> {\"reply\":\"Redo\",\"action\":\"redo\",\"target\":\"\"}"]},
    "select_all":    {"desc": "Select all",             "examples": ["select all -> {\"reply\":\"Selected all\",\"action\":\"select_all\",\"target\":\"\"}"]},
    "save":          {"desc": "Save current file",      "examples": ["save -> {\"reply\":\"Saved\",\"action\":\"save\",\"target\":\"\"}"]},
    "type_text":     {"desc": "Type text using keyboard","examples": ["type hello world -> {\"reply\":\"Typing\",\"action\":\"type_text\",\"target\":\"hello world\"}"]},
}

PROJECT_ACTIONS = {
    "open_project": {
        "desc": "Open the voice.ai project folder",
        "examples": [
            "open my project -> {\"reply\":\"Opening project\",\"action\":\"open_project\",\"target\":\"\"}",
            "mera project kholo -> {\"reply\":\"Project khol raha hun\",\"action\":\"open_project\",\"target\":\"\"}",
        ],

    },
    "list_project_files": {
        "desc": "List all files in the project",
        "examples": [
            "show project files -> {\"reply\":\"Showing files\",\"action\":\"list_project_files\",\"target\":\"\"}",
            "project files dikhao -> {\"reply\":\"Files dikha raha hun\",\"action\":\"list_project_files\",\"target\":\"\"}",
        ],
    },
    "open_project_file": {
        "desc": "Open a specific project file in editor",
        "examples": [
            "open ai_fallback.py -> {\"reply\":\"Opening ai_fallback.py\",\"action\":\"open_project_file\",\"target\":\"ai_fallback.py\"}",
            "open commands.py -> {\"reply\":\"Opening commands.py\",\"action\":\"open_project_file\",\"target\":\"commands.py\"}",
        ],
    },
    "run_project_file": {
        "desc": "Run a project Python file in terminal",
        "examples": [
            "run main.py -> {\"reply\":\"Running main.py\",\"action\":\"run_project_file\",\"target\":\"main.py\"}",
            "main.py chalao -> {\"reply\":\"main.py chala raha hun\",\"action\":\"run_project_file\",\"target\":\"main.py\"}",
        ],
    },
    "search_project": {
        "desc": "Search files inside the project directory",
        "examples": [
            "find python files -> {\"reply\":\"Searching Python files\",\"action\":\"search_project\",\"target\":\"*.py\"}",
            "find ai file -> {\"reply\":\"Searching ai file\",\"action\":\"search_project\",\"target\":\"ai\"}",
        ],
    },
    "project_status": {
        "desc": "Show project file count and stats",
        "examples": [
            "project status -> {\"reply\":\"Checking project status\",\"action\":\"project_status\",\"target\":\"\"}",
        ],
    },
}

UTILITY_ACTIONS = {
    "chat": {
        "desc": "Answer general questions, jokes, or conversations",
        "examples": [
            "tell me a joke -> {\"reply\":\"Why don't scientists trust atoms? Because they make up everything!\",\"action\":\"chat\",\"target\":\"\"}",
        ],
    },
}

# ─── FULL REGISTRY (all groups merged) ───
ALL_ACTIONS = {
    **APP_ACTIONS,
    **TERMINAL_ACTIONS,
    **FOLDER_ACTIONS,
    **FILE_ACTIONS,
    **BROWSER_ACTIONS,
    **SYSTEM_ACTIONS,
    **WINDOW_ACTIONS,
    **PROJECT_ACTIONS,
    **UTILITY_ACTIONS,
}

# ─── INTENT KEYWORDS (for lightweight prompt selection) ───
# Maps group_name -> keywords that strongly suggest that group
INTENT_KEYWORDS = {
    "APP_ACTIONS":      ["open", "close", "launch", "start", "kholo", "band", "chalao", "chala"],
    "TERMINAL_ACTIONS": ["terminal", "console", "bash", "command", "run", "execute", "cmd"],
    "FOLDER_ACTIONS":   ["downloads", "documents", "desktop", "pictures", "videos", "music", "folder", "directory", "dikhao"],
    "FILE_ACTIONS":     ["find", "file", "pdf", "doc", "txt", "dhoondo", "dhoond"],
    "BROWSER_ACTIONS":  ["website", "youtube", "play", "google", "whatsapp", "browser", "url", "http", "search", "lookup", "find online"],
    "SYSTEM_ACTIONS":   ["battery", "volume", "brightness", "screenshot", "time", "date", "ram", "cpu", "wifi", "ip", "disk", "shutdown", "restart", "sleep", "lock", "mute", "trash", "weather", "mausam", "temperature", "forecast", "rain", "baarish", "humidity", "wind"],
    "WINDOW_ACTIONS":   ["window", "minimize", "maximize", "tab", "scroll", "copy", "paste", "undo", "redo", "save", "refresh", "back", "forward", "type"],
    "PROJECT_ACTIONS":  ["project", "main.py", "server.py", "ai_fallback", "commands.py", ".py", "voice.ai", "python files", "python file"],
}

# Maps group name -> action dict
GROUP_MAP = {
    "APP_ACTIONS":      APP_ACTIONS,
    "TERMINAL_ACTIONS": TERMINAL_ACTIONS,
    "FOLDER_ACTIONS":   FOLDER_ACTIONS,
    "FILE_ACTIONS":     FILE_ACTIONS,
    "BROWSER_ACTIONS":  BROWSER_ACTIONS,
    "SYSTEM_ACTIONS":   SYSTEM_ACTIONS,
    "WINDOW_ACTIONS":   WINDOW_ACTIONS,
    "PROJECT_ACTIONS":  PROJECT_ACTIONS,
}

_BASE_PROMPT = """You are Jarvis, a voice assistant. Convert commands to JSON.
Languages: English, Urdu, Roman Urdu, Hindi, Mixed
Format: {"reply":"response in same language as input","action":"action_name","target":"value or empty"}
Rules: reply in same language as input. JSON only."""


def build_system_prompt(group_name: str = "ALL") -> str:
    """
    Build a minimal system prompt for the given group name.
    group_name: one of GROUP_MAP keys, or "ALL" for full prompt.
    """
    if group_name == "ALL":
        actions = ALL_ACTIONS
    else:
        actions = GROUP_MAP.get(group_name, ALL_ACTIONS)

    action_names = ", ".join(actions.keys())
    examples_block = ""
    for action, meta in actions.items():
        for ex in meta["examples"]:
            parts = ex.split(" -> ", 1)
            if len(parts) == 2:
                examples_block += f"Input: {parts[0]}\nOutput: {parts[1]}\n\n"

    return (
        f"{_BASE_PROMPT}\n\n"
        f"Available actions: {action_names}\n\n"
        f"Examples:\n{examples_block.strip()}"
    )


# Commands that start with these words are forced to BROWSER_ACTIONS
_BROWSER_PREFIXES = ("search ", "google ", "youtube ", "play ", "lookup ", "find online ")


def detect_intent_group(command: str) -> str:
    """
    Detect the most likely action group from command keywords.
    Returns group name string or 'ALL' if ambiguous.
    """
    cmd = command.lower().strip()

    # Prefix override — highest priority
    if cmd.startswith(_BROWSER_PREFIXES):
        return "BROWSER_ACTIONS"

    scores = {}
    for group, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in cmd)
        if score > 0:
            scores[group] = score

    if not scores:
        return "ALL"

    best = max(scores, key=scores.get)
    top_score = scores[best]

    # Tie-break: prefer more specific groups over APP_ACTIONS
    top_groups = [g for g, s in scores.items() if s == top_score]
    if len(top_groups) > 1:
        priority = ["PROJECT_ACTIONS", "TERMINAL_ACTIONS", "FOLDER_ACTIONS",
                    "BROWSER_ACTIONS", "SYSTEM_ACTIONS", "FILE_ACTIONS",
                    "WINDOW_ACTIONS", "APP_ACTIONS"]
        for p in priority:
            if p in top_groups:
                return p

    return best
