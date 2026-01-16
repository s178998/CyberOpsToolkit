import bcrypt

def hash_bcrypt(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))

def verify_bcrypt(password: str, hashed_password: bytes):
    return bcrypt.checkpw(password.encode(), hashed_password)
