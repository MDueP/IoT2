import paho.mqtt.subscribe as subscribe
from gpiozero import LED
from time import sleep

led = LED(...)  # placeholder for pin
print("Subscribe MQTT script running")


def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    status = message.payload.decode()

    if status == "taend":
        led.on()
    if status == "sluk":
        led.off()


subscribe.callback(on_message_print, "LED",
                   hostname="Azure Public IP", userdata={"message_count": 0})
