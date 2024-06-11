import sqlite3
class Database:
    
    def AddAllTables():
       Database.AddTableMembers()
       Database.AddTableLog()

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
  