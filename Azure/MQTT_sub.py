import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1883)
client.subscribe("ESP32")


def message(message):
    with open("mqttdata_txt", "a") as file:
        file.write(f"{message.topic}: {message.payload.decode('utf-8')}\n")


client.on_message = message
client.loop_forever()
