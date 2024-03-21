import paho.mqtt.client as mqtt
import serial
from time import sleep
from random import randint

# ser = serial.Serial("/dev/tty1", 9600)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# data_send = ser.readline()
client.connect("20.254.232.236")
while True:
    random_value = randint(0, 100)
    client.publish("LED", str(random_value))
    # client.publish("LED", json.dumps(data_send))
    sleep(0.5)
