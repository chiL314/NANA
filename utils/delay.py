# utils/delay.py
import time
import random

def random_sleep(min_s=1, max_s=3):
    time.sleep(random.uniform(min_s, max_s))