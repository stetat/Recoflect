import secrets
import string

ALPHABET = string.digits + string.ascii_uppercase


def generate_family_invite_code():
    from .models import Family

    while True:
        invite_code = "".join(secrets.choices(ALPHABET, 6))
        if not Family.objects.filter(invite_code=invite_code).exists():
            return invite_code
