import sqlite3
from datetime import datetime
from Account import *
import pandas as pd
import os
import re
import glob
from Encrypt import *

class Database:
    def AddAllTables():
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
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
      print (pd.read_sql_query("SELECT * FROM ActivityLog", conn))
      conn.close()
      Encrypt(Members.SourceDB, "VeryGoodPassWord")

class Members:
    # def __init__(self):
    SourceDB = "DataBase.db"
    BackupDB = "DataBase_Backup.db"

    def UpdateBackUp():
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        EncryptBackup(Members.SourceDB, "VeryGoodPassWord")
    
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
            value = input("What backup do you want to restore?(0 for most recent)(return to return to main menu)")
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
        Decrypt(encrypted_file_path, "VeryGoodPassWord", Members.SourceDB)
        Encrypt(Members.SourceDB, "VeryGoodPassWord")
        print("Backup restored")

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

    def SearchAccount(quary):
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        search_pattern = f"%{quary}%"
        cursor.execute("""SELECT * FROM Members WHERE 
                        Username LIKE ? OR
                        PasswordHash LIKE ? OR
                        FirstName LIKE ? OR
                        LastName LIKE ? OR
                        Age LIKE ? OR
                        Gender LIKE ? OR
                        Weight LIKE ? OR
                        Address LIKE ? OR
                        City LIKE ? OR
                        Email LIKE ? OR
                        PhoneNumber LIKE ? OR
                        Type LIKE ? OR
                        RegistrationDate LIKE ? OR
                        MemberID LIKE ? LIMIT 1""",
                    (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern,
                        search_pattern, search_pattern, search_pattern, search_pattern, search_pattern,
                        search_pattern, search_pattern, search_pattern, search_pattern))
        row = cursor.fetchone()
        connection.close()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")
        if row:
            account = Account(
                Username=row[0],
                PasswordHash=row[1],
                FirstName=row[2],
                LastName=row[3],
                Age=row[4],
                Gender=row[5],
                Weight=row[6],
                Address=row[7],
                City=row[8],
                Email=row[9],
                PhoneNumb=row[10],
                Type=row[11]
            )
            account.RegistrationDate = row[12]
            account.MemberID = row[13]
            return account
        else:
            return None
        
    def DeleteAccount(account):
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        if not isinstance(account, Account):
            raise ValueError("Expected an Account instance")
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Members WHERE MemberID = ?", (account.MemberID,))
        connection.commit()
        connection.close()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")


    def EditAccount(account):
        if not isinstance(account, Account):
            raise ValueError("Expected an Account instance")
        print("="* 30)
        print("What would u like to change? ")
        print("1. First Name:")
        print("2. Last Name:")
        print("3. Age:")
        print("4. Gender:")
        print("5. Weight:")
        print("6. Address:")
        print("7. City:")
        print("8. Email:")
        print("9. Phone Number:")  

        option = input("Choose an option to update (1-9): ")
        fields = ["FirstName", "LastName", "Age", "Gender", "Weight", "Address", "City", "Email", "PhoneNumb"]

        if option in [str(i) for i in range(1, 10)]:
            field = fields[int(option) - 1]
            new_value = input(f"What would you like to change {field} to: ")
            Members.UpdateMemberData(account.MemberID, field, new_value)
            print(f"{field} has been updated.")
        else:
            print("Invalid option selected.")

    def UpdateMemberData(MemberID, field, new_value):
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        with sqlite3.connect('DataBase.db') as conn:
            cur = conn.cursor()
            query = f"UPDATE Members SET {field} = ? WHERE MemberID = ?"
            cur.execute(query, (new_value, MemberID))
            conn.commit()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")

    def ChangeAccount(LoggedinAccount):
        AccountToFind = input("Enter account detail: ")
        Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Selecting from menu options.", f"Looking up {AccountToFind}",False)
        member = Members.SearchAccount(AccountToFind)
        if member != None:
            loop = True
            if (LoggedinAccount.Type.lower() == "superadmin"):
                if member.Type.lower() == "superadmin" :
                    loop = False
            elif (LoggedinAccount.Type.lower() == "admin"):
                if member.Type.lower() == "superadmin" or  member.Type.lower() == "admin":
                    loop = False
            elif (LoggedinAccount.Type.lower() == "consultant"):
                if member.Type.lower() != "member":
                    loop = False

            if loop:
                if LoggedinAccount.Type.lower() == "superadmin" or LoggedinAccount.Type.lower() == "admin":
                    Members.ChoiceAdmin(member, LoggedinAccount, loop)
                elif LoggedinAccount.Type.lower() == "consultant":
                    Members.ChoiceConsultant(member, LoggedinAccount, loop)
            else:
                print("No account found")
    
    def ChoiceAdmin(member, LoggedinAccount, loop):
        while loop:
            print("Found account:")
            member.Print()
            print("1. Return")
            print("2. Edit account")
            print("3. Delete account")
            print("4. Reset password")
            choice2 = input("Enter your choice: ")
            if choice2 == "1":
                loop = False
            elif choice2 == "2":
                Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Selecting from menu options.", f"Editing {member.Username}",False)
                loop = False
                Members.EditAccount(member)
            elif choice2 == "3":
                Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Selecting from menu options.", f"Deleting {member.Username}",False)
                Members.DeleteAccount(member)
                print("Account succesfully deleted!")
                input()
                loop = False
            elif choice2 == "4":
                print("WIP")
                input()
                loop = False
            else:
                print("Invalid input")
                input()

    def ChoiceConsultant(member, LoggedinAccount, loop):
        while loop:
            print("Found account:")
            member.Print()
            print("1. Return")
            print("2. Edit account")
            choice2 = input("Enter your choice: ")
            if choice2 == "1":
                loop = False
                return
            elif choice2 == "2":
                Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Selecting from menu options.", f"Editing {member.Username}",False)
                loop = False
                Members.EditAccount(member)
            else:
                print("Invalid input")
                input()