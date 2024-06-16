import os 
from AccountManager import AccountManager
from Database import *
import bcrypt
from LoggedInAccount import *
from Encrypt import *

# from LogActivity import Logs

class main:

    def start():
        Members.DeleteOldestBackups("Backups")
        # Members.RestoreBackup()
        Database.AddAllTables()
        main.hardcodeAdminAcc()     
        main.menu()

    def menu():   
        while True:     
            os.system('cls')
            if not isinstance(LoggedInAccount.CurrentLoggedInAccount, Account):
                print("Welcome!")
                print("Where would you like to go?")
                print("1. Log in")
                print()
                choice = input("Enter your choice: ")
                os.system('cls')
                if choice == "1":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Going to log in.",False)
                    LoggedInAccount.LogInInput()
            elif LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "superadmin" or LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "admin":
                Members.DeleteOldestBackups("Backups")
                print("1. Create new account")
                print("2. Account information")
                print("3. All user information")
                print("4. Find user(edit and delete)")
                print("5. Show activity log")
                print("6. Make backup")
                print("7. restore backup")
                print("8. Change password")
                print("9. Log out")
                print()
                choice = input("Enter your choice: ")
                os.system('cls')
                if choice == "1":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Creating a new account.",False)
                    AccountManager.CreateAccountInput()
                elif choice == "2":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Printing account information.",False)
                    LoggedInAccount.CurrentLoggedInAccount.Print()
                elif choice == "3":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Looking at all user information",False)
                    Members.PrintMembers()
                elif choice == "4":
                    Members.ChangeAccount(LoggedInAccount.CurrentLoggedInAccount)
                elif choice == "5":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Looking at the activity log",False)
                    Database.PrintLogs()
                elif choice == "6":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Creating new backup.",False)
                    Members.UpdateBackUp()
                    print("Created backup")
                elif choice == "7":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Restoring backup.",False)
                    Members.RestoreBackup()
                elif choice == "8":
                    print("WIP")
                elif choice == "9":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Logging out.",False)
                    LoggedInAccount.LogOut()
                    print("Logged out")
                input()
            
            elif LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "consultant":
                print("1. Create new account")
                print("2. Account information")
                print("3. Find Member")
                print("4. Change Password")
                print("5. Log out")
                print()
                choice = input("Enter your choice: ")
                os.system('cls')
                if choice == "1":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Creating a new account.",False)
                    AccountManager.CreateAccountInput()
                elif choice == "2":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Printing account information.",False)
                    LoggedInAccount.CurrentLoggedInAccount.Print()
                elif choice == "3":
                    Members.ChangeAccount(LoggedInAccount.CurrentLoggedInAccount)
                elif choice == "4":
                    print("WIP")
                elif choice == "5":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Logging out.",False)
                    LoggedInAccount.LogOut()
                input()
            else:
                print("1. Log out")
                print()
                choice = input("Enter your choice: ")
                if choice == "1":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Logging out.",False)
                    LoggedInAccount.LogOut()
                input()

        
    def hardcodeAdminAcc():
        Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       ("admin", bcrypt.hashpw("admin".encode("utf-8"),bcrypt.gensalt()), "admin", "admin", "100", "other", "100", 
                        "admin", "admin", "admin@admin.admin", "612121212", "SuperAdmin", str(date.today().strftime("%d/%m/%Y")), 0)) # from datetime import date
        connection.commit()
        connection.close()
        Encrypt(Members.SourceDB, "VeryGoodPassWord")
        #super_admin, password: Admin_123?

if __name__ == '__main__':
    main.start()