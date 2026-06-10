import socket

def find_free_port(start=5000, end=5100):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    raise RuntimeError('No free port found between 5000-5100')

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import speak as speak_module
import commands as cmd_module
import ai_fallback as ai_fallback_module
from commands import execute_command
import traceback
import threading
from voice import listen

app = Flask(__name__, static_folder='frontend')
CORS(app)

_listen_lock = threading.Lock()

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('frontend', filename)

@app.route('/status')
def status():
    return jsonify({'status': 'online'})

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'response': 'Invalid request.'})

    command = data.get('command', '').lower().strip()
    if not command:
        return jsonify({'response': 'No command received.'})

    captured = []

    def capture_speak(text):
        text = str(text)
        print("Jarvis:", text)
        captured.append(text)
        try:
            speak_module.engine.say(text)
            speak_module.engine.runAndWait()
        except Exception:
            pass

    speak_module.speak = capture_speak
    cmd_module.speak = capture_speak
    ai_fallback_module._speak_module.speak = capture_speak

    try:
        execute_command(command)
    except Exception as e:
        traceback.print_exc()
        captured.append(f"Sorry, something went wrong.")

    return jsonify({
        'response': ' '.join(captured) if captured else 'Command executed.'
    })

@app.route('/listen', methods=['POST'])
def handle_listen():
    if not _listen_lock.acquire(blocking=False):
        return jsonify({'status': 'busy', 'command': '', 'response': 'Already listening'})
    try:
        command = listen()
        if not command:
            return jsonify({'status': 'empty', 'command': '', 'response': ''})

        captured = []

        def capture_speak(text):
            text = str(text)
            print("Jarvis:", text)
            captured.append(text)
            try:
                speak_module.engine.say(text)
                speak_module.engine.runAndWait()
            except Exception:
                pass

        speak_module.speak = capture_speak
        cmd_module.speak = capture_speak
        ai_fallback_module._speak_module.speak = capture_speak

        try:
            execute_command(command)
        except Exception as e:
            traceback.print_exc()
            captured.append('Sorry, something went wrong.')

        return jsonify({
            'status': 'ok',
            'command': command,
            'response': ' '.join(captured) if captured else 'Command executed.'
        })
    finally:
        _listen_lock.release()


if __name__ == '__main__':
    port = find_free_port()
    print(f"Jarvis server starting on http://127.0.0.1:{port}")
    # Write port to temp file so desktop_app.py can read it
    import tempfile, os
    port_file = os.path.join(tempfile.gettempdir(), 'jarvis_port.txt')
    with open(port_file, 'w') as f:
        f.write(str(port))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
