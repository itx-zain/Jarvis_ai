"""
test_intent_detection.py — Unit tests for detect_intent_group()
Run: python3 -m pytest test_intent_detection.py -v
  or: python3 test_intent_detection.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from action_registry import detect_intent_group


def _check(command, expected, label=None):
    got = detect_intent_group(command)
    passed = got == expected
    tag = "PASS" if passed else "FAIL"
    name = label or command
    print(f"  [{tag}] \"{name}\" -> {got}  (expected {expected})")
    return passed


def test_browser_prefix_overrides():
    """Commands starting with search/google/youtube/play must force BROWSER_ACTIONS."""
    cases = [
        ("search python flask tutorial",  "BROWSER_ACTIONS"),  # original bug
        ("search machine learning",       "BROWSER_ACTIONS"),
        ("search best linux distros",     "BROWSER_ACTIONS"),
        ("google how to use flask",       "BROWSER_ACTIONS"),
        ("youtube lofi music",            "BROWSER_ACTIONS"),
        ("play arijit singh songs",       "BROWSER_ACTIONS"),
        ("play lofi beats",               "BROWSER_ACTIONS"),
        ("lookup python docs",            "BROWSER_ACTIONS"),
        ("find online python tutorial",   "BROWSER_ACTIONS"),
        ("SEARCH flask tutorial",         "BROWSER_ACTIONS"),  # case insensitive
        ("PLAY something on youtube",     "BROWSER_ACTIONS"),
    ]
    print("=== test_browser_prefix_overrides ===")
    return all(_check(cmd, exp) for cmd, exp in cases)


def test_browser_keyword_detection():
    """Browser-related keywords without prefix."""
    cases = [
        ("open youtube",           "BROWSER_ACTIONS"),
        ("open whatsapp",          "BROWSER_ACTIONS"),
        ("open website",           "BROWSER_ACTIONS"),
    ]
    print("=== test_browser_keyword_detection ===")
    return all(_check(cmd, exp) for cmd, exp in cases)


def test_app_actions():
    cases = [
        ("open chrome",         "APP_ACTIONS"),
        ("open pycharm",        "APP_ACTIONS"),
        ("close pycharm",       "APP_ACTIONS"),
        ("open github",         "APP_ACTIONS"),
        ("pycharm band karo",   "APP_ACTIONS"),
        ("chrome kholo",        "APP_ACTIONS"),
        ("close it",            "APP_ACTIONS"),
    ]
    print("=== test_app_actions ===")
    return all(_check(cmd, exp) for cmd, exp in cases)


def test_terminal_actions():
    cases = [
        ("open terminal",          "TERMINAL_ACTIONS"),
        ("terminal kholo",         "TERMINAL_ACTIONS"),
        ("close terminal",         "TERMINAL_ACTIONS"),
        ("terminal band karo",     "TERMINAL_ACTIONS"),
        ("run python main.py",   "PROJECT_ACTIONS"),  # .py suffix = project context
        ("execute command",        "TERMINAL_ACTIONS"),
    ]
    print("=== test_terminal_actions ===")
    return all(_check(cmd, exp) for cmd, exp in cases)


def test_folder_actions():
    cases = [
        ("open downloads",       "FOLDER_ACTIONS"),
        ("downloads kholo",      "FOLDER_ACTIONS"),
        ("open documents",       "FOLDER_ACTIONS"),
        ("documents kholo",      "FOLDER_ACTIONS"),
        ("open desktop",         "FOLDER_ACTIONS"),
        ("open pictures",        "FOLDER_ACTIONS"),
        ("open videos",          "FOLDER_ACTIONS"),
        ("open music",           "FOLDER_ACTIONS"),
    ]
    print("=== test_folder_actions ===")
    return all(_check(cmd, exp) for cmd, exp in cases)


def test_file_actions():
    cases = [
        ("find resume",          "FILE_ACTIONS"),
        ("find invoice.pdf",     "FILE_ACTIONS"),
        ("resume dhoondo",       "FILE_ACTIONS"),
        ("open report.pdf",      "FILE_ACTIONS"),
        ("open test.txt",        "FILE_ACTIONS"),
    ]
    print("=== test_file_actions ===")
    return all(_check(cmd, exp) for cmd, exp in cases)


def test_system_actions():
    cases = [
        ("check battery",        "SYSTEM_ACTIONS"),
        ("battery kitni hai",    "SYSTEM_ACTIONS"),
        ("volume up",            "SYSTEM_ACTIONS"),
        ("volume up karo",       "SYSTEM_ACTIONS"),
        ("take screenshot",      "SYSTEM_ACTIONS"),
        ("screenshot lo",        "SYSTEM_ACTIONS"),
        ("check ram",            "SYSTEM_ACTIONS"),
        ("check cpu",            "SYSTEM_ACTIONS"),
        ("wifi status",          "SYSTEM_ACTIONS"),
        ("what is my ip",        "SYSTEM_ACTIONS"),
        ("check disk",           "SYSTEM_ACTIONS"),
        ("lock screen",          "SYSTEM_ACTIONS"),
        ("shutdown",             "SYSTEM_ACTIONS"),
        ("restart",              "SYSTEM_ACTIONS"),
        ("brightness up",        "SYSTEM_ACTIONS"),
        ("mute",                 "SYSTEM_ACTIONS"),
    ]
    print("=== test_system_actions ===")
    return all(_check(cmd, exp) for cmd, exp in cases)


def test_project_actions():
    cases = [
        ("project status",          "PROJECT_ACTIONS"),
        ("open my project",         "PROJECT_ACTIONS"),
        ("mera project kholo",      "PROJECT_ACTIONS"),
        ("show project files",      "PROJECT_ACTIONS"),
        ("run main.py",             "PROJECT_ACTIONS"),
        ("open ai_fallback.py",     "PROJECT_ACTIONS"),
        ("find python files",       "PROJECT_ACTIONS"),
    ]
    print("=== test_project_actions ===")
    return all(_check(cmd, exp) for cmd, exp in cases)


def test_window_actions():
    cases = [
        ("scroll down",         "WINDOW_ACTIONS"),
        ("scroll up",           "WINDOW_ACTIONS"),
        ("minimize window",     "WINDOW_ACTIONS"),
        ("close window",        "WINDOW_ACTIONS"),
        ("new tab",             "WINDOW_ACTIONS"),
        ("copy",                "WINDOW_ACTIONS"),
        ("paste",               "WINDOW_ACTIONS"),
        ("undo",                "WINDOW_ACTIONS"),
        ("save",                "WINDOW_ACTIONS"),
    ]
    print("=== test_window_actions ===")
    return all(_check(cmd, exp) for cmd, exp in cases)


def test_fallback_to_all():
    cases = [
        ("some random query",    "ALL"),
        ("xyz abc def",          "ALL"),
        ("",                     "ALL"),
    ]
    print("=== test_fallback_to_all ===")
    return all(_check(cmd, exp) for cmd, exp in cases)


if __name__ == "__main__":
    suites = [
        test_browser_prefix_overrides,
        test_browser_keyword_detection,
        test_app_actions,
        test_terminal_actions,
        test_folder_actions,
        test_file_actions,
        test_system_actions,
        test_project_actions,
        test_window_actions,
        test_fallback_to_all,
    ]

    total_pass = total_fail = 0
    for suite in suites:
        result = suite()
        print()
        if result:
            total_pass += 1
        else:
            total_fail += 1

    total = total_pass + total_fail
    print(f"{'='*40}")
    print(f"Suites passed: {total_pass}/{total}  |  Failed: {total_fail}/{total}")
    sys.exit(0 if total_fail == 0 else 1)
