import sqlite3
from datetime import datetime

class Logs:
    def LogAction(username: str, activity: str, info: str, sus: bool):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        date = now.strftime("%d/%m/%Y")
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ActivityLog VALUES (?, ?, ?, ?, ?, ?)", 
                       (str(date), str(time), username, activity, info, sus))
        connection.commit()
        connection.close()

    def PrintLogs():
      conn = sqlite3.connect('DataBase.db')
      cur = conn.cursor()
      cur.execute("SELECT * FROM ActivityLog")
      rows = cur.fetchall()
      conn.close()
      for row in rows:
         print(row)