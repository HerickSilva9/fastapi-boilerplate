from argon2 import PasswordHasher

ph = PasswordHasher()


def generate_hash(string: str) -> str:
    return ph.hash(string)