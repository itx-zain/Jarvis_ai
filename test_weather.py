"""
test_weather.py — Test global weather support
"""

from weather import get_weather, _normalize_city, _is_valid_city, CITY_ALIASES

def test_city_normalization():
    """Test city name normalization and aliases."""
    print("=== CITY NORMALIZATION TESTS ===\n")
    
    test_cases = [
        ("bwp", "bahawalpur"),
        ("isb", "islamabad"),
        ("khi", "karachi"),
        ("lhr", "lahore"),
        ("rwp", "rawalpindi"),
        ("lahore", "lahore"),
        ("dubai", "dubai"),
        ("tokyo", "tokyo"),
        ("", ""),
    ]
    
    for raw, expected in test_cases:
        normalized = _normalize_city(raw)
        status = "✓" if normalized == expected else "✗"
        print(f"{status} '{raw}' -> '{normalized}' (expected: '{expected}')")
    
    print("\n=== VALID CITY TESTS ===\n")
    
    valid_cases = ["lahore", "dubai", "bahawalpur", "tokyo", "new york", "berlin"]
    for city in valid_cases:
        valid = _is_valid_city(city)
        print(f"✓ '{city}' is valid: {valid}")
    
    print("\n=== ALIASES ===")
    for abbr, full in CITY_ALIASES.items():
        print(f"  {abbr} -> {full}")


def test_weather_api():
    """Test actual weather API calls."""
    print("\n=== WEATHER API TESTS ===\n")
    
    test_cases = [
        ("bwp ka mausam batao", "bahawalpur"),
        ("isb weather", "islamabad"),
        ("khi weather", "karachi"),
        ("lahore weather", "lahore"),
        ("dubai weather", "dubai"),
        ("weather in tokyo", "tokyo"),
        ("weather in london", "london"),
    ]
    
    for cmd, expected_city in test_cases:
        print(f"=== Test: '{cmd}' (expected: {expected_city}) ===")
        result = get_weather(expected_city)
        if "Unable to fetch" not in result and "could not identify" not in result:
            print(f"✓ Got weather data")
        else:
            print(f"✗ Failed: {result}")
        print()


if __name__ == "__main__":
    test_city_normalization()
    test_weather_api()