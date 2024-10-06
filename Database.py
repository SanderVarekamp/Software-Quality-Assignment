import sqlite3
from datetime import *
from Account import *
import pandas as pd
import os
import re
import glob
from Encrypt import *

class Database:
    def AddAllTables():
        Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        Database.AddTableMembers()
        Database.AddTableLog()
        Encrypt(Members.SourceDB, Members.HardCodePassword)

    def AddTableMembers():
        connection = sqlite3.connect(Members.SourceDB)
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
      connection = sqlite3.connect(Members.SourceDB)
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

    def SelectFromDatabase(query, fetchAll, input = None):
        Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        try:
            connection = sqlite3.connect(Members.SourceDB)
            cursor = connection.cursor()
            try:
                FullQuery = "SELECT "+query
                if(input is None):
                    cursor.execute(FullQuery)
                else:
                    cursor.execute(FullQuery, input)
                if(fetchAll):
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
            except:
                result = ""
            connection.close()
            return result
        except:
            None
        Encrypt(Members.SourceDB, Members.HardCodePassword)

    def LogAction(username: str, activity: str, info: str, sus: bool):
        max_retries = 5
        retry_delay = 0.1
        timeout = 30

        for attempt in range(max_retries):
            try:
                Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
                now = datetime.now()
                time_str = now.strftime("%H:%M:%S")
                date_str = now.strftime("%d/%m/%Y")

                connection = sqlite3.connect(Members.SourceDB, timeout=timeout)
                connection.execute("PRAGMA journal_mode=WAL")
                cursor = connection.cursor()
                

                cursor.execute("INSERT INTO ActivityLog VALUES (?, ?, ?, ?, ?, ?)", 
                               (str(date_str), str(time_str), username, activity, info, sus))
                connection.commit()
                connection.close()
                Encrypt(Members.SourceDB, Members.HardCodePassword)
                break 
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        print(f"Failed to log action after {max_retries} attempts due to a locked database.")
                        raise
                else:
                    raise
            finally:
                try:
                    connection.close()
                except Exception as close_err:
                    print(f"Error closing the database connection: {close_err}")

    def PrintLogs():
      Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
      conn = sqlite3.connect(Members.SourceDB)
      print (pd.read_sql_query("SELECT * FROM ActivityLog", conn))
      conn.close()
      Encrypt(Members.SourceDB, Members.HardCodePassword)

class Members:
    SourceDB = "DataBase.db"
    EncryptedDB = "DataBase.db.enc"
    BackupDB = "DataBase_Backup.db"
    HardCodePassword = "VeryGoodPassWord"
    def UpdateBackUp():
        Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        EncryptBackup(Members.SourceDB, Members.HardCodePassword)
    
    def DeleteOldestBackups(directory, MaxBackups = 10):
        while True:
            file_list = glob.glob(os.path.join(directory, '*'))
            if len(file_list) <= MaxBackups:
                break
            oldest_file = Members.GetOldestsFile(directory)
            if oldest_file:
                os.remove(oldest_file)
                print(f"Deleted {oldest_file}")
            else:
                break
    
    def GetOldestsFile(directory):
        file_list = glob.glob(os.path.join(directory, '*'))
        pattern = re.compile(r'(\d{6})\.(\d+)\.dbBackup\.enc\.zip')
        oldest_file = None
        lowest_date = float('inf')
        lowest_order = float('inf')
        
        for file_path in file_list:
            file_name = os.path.basename(file_path)
            match = pattern.match(file_name)
            if match:
                date = int(match.group(1))
                order = int(match.group(2))
                if (date < lowest_date) or (date == lowest_date and order < lowest_order):
                    lowest_date = date
                    lowest_order = order
                    oldest_file = file_path
        return oldest_file
    
    def GetMostRecentFile(directory):
        file_list = glob.glob(os.path.join(directory, '*'))
        pattern = re.compile(r'(\d{6})\.(\d+)\.dbBackup\.enc\.zip')
        
        most_recent_file = None
        highest_date = -1
        highest_order = -1
        
        for file_path in file_list:
            file_name = os.path.basename(file_path)
            match = pattern.match(file_name)
            if match:
                date = int(match.group(1))
                order = int(match.group(2))
                if (date > highest_date) or (date == highest_date and order > highest_order):
                    highest_date = date
                    highest_order = order
                    most_recent_file = file_name
        
        return most_recent_file
    
    def RestoreBackup():
        files = glob.glob(os.path.join("Backups", '*'))
        count = 0
        filesdict = {}
        for file_path in files:
            count = count+1
            if os.path.isfile(file_path):
                filesdict[str(count)] = os.path.basename(file_path)
                print(str(count) + ". "+ os.path.basename(file_path))

        check = True
        name = None
        if len(files) <= 0:
            print("No backups found")
            return
        while check:
            print("What backup do you want to restore? (0 for most recent) (return to return to main menu)")
            value = input("> ")
            if value == "0":
                name = Members.GetMostRecentFile("Backups")
                check = False
            elif value.lower() == "return":
                check = False
                return
            else:
                for x in range(count):
                    if value == str(x+1):
                        name = filesdict[value]
                        check = False
            if name == None:
                print("No file found, try again")

        encrypted_file_path = "Backups/" + name
        Decrypt(encrypted_file_path, Members.HardCodePassword, Members.SourceDB)
        Encrypt(Members.SourceDB, Members.HardCodePassword)
        print("Backup restored")

    def PrintMembers():
        Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        conn = sqlite3.connect(Members.SourceDB)
        cur = conn.cursor()
        try:
            print (pd.read_sql_query("SELECT Username, FirstName, LastName, Age, Gender, Weight, Address, City, Email, PhoneNumber, Type,RegistrationDate, MemberID FROM Members", conn))
        except:
            print("No Data found")
        conn.close()
        Encrypt(Members.SourceDB, Members.HardCodePassword)