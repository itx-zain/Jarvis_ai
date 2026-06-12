"""
weather.py — Global weather查询 using wttr.in API
"""

import requests
import speak as _speak_module

_WTTR_URL = "https://wttr.in/{city}?format=j1"
_CURRENT_URL = "https://wttr.in/?format=j1"

# City aliases for common abbreviations
CITY_ALIASES = {
    "bwp": "bahawalpur",
    "isb": "islamabad",
    "khi": "karachi",
    "lhr": "lahore",
    "rwp": "rawalpindi",
    "fsd": "faisalabad",
    "mul": "multan",
    "guj": "gujranwala",
}

# Valid cities database (common cities to validate against)
_VALID_CITIES = {
    # Pakistan
    "lahore", "karachi", "islamabad", "rawalpindi", "faisalabad", "multan",
    "gujranwala", "peshawar", "quetta", "bahawalpur", "sialkot", "hyderabad",
    "bwp", "khi", "lhr", "isb", "rwp", "fsd", "mul", "guj",
    # Global
    "london", "paris", "tokyo", "new york", "berlin", "dubai", "mumbai",
    "delhi", "beijing", "shanghai", "sydney", "melbourne", "toronto",
    "vancouver", "los angeles", "san francisco", "chicago", "seattle",
    "amsterdam", "brussels", "madrid", "barcelona", "rome", "milan",
    "moscow", "istanbul", "cairo", "johannesburg", "singapore", "hong kong",
    "bangkok", "kuala lumpur", "jakarta", "manila", "seoul", "bangkok",
}

def speak(text):
    """Proxy for server.py to patch _speak_module.speak at runtime."""
    _speak_module.speak(text)


def _normalize_city(city: str) -> str:
    """Normalize city name using aliases and return lowercase."""
    if not city:
        return ""
    city_lower = city.lower().strip()
    normalized = CITY_ALIASES.get(city_lower, city)
    print(f"[WEATHER CITY RAW] {city}")
    print(f"[WEATHER CITY NORMALIZED] {normalized}")
    return normalized.lower().strip()


def _is_valid_city(city: str) -> bool:
    """Check if city appears in the valid cities list or has reasonable length."""
    if not city:
        return False
    city_lower = city.lower().strip()
    # Check against valid cities
    if city_lower in _VALID_CITIES:
        return True
    # Check if it looks like a real city name (2+ words, reasonable chars)
    if len(city_lower) >= 2 and all(c.isalpha() or c.isspace() or c == '-' for c in city_lower):
        # Accept city names with 2+ characters
        return len(city_lower.replace(" ", "").replace("-", "")) >= 2
    return False


def get_weather(city: str = "") -> str:
    """Get weather for a city or current location if city is empty."""
    # Normalize city name
    city = _normalize_city(city)
    
    # Validate city presence
    if city and not _is_valid_city(city):
        return "I could not identify the city. Please specify a city name."
    
    url = _CURRENT_URL if not city else _WTTR_URL.format(city=city)
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        current = data.get("current_condition", [{}])[0]
        location = data.get("nearest_area", [{}])[0].get("areaName", [{}])[0].get("value", city or "Current Location")
        
        temp = current.get("temp_C", "N/A")
        feels = current.get("FeelsLikeC", "N/A")
        cond = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        humidity = current.get("humidity", "N/A")
        wind = current.get("windspeedKmph", "N/A")
        
        return (
            f"Location: {location}\n"
            f"Temperature: {temp}°C\n"
            f"Feels Like: {feels}°C\n"
            f"Condition: {cond}\n"
            f"Humidity: {humidity}%\n"
            f"Wind: {wind} km/h"
        )
    except Exception as e:
        return f"Unable to fetch weather: {e}"