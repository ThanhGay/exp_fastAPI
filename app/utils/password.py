import bcrypt
import secrets
import string

def encode_password(pwd: str) -> str:
    hashed = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(pwd: str, hashed_pwd: str) -> bool:
    return bcrypt.checkpw(pwd.encode("utf-8"), hashed_pwd.encode("utf-8"))

def generate_secure_password(length=8):
    if length < 4:
        raise ValueError("Length must be at least 4")

    uppercase = secrets.choice(string.ascii_uppercase)
    lowercase = secrets.choice(string.ascii_lowercase)
    digit = secrets.choice(string.digits)
    special = secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")

    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"

    remaining = [secrets.choice(all_chars) for _ in range(length - 4)]

    password_list = [uppercase, lowercase, digit, special] + remaining
    secrets.SystemRandom().shuffle(password_list)

    return ''.join(password_list)
