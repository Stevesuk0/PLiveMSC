import random


asd = "qwertyuiopasdfghjklzxcvbnm1234567890"


def randstr(length):
    a = ""
    for i in range(length):
        a = a + asd[random.randint(0, len(asd) - 1)]
    return a