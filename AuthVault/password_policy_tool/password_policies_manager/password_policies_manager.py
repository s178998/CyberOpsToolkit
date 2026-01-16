import random
import string
from password_policy_tool.logs.logs import _Logs

class PasswordPolicy:
    """
    Password Policy Manager
    - Can generate strong passwords
    - Can validate passwords
    - Can be used independently or by AuthVault modules
    """

    def __init__(self):
        self.logs = _Logs()
        # Define policy rules
        self.min_length = 8
        self.max_length = 128
        self.require_upper = True
        self.require_lower = True
        self.require_digit = True
        self.require_special = True
        self.special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

    # -------------------- Check Password --------------------
    def check_password(self, password: str):
        messages = []

        if len(password) < self.min_length:
            messages.append(f"Password must be at least {self.min_length} chars")
        if len(password) > self.max_length:
            messages.append(f"Password must be less than {self.max_length} chars")
        if self.require_upper and not any(c.isupper() for c in password):
            messages.append("Password must have at least one uppercase letter")
        if self.require_lower and not any(c.islower() for c in password):
            messages.append("Password must have at least one lowercase letter")
        if self.require_digit and not any(c.isdigit() for c in password):
            messages.append("Password must have at least one digit")
        if self.require_special and not any(c in self.special_chars for c in password):
            messages.append(f"Password mus have at least one special char: {self.special_chars}")

        valid = len(messages) == 0
        return valid, messages if messages else ["Password valid"]

    # -------------------- Generate Strong Password --------------------
    def generate_password(self, length=12):
            password_chars = [
                random.choice(string.ascii_uppercase),
                random.choice(string.ascii_lowercase),
                random.choice(string.digits),
                random.choice(self.special_chars)
            ]
            remaining_length = length - 4
            all_chars = string.ascii_letters + string.digits + self.special_chars
            password_chars += random.choices(all_chars, k=remaining_length)
            random.shuffle(password_chars)
            password = ''.join(password_chars)

            valid, messages = self.check_password(password)
            self.logs.log_check(password, valid, messages)
            return password

