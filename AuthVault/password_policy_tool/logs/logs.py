import pathlib
import json
from datetime import datetime, timezone
from threading import Lock

class _Logs:
    PATH = pathlib.Path.cwd()
    DATABASE = PATH / "password_policy_tool" / "data" / "raw_logs"
    LOG_FILE = DATABASE / "password_logs.txt"

    def __init__(self):
        self.lock = Lock()
        self.logs = []
        self.DATABASE.mkdir(parents=True, exist_ok=True)

        # Make sure log file exists
        if not self.LOG_FILE.exists():
            self.LOG_FILE.write_text("[]")
        self.load_logs()

    def load_logs(self):
        try:
            with open(self.LOG_FILE, "r") as f:
                self.logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.logs = []

    def log_check(self, password, valid, messages):
        entry = {
            "password": password,
            "valid": valid,
            "messages": messages if messages else ["Password valid"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.logs.append(entry)
        self._write_file()

    def _write_file(self):
        try:
            with self.lock:
                with open(self.LOG_FILE, "w", encoding="utf-8") as f:
                    json.dump(self.logs, f, indent=2)
        except Exception as e:
            print(f"Error writing logs: {e}")
