import sqlite3
import bcrypt
from datetime import * 
from Account import *
from Database import Database, Members



class LoggedInAccount:
    CurrentLoggedInAccount = None

    FailedLogInCounter = 0
    MaxLogInFails = 3
    StandardTimeCooldownSeconds = 5
    CurrentTimeCooldownSeconds = StandardTimeCooldownSeconds
    UnblockTime = datetime.now()

    def LogOut():
        Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Logging out.", "Logged out.",False)
        LoggedInAccount.CurrentLoggedInAccount = None

    def LogIn(Username, Password):
        result = None
        message = None
        
        if LoggedInAccount.UnblockTime > datetime.now():
            timedif = LoggedInAccount.UnblockTime - datetime.now()
            return False, "Too many failed attempts. try again in "+str(timedif).split(".")[0]+" seconds."

        if not isinstance(Username, str) or not isinstance(Password, str): 
            result = False
            message = "Login credentials are incorrect."
        
        else:
            Decrypt("DataBase.db.enc", "VeryGoodPassWord", Members.SourceDB)
            connection = sqlite3.connect("DataBase.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Members WHERE Username = ?", (Username,))
            rows = cursor.fetchone()
            connection.close()
            Encrypt(Members.SourceDB, "VeryGoodPassWord")

            if rows is None or not bcrypt.checkpw(Password.encode("utf-8"),rows[1]): 
                result = False
                message = "Login credentials are incorrect."
            else:
                account = Account(rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7],rows[8],rows[9],rows[10], rows[11])
                LoggedInAccount.CurrentLoggedInAccount = account
                Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Logging in.", "Logged in.",False)
                result = True
                message = "Logged in."
        if result == True:
            LoggedInAccount.FailedLogInCounter = 0
            LoggedInAccount.CurrentTimeCooldownSeconds = LoggedInAccount.StandardTimeCooldownSeconds
        else:
            LoggedInAccount.FailedLogInCounter += 1 

        if LoggedInAccount.FailedLogInCounter >= LoggedInAccount.MaxLogInFails:
            LoggedInAccount.UnblockTime = datetime.now() + timedelta(seconds=LoggedInAccount.CurrentTimeCooldownSeconds)
            timedif = LoggedInAccount.UnblockTime - datetime.now()
            Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Logging in", "Too many failed attempts. "+str(timedif).split(".")[0]+" seconds cooldown.",True)
            message += " Too many failed attempts. try again in "+str(timedif).split(".")[0]+" seconds."
            LoggedInAccount.FailedLogInCounter -= 1
            LoggedInAccount.CurrentTimeCooldownSeconds *= 2

        return result, message

    def LogInInput():
        print("What is your username?")
        username = input("> ")
        print("What is your password?")
        password = input("> ")
        LoggedIn, message = LoggedInAccount.LogIn(username, password)
        print(message)
        print()
        if not LoggedIn:
            LoggedInAccount.LogInInput()