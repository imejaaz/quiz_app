import random
import string


def generate_random_id(size=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))
