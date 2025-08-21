import string
import random

def shorten_uuid():
    alpha = list(string.ascii_lowercase + string.digits)
    uuid = ''.join(random.choices(alpha, k=8))
    return uuid
