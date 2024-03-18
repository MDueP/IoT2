import sqlite3
# alt efter hvor python programmet er kørt fra
try:
    # Hvis den ikke eksistere, så laver den databasen
    conn = sqlite3.connect('IoT.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE DHT11(
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        DATETIME TEXT NOT NULL, 
        TEMPERATURE REAL NOT NULL, 
        HUMIDITY REAL NOT NULL);""")
    # cursor objektet skal altid gøre ting i string, da den ikke kan f.eks. sql
    conn.commit()
    cur.execute("""CREATE TABLE MQ135(
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        DATETIME TEXT NOT NULL, 
        PPM INTEGER NOT NULL);""")
    conn.commit()
finally:
    conn.close()
