import random
import string
import time


def generate_random_string_from_clock(size=3):
    result = ""
    for _ in range(size):
        number_dict = {x: random.choice(string.ascii_letters) for x in range(10)}
        time_string = str(int(time.time() * 1e7))
        result += "".join([number_dict[int(number)] for number in time_string])
    return result
