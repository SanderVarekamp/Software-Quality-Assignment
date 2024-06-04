import sqlite3
from datetime import datetime
import pandas as pd

class Logs:
    def LogAction(user, activity, info, sus):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        date = now.strftime("%d/%m/%Y")
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Logs (
                            Date TEXT, 
                            Time TEXT, 
                            User TEXT, 
                            Activity TEXT, 
                            Information TEXT, 
                            Suspicious TEXT 
                          )""")
        cursor.execute("INSERT INTO Logs VALUES (?, ?, ?, ?, ?, ?)", 
                       (str(date), str(time), user, activity, info, sus))
        connection.commit()
        connection.close()

    def PrintLogs():
      conn = sqlite3.connect('DataBase.db')
      cur = conn.cursor()
      cur.execute("SELECT * FROM Logs")
      print (pd.read_sql_query("SELECT * FROM Logs", conn))
      conn.close()