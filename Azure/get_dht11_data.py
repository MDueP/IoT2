import sqlite3
from random import randint
from datetime import datetime
from time import sleep


def get_data(number_of_rows):
    query = """SELECT * FROM DHT11 ORDER BY ID DESC;"""
    datetimes = []
    temperatures = []
    humidities = []
    try:
        global conn == sqlite3.connect("database/dht11.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        for row in rows:
            datetimes.append(row[1])
            temperatures.append(row[2])
            humidities.append(row[3])
        return datetimes, temperatures, humidities
    except sqlite3.Error as sql_e:
        print(f"sqlite error occured: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        conn.close()


get_data(20)
