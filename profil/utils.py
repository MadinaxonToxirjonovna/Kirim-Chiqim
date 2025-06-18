import random
import string

def harf_count(matn):
    h = sum(1 for c in matn if c in string.ascii_letters)
    return h <= 2

def generate_verification_code():
    kod = ''
    for i in range(6):
        r = random.randint(0, 9)
        h = random.choice(string.ascii_lowercase)
        if harf_count(kod):
            kod += str(random.choice((r, h)))
        else:
            kod += str(r)
    return kod
