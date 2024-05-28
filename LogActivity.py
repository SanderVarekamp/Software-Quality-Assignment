import sqlite3
from datetime import datetime

class LogActivity:
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