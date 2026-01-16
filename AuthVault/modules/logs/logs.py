# modules/logs/logs.py
from datetime import datetime, timezone
from pathlib import Path
import json
from threading import Lock

class Logs:
    # Always relative to repo root
    BASE_DIR = Path(__file__).resolve().parents[2]  # <-- adjust so this is repo root
    DATABASE = BASE_DIR / "database" / "logs"

    MASTER_ADMIN_LOG_FILE = DATABASE / "master_admin_logs.json"
    ADMIN_LOG_FILE = DATABASE / "admin_logs.json"
    USER_LOG_FILE = DATABASE / "user_logs.json"

    def __init__(self):
        self.lock = Lock()
        self.master_admin_logs = []
        self.admin_logs = []
        self.user_logs = []

        # Ensure folder exists
        self.DATABASE.mkdir(parents=True, exist_ok=True)

        # Ensure files exist
        for file in [self.MASTER_ADMIN_LOG_FILE, self.ADMIN_LOG_FILE, self.USER_LOG_FILE]:
            if not file.exists():
                file.write_text("[]")

        # Load existing logs
        self.load_logs()

    def load_logs(self):
        """Reload logs from disk"""
        self.master_admin_logs = self._load_file(self.MASTER_ADMIN_LOG_FILE)
        self.admin_logs = self._load_file(self.ADMIN_LOG_FILE)
        self.user_logs = self._load_file(self.USER_LOG_FILE)

    def _load_file(self, filepath):
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _write_file(self, filepath, data):
        with self.lock:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)

    # ---------------- Logging ----------------
    def log_master_admin(self, id, username, action, success, reason):
        entry = {
            "master_admin_id": id,
            "master_admin_username": username,
            "master_admin_action": action,
            "master_admin_success": success,
            "master_admin_reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.master_admin_logs.append(entry)
        self._write_file(self.MASTER_ADMIN_LOG_FILE, self.master_admin_logs)

    def log_admin(self, id, username, action, success, reason):
        entry = {
            "admin_id": id,
            "admin_username": username,
            "admin_action": action,
            "admin_success": success,
            "admin_reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.admin_logs.append(entry)
        self._write_file(self.ADMIN_LOG_FILE, self.admin_logs)

    def log_user(self, id, username, action, success, reason):
        entry = {
            "id": id,
            "username": username,
            "action": action,
            "success": success,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.user_logs.append(entry)
        self._write_file(self.USER_LOG_FILE, self.user_logs)
