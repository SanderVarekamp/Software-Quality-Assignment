import sqlite3
class Database:

    def MakeDB():
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
    