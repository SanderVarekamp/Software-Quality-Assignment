import os 
from AccountManager import AccountManager
from Database import *
import bcrypt
from LoggedInAccount import *
from Encrypt import *


class main:

    def start():
        Members.DeleteOldestBackups("Backups")
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
                    if bcrypt.checkpw(AccountManager.TempPasswordForReset.encode("utf-8"),bcrypt.gensalt()):
                        AccountManager.ResetPasswordInput(LoggedInAccount.CurrentLoggedInAccount)
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
                    AccountManager.ChangeAccount(LoggedInAccount.CurrentLoggedInAccount)
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
                    AccountManager.ChangePasswordInput()
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
                    AccountManager.ChangeAccount(LoggedInAccount.CurrentLoggedInAccount)
                elif choice == "4":
                    AccountManager.ChangePasswordInput()
                elif choice == "5":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Logging out.",False)
                    LoggedInAccount.LogOut()
                print()
                print("Press Enter to continue ")
                input()
            else:
                print("1. Log out")
                print()
                choice = input("Enter your choice: ")
                if choice == "1":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Logging out.",False)
                    LoggedInAccount.LogOut()

                print()
                print("Press Enter to continue ")
                input()
                

        
    def hardcodeAdminAcc():
        Decrypt("DataBase.db.enc", Members.HardCodePassword, Members.SourceDB)
        connection = sqlite3.connect(Members.SourceDB)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       ("super_admin", bcrypt.hashpw("Admin_123?".encode("utf-8"),bcrypt.gensalt()), "admin", "admin", "100", "other", "100", 
                        "admin", "admin", "admin@hr.nl", "0107944000", "SuperAdmin", str(date.today().strftime("%d/%m/%Y")), 1)) # from datetime import date
        connection.commit()
        connection.close()
        Encrypt(Members.SourceDB, Members.HardCodePassword)
   

if __name__ == '__main__':
    main.start()
    