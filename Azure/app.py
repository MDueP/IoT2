import base64
from io import BytesIO
from flask import Flask, render_template
from matplotlib.figure import Figure
# from get_dht11_data import get_data
import paho.mqtt.publish as publish
app = Flask(__name__)


# def graph_temp():
# timestamps, temp, hum = get_data(20)
# fig = Figure()
# ax = fig.subplots()
# fig.subplots_adjust(bottom=0.3)
# ax.tick_params(axis='x', which='both', rotation=30)
# ax.set_facecolor("#dbe212")
# ax.plot(timestamps, hum, linestyle="dotted",
# c="#000", marker='o', linewidth='2', ms='5')
# ax.set_xlabel("Timestamps")
# ax.set_ylabel("Temperature Celsius")
# fig.patch.set_facecolor("#fff")
# ax.tick_params(axis="x", colors="black")
# ax.tick_params(axis="y", colors="black")
# buf = BytesIO()
# fig.savefig(buf, format="png")
# data = base64.b64encode(buf.getbuffer()).decode("ascii")
# return data


# def graph_fugt():
# timestamps, temp, hum = get_data(20)
# fig = Figure()
# ax = fig.subplots()
# fig.subplots_adjust(bottom=0.3)
# ax.tick_params(axis='x', which='both', rotation=30)
# ax.set_facecolor("#12e2ca")
# ax.plot(timestamps, hum, linestyle="dotted",
# c="#000", marker='o', linewidth='2', ms='5')
# ax.set_xlabel("Timestamps")
# ax.set_ylabel("Humidity")
# fig.patch.set_facecolor("#fff")
# ax.tick_params(axis="x", colors="black")
# ax.tick_params(axis="y", colors="black")
# Save it to a temporary buffer.
# buf = BytesIO()
# fig.savefig(buf, format="png")
# Embed the result in the html output.
# data = base64.b64encode(buf.getbuffer()).decode("ascii")
# return data


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/Data')
def Data():
    return render_template('Data.html')


# @app.route('/DHT11graph')
# def DHT11_graph():
    temp = graph_temp()
    fugt = graph_fugt()
    return render_template('DHT11 graph.html', temp=temp, fugt=fugt)


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