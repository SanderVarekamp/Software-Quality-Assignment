import sqlite3
from datetime import datetime
import pandas as pd

from Encrypt import *
class Database:
    
    def AddAllTables():
       Database.AddTableMembers()
       Database.AddTableLog()
       Encrypt(Members.SourceDB, "VeryGoodPassWord")

    def AddTableMembers():
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Members (
                            Username TEXT,
                            PasswordHash TEXT,
                            FirstName TEXT, 
                            LastName TEXT, 
                            Age INTEGER, 
                            Gender TEXT, 
                            Weight INTEGER, 
                            Address TEXT, 
                            City TEXT, 
                            Email TEXT, 
                            PhoneNumber TEXT, 
                            Type TEXT,
                            RegistrationDate TEXT, 
                            MemberID INTEGER
                          )""")
        connection.commit()
        connection.close()

    def AddTableLog():
      connection = sqlite3.connect("DataBase.db")
      cursor = connection.cursor()
      cursor.execute("""CREATE TABLE IF NOT EXISTS ActivityLog (
                            Date TEXT, 
                            Time TEXT, 
                            Username TEXT, 
                            Activity TEXT, 
                            Information TEXT, 
                            Suspicious TEXT 
                          )""")
      connection.commit()
      connection.close()

    def LogAction(username: str, activity: str, info: str, sus: bool):
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        date = now.strftime("%d/%m/%Y")
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ActivityLog VALUES (?, ?, ?, ?, ?, ?)", 
                       (str(date), str(time), username, activity, info, sus))
        connection.commit()
        connection.close()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")

    def PrintLogs():
      Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
      conn = sqlite3.connect('DataBase.db')
    #   cur = conn.cursor()
      print (pd.read_sql_query("SELECT * FROM ActivityLog", conn))
    #   cur.execute("SELECT * FROM ActivityLog")
    #   rows = cur.fetchall()
      conn.close()
    #   for row in rows:
    #      print(row)
      Encrypt(Members.SourceDB, "VeryGoodPassWord")

class Members:
    # def __init__(self):
    SourceDB = "DataBase.db"
    BackupDB = "DataBase_Backup.db"

    def UpdateBackUp():
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        EncryptBackup(Members.SourceDB, "VeryGoodPassWord")
    
    def RestoreBackup():
        Decrypt("DataBase.dbBackup.enc", "VeryGoodPassWord", Members.SourceDB)
        Encrypt(Members.SourceDB, "VeryGoodPassWord")
    
    def PrintMembers():
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        conn = sqlite3.connect(Members.SourceDB)
        cur = conn.cursor()
        try:
            # cur.execute("SELECT * FROM Logs")`
            print (pd.read_sql_query("SELECT Username, FirstName, LastName, Age, Gender, Weight, Address, City, Email, PhoneNumber, Type,RegistrationDate, MemberID FROM Members", conn))
        except:
            print("No Data found")
        conn.close()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")

    def FindMember(Firstname, Lastname):
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        conn = sqlite3.connect(Members.SourceDB)
        cur = conn.cursor()
        try:
            query = "SELECT * FROM Members WHERE Firstname=? AND Lastname=?"
            params = (Firstname, Lastname)
            # cur.execute(query, params)
            # rows = cur.fetchall()
            df = pd.read_sql_query(query, conn, params=params)
            print(df)
        except:
            print("No member by that name found")
        conn.close()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")