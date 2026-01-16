from modules.user.user import User, generate_id, verify_bcrypt
from modules.auth.permissions import user_groups, can_user_perform
from password_policy_tool.password_policies_manager.password_policies_manager import PasswordPolicy
from modules.logs.logs import Logs
from pathlib import Path
import csv

# -------------------- Faculty Users --------------------
def get_faculty_users():
    """
    Returns initial faculty users with roles.
    Passwords will be set automatically using PasswordPolicy if preloaded.
    """
    return {
        "Dr_Smith_1001": {"role": "master_admin", "title": "Dean"},
        "Dr_Johnson_1002": {"role": "master_admin", "title": "Registrar"},
        "Dr_Williams_1003": {"role": "master_admin", "title": "CIO"},
        "Dr_Brown_1004": {"role": "admin", "title": "Department_Head"},
        "Dr_Jones_1005": {"role": "admin", "title": "IT_Admin"},
        "Prof_Davis_1006": {"role": "user", "title": "Professor"},
        "TA_Miller_1007": {"role": "user", "title": "TA"}
    }

# -------------------- User Manager --------------------
class UserManager:
    def __init__(self):
        self.users = {}  # username → {hashed_password, role, id, force_reset}
        self.pp = PasswordPolicy()
        self.logs = Logs()

    # -------------------- Standard Return --------------------
    def _return(self, ok, code, error=None, data=None):
        return {"ok": ok, "code": code, "error": error, "data": data}

    # -------------------- Role Normalization --------------------
    def _normalize_role(self, role):
        if isinstance(role, dict):
            return {"role": role.get("role", "user"), "title": role.get("title")}
        elif isinstance(role, str):
            return {"role": role, "title": None}
        return {"role": "user", "title": None}

    # -------------------- Logging Helper --------------------
    def get_log_func(self, role_name):
        role_map = {
            "master_admin": self.logs.log_master_admin,
            "admin": self.logs.log_admin,
            "user": self.logs.log_user
        }
        return role_map.get(role_name, self.logs.log_user)

    # -------------------- Register User --------------------
    def register(self, username, password, role):
        role_obj = self._normalize_role(role)
        log_func = self.get_log_func(role_obj["role"])

        # Password policy check
        valid, feedback = self.pp.check_password(password)
        log_func(id=None, username=username, action="register", success=valid, reason=feedback)
        if not valid:
            return self._return(False, "PASSWORD_INVALID", error=feedback)

        # Username uniqueness
        if username in self.users:
            log_func(id=self.users[username]["id"], username=username, action="register", success=False, reason="USERNAME_TAKEN")
            return self._return(False, "USERNAME_TAKEN", error="USERNAME_TAKEN")

        uid = generate_id(username)
        user_obj = User(username, password, role_obj)
        self.users[username] = {
            "hashed_password": user_obj.hashed_password,
            "role": role_obj,
            "id": uid,
            "force_reset": False
        }

        log_func(id=uid, username=username, action="register", success=True, reason="USER_CREATED")
        return self._return(True, "USER_CREATED", data={"id": uid, "username": username})

    # -------------------- Login User --------------------
    def login(self, username, password):
        if username not in self.users:
            self.logs.log_user(id=None, username=username, action="login", success=False, reason="USER_NOT_FOUND")
            return self._return(False, "USER_NOT_FOUND", error="USER_NOT_FOUND")

        user = self.users[username]
        log_func = self.get_log_func(user["role"]["role"])

        if not verify_bcrypt(password, user["hashed_password"]):
            log_func(id=user["id"], username=username, action="login", success=False, reason="INVALID_PASSWORD")
            return self._return(False, "INVALID_PASSWORD", error="INVALID_PASSWORD")

        log_func(id=user["id"], username=username, action="login", success=True, reason="CREDENTIALS_VALID")
        return self._return(True, "CREDENTIALS_VALID", data={
            "id": user["id"],
            "username": username,
            "role": user["role"],
            "force_reset": user["force_reset"]
        })

    # -------------------- Change Password --------------------
    def change_password(self, username, old_password, new_password):
        if username not in self.users:
            return self._return(False, "USER_NOT_FOUND", error="USER_NOT_FOUND")

        user = self.users[username]
        log_func = self.get_log_func(user["role"]["role"])

        # Verify old password
        if not verify_bcrypt(old_password, user["hashed_password"]):
            log_func(id=user["id"], username=username, action="change_password", success=False, reason="INVALID_OLD_PASSWORD")
            return self._return(False, "INVALID_OLD_PASSWORD", error="INVALID_OLD_PASSWORD")

        # Validate new password against policy
        valid, feedback = self.pp.check_password(new_password)
        log_func(id=user["id"], username=username, action="change_password", success=valid, reason=feedback)
        if not valid:
            return self._return(False, "PASSWORD_POLICY_FAILED", error=feedback)

        # Update password
        new_user_obj = User(username, new_password, user["role"])
        user["hashed_password"] = new_user_obj.hashed_password
        user["force_reset"] = False

        return self._return(True, "PASSWORD_CHANGED", data={"username": username})

    # -------------------- Preload Faculty Users --------------------
    def preload_faculty_users(self, export_csv: bool = True):
        faculty_users = get_faculty_users()
        results = []

        # Ensure logs folder exists
        LOG_DIR = Path(__file__).parent.parent / "logs"
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        export_file = LOG_DIR / "faculty_temp_passwords.csv"

        for username, role in faculty_users.items():
            if username not in self.users:
                # Generate a strong password that passes policy
                temp_pw = self.pp.generate_password(12)
                res = self.register(username, temp_pw, role)
                # Force password reset on first login
                self.users[username]["force_reset"] = True
                results.append({"username": username, "temp_password": temp_pw, "result": res})

        if export_csv:
            with open(export_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["username", "temp_password"])
                writer.writeheader()
                for r in results:
                    writer.writerow({"username": r["username"], "temp_password": r["temp_password"]})

        return results
