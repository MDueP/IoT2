import paho.qtt.publish as publish
import paho.mqtt.subscribe as subscribe
import serial
import json
from time import sleep

ser = serial.Serial("/dev/ttyS0", 9600)

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    status = message.payload.decode()

    print("LED status = ", status)
    ser.write(status)
        
print("Online.")
while True:
    sleep(0.5)
    data_send = ser.readline()
    print("ESP data = ", data_send)
    publish.single("ESP32", json.dumps(data_send), hostname = "Azure Public IP" )
    
    subscribe.callback(on_message_print, "LED", hostname = "Azure Public IP", userdata = {"message_count": 0})
    