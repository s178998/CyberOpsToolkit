import pathlib
import json
from password_policy_tool.logs.logs import _Logs
import csv
from datetime import datetime, timezone
from json import JSONDecodeError

class LogAnalyzer:
    """
    Analyze password policy logs
    - Can be used standalone or called from other modules
    """

    BASE_PATH = pathlib.Path(__file__).parent.parent
    LOG_PATH = BASE_PATH / "data" / "raw_logs"
    REPORT_PATH = BASE_PATH / "reports"
    LOG_FILE = LOG_PATH / "password_logs.txt"

    def __init__(self):
        self.logs = _Logs().logs

    # -------------------- Stats --------------------
    def stats(self):
        total = len(self.logs)
        valid_count = sum(1 for entry in self.logs if entry["valid"])
        invalid_count = total - valid_count

        print(f"Total: {total}\nValid count: {valid_count}\nInvalid_count: {invalid_count}")
        return {
            "total": total,
            "valid": valid_count,
            "invalid": invalid_count
        }

    # -------------------- Export Report --------------------
    def export_csv(self):
        if not self.logs:
            print("❌ No logs to export")
            return

        self.REPORT_PATH.mkdir(parents=True, exist_ok=True)
        dt = datetime.now(timezone.utc).strftime("%d%m%Y_H%M%S")
        csv_path = self.REPORT_PATH / f"{dt}_passwords_report.csv"

        logs_for_csv = []
        for entry in self.logs:
            e = entry.copy()
            if e["messages"] is None:
                e["messages"] = ""
            elif isinstance(e["messages"], list):
                e["messages"] = " | ".join(e["messages"])
            logs_for_csv.append(e)

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=logs_for_csv[0].keys())
            writer.writeheader()
            writer.writerows(logs_for_csv)

        print(f"✅ CSV report exported -> {csv_path}")
        return csv_path

    
    def load_logs(self):
        if not self.LOG_FILE.exists():
            print(f"❌ file not found: {self.LOG_FILE}")
            return

        try:
            with open(self.LOG_FILE, "r") as f:
                self.logs = json.load(f)
        except JSONDecodeError:
            print("❌ Could not read JSON file")
            self.logs = []

    def check_file(self, mode="all"):
        """
        Print passwords from logs based on mode.
        
        Args:
            mode (str): "all", "valid", "invalid"
        """
        self.load_logs()

        if not self.logs:
            print("❌ No logs to analyze")
            return

        printed = False
        for entry in self.logs:
            password = entry.get("password", "<unknown>")
            valid = entry.get("valid", False)

            if mode == "all":
                print(f"password: {password} | valid: {valid}")
                printed = True
            elif mode == "valid" and valid:
                print(f"password: {password} | valid: True")
                printed = True
            elif mode == "invalid" and not valid:
                print(f"password: {password} | valid: False")
                printed = True

        if not printed:
            if mode == "valid":
                print("❌ No valid passwords to show.")
            elif mode == "invalid":
                print("❌ No invalid passwords to show.")