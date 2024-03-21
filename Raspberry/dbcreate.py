import sqlite3
try:
    conn = sqlite3.connect('IoT.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE DHT11(
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        DATETIME TEXT NOT NULL, 
        TEMPERATURE REAL NOT NULL, 
        HUMIDITY REAL NOT NULL);""")
    conn.commit()
    cur.execute("""CREATE TABLE MQ135(
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        DATETIME TEXT NOT NULL, 
        PPM INTEGER NOT NULL);""")
    conn.commit()
finally:
    conn.close()
