import sys
import os
import time
import logging
import threading
import subprocess
import urllib.request
import urllib.error
import tempfile
from typing import Optional

try:
    import webview
except ImportError as e:
    print("pywebview not installed. Run: pip install pywebview")
    raise SystemExit(1) from e

# ─── LOGGING ───
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(BASE_DIR, "jarvis.log")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file),
    ],
)
log = logging.getLogger(__name__)

PORT_FILE: str = os.path.join(tempfile.gettempdir(), "jarvis_port.txt")
SERVER_READY_TIMEOUT = 30

server_process: Optional[subprocess.Popen] = None


def get_server_url() -> str:
    """Read port from temp file written by server.py"""
    for _ in range(60):
        try:
            with open(PORT_FILE, "r") as f:
                port = int(f.read().strip())
                return f"http://127.0.0.1:{port}"
        except (OSError, ValueError):
            time.sleep(0.1)
    return "http://127.0.0.1:5000"


def wait_for_server(timeout: int = SERVER_READY_TIMEOUT) -> Optional[str]:
    log.info("Waiting for Flask server to be ready...")
    server_url = get_server_url()
    log.info(f"Server URL: {server_url}")
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(f"{server_url}/status", timeout=1)
            log.info("Flask server is ready.")
            return server_url
        except (urllib.error.URLError, OSError):
            time.sleep(0.5)
    log.error("Flask server did not start in time.")
    return None


def start_flask_server() -> None:
    global server_process
    server_script = os.path.join(BASE_DIR, "server.py")
    log.info(f"Starting Flask server: {server_script}")
    proc = subprocess.Popen(
        [sys.executable, server_script],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    server_process = proc
    log.info(f"Flask server started with PID: {proc.pid}")


def stop_flask_server() -> None:
    global server_process
    proc = server_process
    if proc is None or proc.poll() is not None:
        return
    log.info("Stopping Flask server...")
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
    log.info("Flask server stopped.")


class JarvisApp:
    def __init__(self, window: "webview.Window") -> None:
        self.window = window

    @staticmethod
    def on_closed() -> None:
        log.info("Window closed. Shutting down...")
        stop_flask_server()


def main() -> None:
    try:
        os.remove(PORT_FILE)
    except OSError:
        pass

    server_thread = threading.Thread(target=start_flask_server, daemon=True)
    server_thread.start()

    server_url = wait_for_server()
    if not server_url:
        log.error("Could not connect to server. Exiting.")
        stop_flask_server()
        sys.exit(1)

    window = webview.create_window(
        title="Jarvis AI",
        url=server_url,
        width=480,
        height=750,
        resizable=True,
        min_size=(420, 650),
        background_color="#0a0a0f",
    )

    app = JarvisApp(window)
    window.events.closed += app.on_closed

    log.info("Launching Jarvis desktop window...")
    webview.start(debug=False)

    stop_flask_server()
    log.info("Jarvis shut down cleanly.")


if __name__ == "__main__":
    main()
