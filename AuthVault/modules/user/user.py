from modules.user.passwords import hash_bcrypt, verify_bcrypt
import secrets

def generate_id(username):
    return username + "_" + secrets.token_hex(12)

class User:
    def __init__(self, username, password, role: dict):
        self.username = username
        self.hashed_password = self.hash_password(password)
        self.role = role.get("role")
        
    def hash_password(self, password: str):
        return hash_bcrypt(password)

    def verify_password(self, password: str):
        return verify_bcrypt(password.encode(), self.hashed_password)
