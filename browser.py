import os
import time
import urllib.parse

def open_url(url):
    try:
        os.system(f'google-chrome "{url}" &')
        time.sleep(0.5)
    except Exception as e:
        print("Browser error:", e)

def youtube_open():
    open_url("https://www.youtube.com")
    return "Opened YouTube"

def youtube_search(query):
    open_url(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
    return f"Searched '{query}' on YouTube"

def youtube_search_and_play(query):
    open_url(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
    return f"Searching '{query}' on YouTube"

def youtube_pause_play():
    os.system("xdotool key k")
    return "Toggled play pause"

def youtube_next():
    os.system("xdotool key shift+n")
    return "Next video"

def youtube_fullscreen():
    os.system("xdotool key f")
    return "Toggled fullscreen"

def google_open():
    open_url("https://www.google.com")
    return "Opened Google"

def google_search(query):
    open_url(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
    return f"Searched '{query}' on Google"

def facebook_open():
    open_url("https://www.facebook.com")
    return "Opened Facebook"

def facebook_search(query):
    open_url(f"https://www.facebook.com/search/top?q={urllib.parse.quote(query)}")
    return f"Searched '{query}' on Facebook"

def instagram_open():
    open_url("https://www.instagram.com")
    return "Opened Instagram"

def whatsapp_open():
    open_url("https://web.whatsapp.com")
    return "Opened WhatsApp"

def whatsapp_search_contact(name):
    open_url("https://web.whatsapp.com")
    return f"Opened WhatsApp, search {name} manually"

def gmail_open():
    open_url("https://mail.google.com")
    return "Opened Gmail"

def gmail_compose():
    open_url("https://mail.google.com/mail/u/0/#compose")
    return "Opened Gmail compose"

def github_open():
    open_url("https://www.github.com")
    return "Opened GitHub"

def github_search(query):
    open_url(f"https://github.com/search?q={urllib.parse.quote(query)}")
    return f"Searched '{query}' on GitHub"

def spotify_open():
    open_url("https://open.spotify.com")
    return "Opened Spotify"

def go_back():
    os.system("xdotool key alt+Left")
    return "Went back"

def go_forward():
    os.system("xdotool key alt+Right")
    return "Went forward"

def refresh_page():
    os.system("xdotool key F5")
    return "Page refreshed"

def scroll_down():
    os.system("xdotool key Page_Down")
    return "Scrolled down"

def scroll_up():
    os.system("xdotool key Page_Up")
    return "Scrolled up"

def close_browser():
    os.system("pkill google-chrome")
    return "Browser closed"
