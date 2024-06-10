import os 
from AccountManager import AccountManager
from Database import *
import bcrypt
from LoggedInAccount import *
from datetime import date
# from LogActivity import Logs

class main:

    def start():
        Database.MakeDB()
        # AccountManager.CreateAccount("Testworlds","TestingPassword1!", "Daan", "Polet", "20", "other", "20", "somewhere", "somecity", "Email@Email.Email", "06-24995072")
        main.menu()

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
    
        # Database.InsertAccount(Account("Username","unhashedpassword", "testing", "ing", 20, "other", 20, "somewhere", "somecity", "Email@Email.Email", "06-24995072"))
        # Account.InsertIntoDatabase(Account.Create())
        # main.menu()
    
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
            else:
                # print("oh oh")
                print("1. Create new account")
                print("2. Account information")
                print("3. Log out")
                print()
                choice = input("Enter your choice: ")
                os.system('cls')
                if choice == "1":
                    AccountManager.CreateAccountInput()
                elif choice == "2":
                    LoggedInAccount.CurrentLoggedInAccount.Print()
                elif choice == "3":
                    LoggedInAccount.LogOut()
                input("> ")

        
    def hardcodeAdminAcc():
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       ("admin", bcrypt.hashpw("admin".encode("utf-8"),bcrypt.gensalt()), "admin", "admin", "100", "other", "100", 
                        "admin", "admin", "admin@admkin.admin", "612121212", "SuperAdmin", str(date.today().strftime("%d/%m/%Y")), Account.GenerateId())) # from datetime import date
        connection.commit()
        connection.close()

                

# test insert
# Database.InsertAccount(Account("testing", "ing", 20, "other", 20, "somewhere", "somecity", "Email@Email.Email", 06-24995072))
            
# if not arr[0].isalpha(): print(2);return False
# if not any(char.isdigit() for char in arr[1]): print(3);return False
# if len(arr) == 3:
#     if not (arr[2][:-2].isalpa() & arr[2][-2:].isdigit()): print(4);return False
# elif len(arr) == 3:
#     if not arr[2].isalpha(): return print(5);False
# if len(arr) == 4:
#     if not arr[3].isdigit(): return print(6);False
# return True

if __name__ == '__main__':
    # Logs.PrintLogs()
    main.start()