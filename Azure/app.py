import base64
from io import BytesIO
from flask import Flask, render_template
from matplotlib.figure import Figure
import datetime
from random import randint
import paho.mqtt.client as mqtt
app = Flask(__name__)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1883)
client.subscribe("ESP32")


def message(client, userdata, message):
    with open("mqttdata.txt", "a") as file:
        file.write(f"{message.topic}: {message.payload.decode('utf-8')}\n")


client.on_message = message
client.loop_start()


def graph_dht11():
    hum = [randint(20, 90) for j in range(10)]
    Timestamps = [datetime.datetime.now() + datetime.timedelta(hours=i)
                  for i in range(10)]
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#dbe212")
    ax.plot(Timestamps, hum, linestyle="dotted",
            c="#000", marker='o', linewidth='2', ms='5')
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("Temp/hum")
    fig.patch.set_facecolor("#fff")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="black")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


def graph_mq135():
    PPM = [randint(200, 4000) for j in range(10)]
    Timestamps = [datetime.datetime.now() + datetime.timedelta(hours=i)
                  for i in range(10)]
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#dbe212")
    ax.plot(Timestamps, PPM, linestyle="dotted",
            c="#000", marker='o', linewidth='2', ms='5')
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("PPM")
    fig.patch.set_facecolor("#fff")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="black")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/Data')
def Data():
    return render_template('Data.html')


@app.route('/DHT11graph')
def graph():
    dht11 = graph_dht11()
    mq135 = graph_mq135()
    return render_template('DHT11 graph.html', dht11=dht11, mq135=mq135)


@app.route('/Dashboard')
def Dashboard():

    return render_template('Dashboard.html')


@app.route('/taend', methods=['POST'])
def taend():
    publish.single("LED", "taend", hostname="Azure Public IP")
    return render_template('taend.html')


@app.route('/sluk', methods=['POST'])
def sluk():
    publish.single("LED", "sluk", hostname="Azure Public IP")
    return render_template('sluk.html')


app.run(debug=True)
