import sqlite3
import bcrypt

from Account import *


class LoggedInAccount:
    CurrentLoggedInAccount = None

    def LogOut():
        LoggedInAccount.CurrentLoggedInAccount = None

    def LogIn(Username, Password):
        if not isinstance(Username, str) or not isinstance(Password, str): 
            return False, "Login credentials are of incorrect format."
        
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Members WHERE Username = ?", (Username,))
        rows = cursor.fetchone()
        connection.close()

        if rows is None or not bcrypt.checkpw(Password.encode("utf-8"),rows[1]): 
            return False, "Login credentials are incorrect."

        account = Account(rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7],rows[8],rows[9],rows[10], rows[11])
        LoggedInAccount.CurrentLoggedInAccount = account
        return True, "Logged in."
        
        # if rows is not None:
        #     # main.LoggedInAccount = Account(rows)
            # account = Account(rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7],rows[8],rows[9],rows[10], rows[11])
        #     LoggedInAccount.CurrentLoggedInAccount = account
        #     return True, "Logged in."
        # return False, "Login credentials are incorrect."
    
    # def LogIn(Username, Password):
    #     connection = sqlite3.connect("DataBase.db")
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT * FROM Members WHERE Username = ? AND PasswordHash = ?", (Username, Password))
    #     rows = cursor.fetchone()
    #     connection.close()
    #     if rows is not None:
    #         # main.LoggedInAccount = Account(rows)
    #         account = Account(rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7],rows[8],rows[9],rows[10], rows[11])
    #         LoggedInAccount.CurrentLoggedInAccount = account
    #         return True, "Logged in."
    #     return False, "Login credentials are incorrect."
    

    def LogInInput():
        
        print("What is your username?")
        username = input("> ")
        print("What is your password?")
        password = input("> ")
        LoggedIn, message = LoggedInAccount.LogIn(username, password)
        print(message)
        if not LoggedIn:
            LoggedInAccount.LogInInput()