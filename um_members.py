import os 
from AccountManager import AccountManager
from Database import *
import bcrypt
from LoggedInAccount import *


class main:

    def start():
        # Encrypt(Members.SourceDB, Members.HardCodePassword)
        # Members.DeleteOldestBackups("Backups")
        Database.AddAllTables()
        main.hardcodeSuperAdmin()  
        main.hardcodeConsultant()  
        #Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        main.menu()

    def menu():   
        while True:     
            os.system('cls')
            if not isinstance(LoggedInAccount.CurrentLoggedInAccount, Account):
                print("Welcome!")
                print("Where would you like to go?")
                print("1. Log in")
                print()
                print("Enter your choice: ")
                choice = input("> ")
                os.system('cls')
                if choice == "1":
                    #Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Going to log in.",False)
                    AccountManager.LogInInput()
                    if bcrypt.checkpw(AccountManager.TempPasswordForReset.encode("utf-8"),bcrypt.gensalt()):
                        AccountManager.ResetPasswordInput(LoggedInAccount.CurrentLoggedInAccount)
            elif LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "superadmin" or LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "admin":
                Members.DeleteOldestBackups("Backups")
                print("1. Create new account")
                print("2. Account information")
                print("3. All user information")
                print("4. Find user (edit and delete)")
                print("5. Show activity log")
                print("6. Make backup")
                print("7. restore backup")
                print("8. Change password")
                print("9. Log out")
                print()
                print("Enter your choice: ")
                choice = input("> ")
                os.system('cls')
                if choice == "1":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Creating a new account.",False)
                    AccountManager.CreateAccountInput()
                elif choice == "2":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Printing account information.",False)
                    LoggedInAccount.CurrentLoggedInAccount.Print()
                    input()
                elif choice == "3":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Looking at all user information",False)
                    Members.PrintMembers()
                    input()
                elif choice == "4":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Searching for user",False)
                    AccountManager.ChangeAccount(LoggedInAccount.CurrentLoggedInAccount)
                elif choice == "5":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Looking at the activity log",False)
                    Database.PrintLogs()
                    print()
                    print("Press Enter to continue")
                    input()
                elif choice == "6":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Creating new backup.",False)
                    Members.UpdateBackUp()
                    print("Created backup")
                    print("Press Enter to continue")
                    input()
                elif choice == "7":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Restoring backup.",False)
                    Members.RestoreBackup()
                    if AccountManager.SearchAccountForce(LoggedInAccount.CurrentLoggedInAccount.Username).Username != LoggedInAccount.CurrentLoggedInAccount.Username:
                        print("Account not found, logging out")
                        LoggedInAccount.LogOut()
                elif choice == "8":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Changing password",False)
                    AccountManager.ChangePasswordInput()
                elif choice == "9":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Logging out.",False)
                    LoggedInAccount.LogOut()
                    print("Logged out")
                
            
            elif LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "consultant":
                print("1. Create new account")
                print("2. Account information")
                print("3. Find user")
                print("4. Change Password")
                print("5. Log out")
                print()
                print("Enter your choice: ")
                choice = input("> ")
                os.system('cls')
                if choice == "1":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Creating a new account.",False)
                    AccountManager.CreateAccountInput()
                elif choice == "2":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Printing account information.",False)
                    LoggedInAccount.CurrentLoggedInAccount.Print()
                elif choice == "3":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Searching for user",False)
                    AccountManager.ChangeAccount(LoggedInAccount.CurrentLoggedInAccount)
                elif choice == "4":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Changing password",False)
                    AccountManager.ChangePasswordInput()
                elif choice == "5":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Logging out.",False)
                    LoggedInAccount.LogOut()

            else:
                print("1. Log out")
                print()
                print("Enter your choice: ")
                choice = input("> ")
                if choice == "1":
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Logging out.",False)
                    LoggedInAccount.LogOut()
                

        
    def hardcodeSuperAdmin():
        # Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        # connection = sqlite3.connect(Members.SourceDB)
        # cursor = connection.cursor()
        # cursor.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        #                ("super_admin", bcrypt.hashpw("Admin_123?".encode("utf-8"),bcrypt.gensalt()), "admin", "admin", "100", "other", "100", 
        #                 "admin", "admin", "admin@hr.nl", "0107944000", "SuperAdmin", str(date.today().strftime("%d/%m/%Y")), 1)) # from datetime import date
        # connection.commit()
        # connection.close()
        # Encrypt(Members.SourceDB, Members.HardCodePassword)
        account = Account("super_admin", bcrypt.hashpw("Admin_123?".encode("utf-8"),bcrypt.gensalt()), "admin", "admin", "100", "other", "100", "admin", "admin", "admin@hr.nl", "0107944000", "SuperAdmin", str(date.today().strftime("%d/%m/%Y")), 1)
        EncryptNew().encrypt_member(account)

    def hardcodeAdmin():
        # Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        # connection = sqlite3.connect(Members.SourceDB)
        # cursor = connection.cursor()
        # cursor.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        #                ("admin", bcrypt.hashpw("admin".encode("utf-8"),bcrypt.gensalt()), "admin", "admin", "100", "other", "100", 
        #                 "admin", "admin", "admin@hr.nl", "0107944000", "Admin", str(date.today().strftime("%d/%m/%Y")), 1)) # from datetime import date
        # connection.commit()
        # connection.close()
        # Encrypt(Members.SourceDB, Members.HardCodePassword)
        account = Account("admin", bcrypt.hashpw("admin".encode("utf-8"),bcrypt.gensalt()), "admin", "admin", "100", "other", "100", "admin", "admin", "admin@hr.nl", "0107944000", "Admin", str(date.today().strftime("%d/%m/%Y")), 1)
        EncryptNew().encrypt_member(account)

    def hardcodeConsultant():
        # Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        # connection = sqlite3.connect(Members.SourceDB)
        # cursor = connection.cursor()
        # cursor.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        #                ("consultant", bcrypt.hashpw("consultant".encode("utf-8"),bcrypt.gensalt()), "admin", "admin", "100", "other", "100", 
        #                 "admin", "admin", "admin@hr.nl", "0107944000", "Admin", str(date.today().strftime("%d/%m/%Y")), 1)) # from datetime import date
        # connection.commit()
        # connection.close()
        # Encrypt(Members.SourceDB, Members.HardCodePassword)
        account = Account("consultant", bcrypt.hashpw("consultant".encode("utf-8"),bcrypt.gensalt()), "admin", "admin", "100", "other", "100", "admin", "admin", "admin@hr.nl", "0107944000", "Admin", str(date.today().strftime("%d/%m/%Y")), 1)
        EncryptNew().encrypt_member(account)   

if __name__ == '__main__':
    main.start()

    