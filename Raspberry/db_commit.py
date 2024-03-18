import sqlite3
import datetime
from time import sleep
from socket import *
from random import randint #placeholder for de værdier vi får via UART, bliver nok gemt i EEPROM


query_dht = """INSERT INTO DHT11 (DATETIME, TEMPERATURE, HUMIDITY) VALUES(?,?,?)"""
query_mq135 = """INSERT INTO MQ135 (DATETIME, PPM) VALUES(?,?)"""
while True:
    # Vigtigt de er inde i loopet, ellers bliver de ikke opdateret:
    HUMIDITY = randint(0, 100) 
    TEMPERATURE = randint(0, 100)
    PPM = randint(380, 1400)
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
        cur.execute("""SELECT * FROM DHT11 ORDER BY ID DESC LIMIT 20""")  # limit fortæller at det er de første 20, med order by ID DESC, vender tabellen og de nyeste commits er nu i toppen
        dataudtræk = cur.fetchall()
        print(dataudtræk)  # Det er ikke kønt, men det virker
        conn.close
        sleep(1)
