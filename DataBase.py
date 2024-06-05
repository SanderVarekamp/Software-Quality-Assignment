import sqlite3
from datetime import datetime
import pandas as pd
import shutil

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

class Members:
    def __init__(self):
        self.SourceDB = "DataBase.db"
        self.BackupDB = "DataBase_Backup.db"

    def backup_sqlite_db(self):
        try:
            shutil.copy2(self.SourceDB, self.BackupDB)
            print(f"Backup successful! Database backed up to {self.BackupDB}")
        except Exception as e:
            print(f"An error occurred while backing up the database: {e}")
    
    def PrintMembers():
        conn = sqlite3.connect('DataBase.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM Logs")
        print (pd.read_sql_query("SELECT * FROM Members", conn))
        conn.close()

    def FindMember(Firstname, Lastname):
        conn = sqlite3.connect('DataBase.db')
        cur = conn.cursor()
        query = "SELECT * FROM Members WHERE Firstname=? AND Lastname=?"
        params = (Firstname, Lastname)
        cur.execute(query, params)
        rows = cur.fetchall()
        df = pd.read_sql_query(query, conn, params=params)
        print(df)
        conn.close()