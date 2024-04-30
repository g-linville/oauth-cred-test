import secrets
import string


def generate_random_string(length: int) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def capitalize_first_letter(s: str) -> str:
    return s[0].upper() + s[1:]
