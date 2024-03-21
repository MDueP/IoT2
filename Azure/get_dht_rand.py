from random import randint
from datetime import datetime
from time import sleep


def get_dht11():
    temperatures = [randint(0, 50)]
    humidities = [randint(20, 90)]
    return temperatures, humidities
print(get_dht11())
