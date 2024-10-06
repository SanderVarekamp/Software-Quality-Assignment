from datetime import * 
from Account import *
from Database import Database, Members



class LoggedInAccount:
    CurrentLoggedInAccount = None

    def LogOut():
        Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Logging out.", "Logged out.",False)
        LoggedInAccount.CurrentLoggedInAccount = None