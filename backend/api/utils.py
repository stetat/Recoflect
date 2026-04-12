import string
import secrets
from .models import Family

def generate_family_invite_code():
    ALPHABET = string.digits + string.ascii_uppercase
    all_invite_codes = Family.invite_code.all()
    while True:
        invite_code = ''.join(secret.choices(ALPHABET, 6))
        if not Family.objects.filter(invite_code=invite_code).exists():
            return invite_code
    
    