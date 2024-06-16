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
        # input()
        # Encrypt("DataBase.db", "VeryGoodPassWord")
        # input()
        # Decrypt("DataBase.db.enc", "VeryGoodPassWord", "DataBase.db")
        # Members.UpdateBackUp()
        # Members.PrintMembers()

        
        main.menu()

    # example incrypting database and making a backup of database
    # Encrypted = Encrypt("DataBase.db", "VeryGoodPassWord")
    # Decrypt(Encrypted, "VeryGoodPassWord", "DataBase.db")
    # member = Members()
    # member.UpdateBackUp()
    # Decrypt("DataBase_Backup.db.enc", "VeryGoodPassWord", member.BackupDB)
    #       
    
    # def tim():
    #     now = datetime.datetime.now()
    #     later = now + datetime.timedelta(seconds=5)
    #     earlier = now - datetime.timedelta(seconds=5)
    #     print(earlier)
    #     print(now)
    #     print(later)
    #     print(earlier > now)
    #     print(earlier < now)
    #     print(now > later)
    #     print(now < later)
    #     print(earlier > later)
    #     print(earlier < later)
    #     timedif = later-earlier
    #     print(timedif)
    #     print(f"hello {timedif.total_seconds()}")
    #     print("hello "+str(timedif))
        

        # AccountManager.CreateAccount("Testworlds","TestingPassword1!", "Daan", "Polet", "20", "other", "20", "somewhere", "somecity", "Email@Email.Email", "06-24995072")
        # LoggedInAccount.LogIn("admin", "admin")
        # AccountManager.CreateAccount(input(),"TestingPassword1!", "Daan", "Polet", "20", "other", "20", "somewhere", "somecity", "Email@Email.Email", "06-24995072", "admin")


    # def testHash():
    #     password = "Hello"
    #     byte = bytes(password, 'utf-8')
    #     tohash = b""+ byte
    #     salt = bcrypt.gensalt()
    #     hashed = bcrypt.hashpw(tohash, salt)
    #     print(password)
    #     print(byte)
    #     print(tohash)
    #     print(salt)
    #     print(hashed)

    
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
                    # print("WIP")
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", "Going to log in.",False)
                    LoggedInAccount.LogInInput()
                    # account1 = Account("testing", "ing","unhashedpassword", 20, "other", 20, "somewhere", "somecity", "Email@Email.Email", "06-24995072")

                    # Database.InsertAccount(account1)
                    # account1.Print()

            # elif LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "consultant":
            #     print("Logged in!")
            #     LoggedInAccount.CurrentLoggedInAccount.Print()
            #     input("> ")
            # elif LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "member":
            #     print("good i think")
            #     input("> ")
            elif LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "superadmin":
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
                    AccountToFind = input("Enter account detail: ")
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", f"Looking up {AccountToFind}",False)
                    member = Members.SearchAccount(AccountToFind)
                    if member != None:
                        if member.Type.lower() != "superadmin" :
                            loop = True
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
                                    main.menu()
                                elif choice2 == "2":
                                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", f"Editing {member.Username}",False)
                                    loop = False
                                    Members.EditAccount(member)
                                elif choice2 == "3":
                                    loop = False
                                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", f"Deleting {member.Username}",False)
                                    Members.DeleteAccount(member)
                                    print("Account succesfully deleted!")
                                    input()
                                elif choice2 == "4":
                                    print("WIP")
                                else:
                                    print("Invalid input")
                                    input()
                        else:
                            print("No account found")
                    else:
                        print("No account found")
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

            elif LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "admin":
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
                    AccountToFind = input("Enter account detail: ")
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", f"Looking up {AccountToFind}",False)
                    member = Members.SearchAccount(AccountToFind)
                    if member != None:
                        if member.Type.lower() != "superadmin" and member.Type.lower != "admin" :
                            loop = True
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
                                    main.menu()
                                elif choice2 == "2":
                                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", f"Editing {member.Username}",False)
                                    loop = False
                                    Members.EditAccount(member)
                                elif choice2 == "3":
                                    loop = False
                                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", f"Deleting {member.Username}",False)
                                    Members.DeleteAccount(member)
                                    print("Account succesfully deleted!")
                                    input()
                                elif choice2 == "4":
                                    print("WIP")
                                else:
                                    print("Invalid input")
                                    input()
                        else:
                            print("No account found")
                    else:
                        print("No account found")
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
                print("4. Update Password")
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
                    AccountToFind = input("Enter account detail: ")
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", f"Looking up {AccountToFind}",False)
                    member = Members.SearchAccount(AccountToFind)
                    if member != None:
                        if member.Type.lower() == "member" :
                            loop = True
                            while loop:
                                print("Found account:")
                                member.Print()
                                print("1. Return")
                                print("2. Edit account")
                                choice2 = input("Enter your choice: ")
                                if choice2 == "1":
                                    loop = False
                                    main.menu()
                                elif choice2 == "2":
                                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Selecting from menu options.", f"Editing {member.Username}",False)
                                    loop = False
                                    Members.EditAccount(member)
                                else:
                                    print("Invalid input")
                                    input()
                        else:
                            print("No account found")
                    else:
                        print("No account found")
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