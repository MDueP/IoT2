import sqlite3
from datetime import datetime
import json
import paho.mqtt.subscribe as subscribe
print("Subscribe MQTT script running!")


def create_tabel():
    query = """CREATE TABLE IF NOT EXISTS DHT11(
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        DATETIME TEXT NOT NULL, 
        TEMPERATURE REAL NOT NULL, 
        HUMIDITY REAL NOT NULL);"""
    try:
        conn = sqlite3.connect('database/dht11.db')
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"sqlite error occured: {sql_e}")
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        conn.close()


create_tabel()


def on_message_print(client, userdata, message):

    query = """INSERT INTO DHT11 (datetime, temperature, humidity) VALUES(?,?,?)"""
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M:%S")
    print(type(json.loads(message.payload.decode())))
    # bliver til den dictionary
    dht11_data = json.loads(message.payload.decode())
    data = (now, dht11_data['temperature'], dht11_data['humidity'])

    try:
        conn = sqlite3.connect("database/dht11.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"sqlite error occured: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        conn.close()
