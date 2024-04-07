import sqlite3
import datetime
from time import sleep
from socket import *
import serial
import paho.mqtt.client as mqtt

ser = serial.Serial("/dev/ttyS0", 9600)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("20.162.97.36")

query_dht = """INSERT INTO DHT11 (DATETIME, TEMPERATURE, HUMIDITY) VALUES(?,?,?)"""
query_mq135 = """INSERT INTO MQ135 (DATETIME, PPM) VALUES(?,?)"""
while True:
    data = ser.readline().decode('utf-8').rstrip()
    listdata = [data]
    data[0:9]
    HUMIDITY = data[3:5]
    TEMPERATURE = data[0:2]
    PPM = data[6:9]
    data_dht = (datetime.datetime.now(), TEMPERATURE, HUMIDITY)
    data_mq135 = (datetime.datetime.now(), PPM)
    try:
        conn = sqlite3.connect('IoT.db')
        cur = conn.cursor()
        cur.execute(query_dht, data_dht)
        conn.commit()
        cur.execute(query_mq135, data_mq135)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f'Could not insert! {e}')
    finally:
        cur.execute("""SELECT * FROM DHT11 ORDER BY ID DESC LIMIT 1""")
        cur.execute("""SELECT * FROM MQ135 ORDER BY ID DESC LIMIT 1""")
        dataudtræk2 = cur.fetchall()
        datapub = [dataudtræk2]
        strdata = ','.join([str(datapub)])
        print(strdata)
        client.publish("ESP32", (strdata))
        sleep(60)
        conn.close
        sleep(60)
