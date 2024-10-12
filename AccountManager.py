import os
import re
import sqlite3
import bcrypt
from Account import *
from LoggedInAccount import *
from Database import Members
from Encrypt2 import EncryptNew
class AccountManager:
    
    FailedLogInCounter = 0
    MaxLogInFails = 3
    StandardTimeCooldownSeconds = 5
    CurrentTimeCooldownSeconds = StandardTimeCooldownSeconds
    UnblockTime = datetime.now()

    def Is_Valid_FirstName(firstname):
        if(len(firstname) < 20):
            if(firstname.isalpha()): 
                return True
        return False
    
    def Is_Valid_LastName(lastname):
        if(len(lastname) < 20):
            if(lastname.isalpha()): 
                return True
        return False
    
    def Is_Valid_age(age):
        if(isinstance(age, int) or age.isdigit()):
            if(0 < int(age) < 150):
                return True
        return False
    
    def Is_Valid_gender(gender):
        if(gender.lower() in ['male', 'female', 'other']):
            return True        
        return False
    
    def Is_Valid_weight(weight):
        if(weight.replace('.', '', 1).isdigit()):
            if(0 < float(weight) < 1000):
                return True
        return False
    
    def Is_Valid_Address(address):
        if(len(address) < 50):
            pattern = re.compile(r'^[A-Za-z\s]+ \d+[a-zA-Z]? \d{4}[A-Z]{2}$')
            if(bool(pattern.match(address))):
                return True
        return False
    
    def Is_Valid_City(city):
        if(len(city) < 30):
            words = city.split()
            if(all(word.isalpha() for word in words)):
                return True
        return False
    
    def Is_Valid_email(email):
        if(len(email) < 50):
            pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
            if(bool(re.match(pattern, email))):
                return True
        return False
    
    def Is_Valid_phone(phone):
        if(len(phone) < 15):
            pattern1 = re.compile(r"6-\d{8}$")
            pattern2 = re.compile(r"6\d{8}$")
            if(bool(re.match(pattern1, phone))):
                return True
            if(bool(re.match(pattern2, phone))):
                return True
        return False

    def Is_Valid_Username(username):
        username = username.lower()
        if(7 < len(username) < 11): # username at least 8 characters and no longer than 10
            if(re.match(r'^[a-z_]', username)): # Username must start with a letter or underscore
                if(re.match(r'^[a-z0-9_\'\.]+$', username)): # Username can only contain letters, numbers, underscores, apostrophes, and periods
                    return True
        return False
    
    def UsernameCheck(username):
        if(AccountManager.Is_Valid_Username(username)):
            ExistingUsernames = Database.SelectFromDatabase("Username FROM Members", True)
            if(username not in ExistingUsernames): # username doesnt exist yet
                return True
        return False



    
    def Is_Valid_Password(password):
        special_characters = r'~!@#$%&_\-+=`|\(\){}\[\]:;\'<>,\.?/'
        if(11 < len(password) < 31): # password at least 12 characters and no longer than 30
            if(re.search(r'[a-z]', password)): # Password must contain at least one lowercase letter
                if(re.search(r'[A-Z]', password)): # Password must contain at least one uppercase letter
                    if(re.search(r'\d', password)): # Password must contain at least one digit
                        if(re.search(f"[{re.escape(special_characters)}]", password)): # Password must contain at least one special character
                            return True
        return False

    def Is_Valid_AccountType(type):
        AccountTypeList = ['member', 'consultant', 'admin']
        if(type.lower() in AccountTypeList):
            return True
        return False
    
    def AccountTypeCheck(type):
        if(AccountManager.Is_Valid_AccountType(type)):
            if isinstance(LoggedInAccount.CurrentLoggedInAccount, Account):
                AccountTypeList = ['member', 'consultant', 'admin']
                if LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "admin": 
                    AccountTypeList.remove("admin")
                elif LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "consultant": 
                    AccountTypeList.remove("admin")
                    AccountTypeList.remove("consultant")

                if(type.lower() in AccountTypeList):
                    return True
        return False
 
    def InputAfterValidation(prompt, validation_func, requirement):
            while True:
                print("What is the users "+prompt+"? "+requirement)
                value = input("> ")
                result = validation_func(value)
                if result:
                    return value

    def CreateAccountInput():
        if not isinstance(LoggedInAccount.CurrentLoggedInAccount, Account): return
        AccountType = "Member" if LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "consultant" else AccountManager.InputAfterValidation("account type",AccountManager.AccountTypeCheck,"Please enter "+("'member', 'consultant' or 'admin'." if LoggedInAccount.CurrentLoggedInAccount.Type.lower() == "superadmin" else "'member' or 'consultant'."))

        Username = AccountManager.InputAfterValidation("username", AccountManager.UsernameCheck, "Must be between 8 and 10 characters long and can only contain letters, numbers, underscores, apostrophes, and periods. Must start with letter or underscore.")
        Password = AccountManager.InputAfterValidation("password", AccountManager.Is_Valid_Password, "Must be between 12 and 30 characters long and must contain at least 1 lowercase, uppercase, digit and special character.")
        FirstName = AccountManager.InputAfterValidation("first name", AccountManager.Is_Valid_FirstName, "")
        LastName = AccountManager.InputAfterValidation("last name", AccountManager.Is_Valid_LastName, "")
        if AccountType.lower() != "consultant" and AccountType.lower() != "admin":
            Age = AccountManager.InputAfterValidation("age", AccountManager.Is_Valid_age, "")
            Gender = AccountManager.InputAfterValidation("gender", AccountManager.Is_Valid_gender, "Please enter 'male', 'female', or 'other'.")
            Weight = AccountManager.InputAfterValidation("weight", AccountManager.Is_Valid_weight, "")
            Address = AccountManager.InputAfterValidation("address", AccountManager.Is_Valid_Address, "Please enter your street name, house number and postal code")
            City = AccountManager.InputAfterValidation("city", AccountManager.Is_Valid_City, "")
            Email = AccountManager.InputAfterValidation("email", AccountManager.Is_Valid_email, "")
            PhoneNumb = AccountManager.InputAfterValidation("phone number", AccountManager.Is_Valid_phone, "(6-XXXXXXXX) or (6XXXXXXXX)")
        else:
            Age = None
            Gender = None
            Weight = None
            Address = None
            City =  None
            Email = None
            PhoneNumb = None
        AccountManager.CreateAccount(Username, Password, FirstName.capitalize(), LastName.capitalize(), Age, Gender, Weight, Address, City, Email, PhoneNumb, AccountType)
        input()

    def CreateAccount(Username, Password, FirstName, LastName, Age, Gender, Weight, Address, City, Email, NewPhoneNumb, Type = "Member"):
        if(AccountManager.UsernameCheck(Username)):
            if(AccountManager.Is_Valid_Password(Password)):
                if(AccountManager.Is_Valid_FirstName(FirstName)):
                    if(AccountManager.Is_Valid_LastName(LastName)):
                        if(Type.lower() == "member"):
                            if(AccountManager.Is_Valid_age(Age)):
                                if(AccountManager.Is_Valid_gender(Gender)):
                                    if(AccountManager.Is_Valid_weight(Weight)):
                                        if(AccountManager.Is_Valid_Address(Address)):
                                            if(AccountManager.Is_Valid_City(City)):
                                                if(AccountManager.Is_Valid_email(Email)):
                                                    if(AccountManager.Is_Valid_phone(NewPhoneNumb)):
                                                        NewPhoneNumb = f"31-{NewPhoneNumb}"
                                                        salt = bcrypt.gensalt()
                                                        Password = bcrypt.hashpw(bytes(Password, 'utf-8'), salt)
                                                        NewAccount = Account(Username, Password, FirstName.capitalize(), LastName.capitalize(), Age, Gender, Weight, Address, City, Email, NewPhoneNumb, Type)
                                                        AccountManager.InsertIntoDatabase(NewAccount)
                                                        Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Creating account", f"Made account with username: {Username}",False)
                                                        print("Account created.")
                        else:
                            NewPhoneNumb = f"31-{NewPhoneNumb}"
                            salt = bcrypt.gensalt()
                            Password = bcrypt.hashpw(bytes(Password, 'utf-8'), salt)
                            NewAccount = Account(Username, Password, FirstName.capitalize(), LastName.capitalize(), Age, Gender, Weight, Address, City, Email, NewPhoneNumb, Type)
                            AccountManager.InsertIntoDatabase(NewAccount)
                            Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Creating account", f"Made account with username: {Username}",False)
                            print("Account created.")


    def InsertIntoDatabase(account):
        if not isinstance(account, Account): return False, "Given account is not of type AccountManager."
        #Decrypt(Members.EncryptedDB, Members.HardCodePassword , Members.SourceDB)
        # connection = sqlite3.connect(Members.SourceDB)
        # cursor = connection.cursor()
        # cursor.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        #                (account.Username, account.PasswordHash, account.FirstName, account.LastName, account.Age, account.Gender, account.Weight, 
        #                 account.Address, account.City, account.Email, account.PhoneNumb, account.Type, str(account.RegistrationDate), account.MemberID))
        # connection.commit()
        # connection.close()
        # Encrypt(Members.SourceDB, Members.HardCodePassword)
        EncryptNew().encrypt_member(account)
        return True, "AccountManager inserted into database."
    
    TempPasswordForReset = "TempPassword123!"

    # na inloggen als wachtwoord gelijk is aan AccountManager.TempPasswordForReset
    def ResetPasswordInput(Acc: Account):
        print("What will be your new Password?")
        NewPassword = input("> ")
        AccountManager.ChangePassword(NewPassword, Acc)

    # voor admin om password van gebruiker te veranderen naar AccountManager.TempPasswordForReset
    def ResetPassword(Acc: Account):
        AccountManager.ChangePassword(AccountManager.TempPasswordForReset, Acc)

    def ChangePassword(NewPassword: str, Acc: Account, CurrentPassword: str = None) -> tuple[bool, str]:
        # Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        EncryptNew().DecryptAll("Members")
        connection = sqlite3.connect(Members.SourceDB)
        cursor = connection.cursor()
        if CurrentPassword != None:
            cursor.execute("SELECT PasswordHash FROM Decrypted WHERE Username = ?",(Acc.Username,))
            PWHash = cursor.fetchone()[0]
            if not bcrypt.checkpw(CurrentPassword.encode("utf-8"),PWHash):
                connection.close()
                EncryptNew().DeleteDecrypted()
                return False, "Current password is incorrect"
        Result = AccountManager.Is_Valid_Password(NewPassword)
        if not Result:
            connection.close()
            EncryptNew().DeleteDecrypted()
            return Result
        cursor.execute( "UPDATE Decrypted SET PasswordHash = ? WHERE Username = ?", (bcrypt.hashpw(NewPassword.encode("utf-8"),bcrypt.gensalt()), Acc.Username))
        connection.commit()
        connection.close()
        # Encrypt(Members.SourceDB, Members.HardCodePassword)
        EncryptNew().ChangeTable("Members")
        return True

        
    def ChangePasswordInput():
        print("What is your current password?")
        CurrentPassword = input("> ")
        print("What will be your new password?")
        NewPassword = input("> ")
        Result = AccountManager.ChangePassword(NewPassword, LoggedInAccount.CurrentLoggedInAccount, CurrentPassword)
        if not Result:
            print("Changing password failed")
            print("Press Enter to continue")
            input()
        else:
            Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Changing password", "Changed password",False)


    def SearchAccount(query, currentuser):
        EncryptNew().DecryptAll("Members")
        connection = sqlite3.connect(Members.SourceDB)
        cursor = connection.cursor()
        search_pattern = f"%{query}%"
  
        base_query = """SELECT * FROM Decrypted WHERE 
                        (Username LIKE ? OR
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
                        MemberID LIKE ?)"""
        if currentuser.Type.lower() == "consultant":
            base_query += " AND Type = 'Member'"
        elif currentuser.Type.lower() == "admin":
            base_query += " AND(Type = 'Member' OR Type = 'Consultant')"
        elif currentuser.Type.lower() == "superadmin":
            base_query += " AND NOT Type = 'SuperAdmin'"
        base_query += " LIMIT 1"
        cursor.execute(base_query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern,
                                    search_pattern, search_pattern, search_pattern, search_pattern, search_pattern,
                                    search_pattern, search_pattern, search_pattern, search_pattern))
        row = cursor.fetchone()
        connection.close()
        EncryptNew().DeleteDecrypted()
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
            print("No account found")
            return None
        
    def SearchAccountForce(query):
        EncryptNew().DecryptAll("Members")
        connection = sqlite3.connect(Members.SourceDB)
        cursor = connection.cursor()
        search_pattern = f"%{query}%"
  
        base_query = """SELECT * FROM Decrypted WHERE 
                        (Username LIKE ? OR
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
                        MemberID LIKE ?)"""
        cursor.execute(base_query, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern,
                                    search_pattern, search_pattern, search_pattern, search_pattern, search_pattern,
                                    search_pattern, search_pattern, search_pattern, search_pattern))
        row = cursor.fetchone()
        connection.close()
        EncryptNew().DeleteDecrypted()
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
            print("No account found")
            return None
        
    def DeleteAccount(account):
        # Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        EncryptNew().DecryptAll("Members")
        if not isinstance(account, Account):
            raise ValueError("Expected an Account instance")
        try:
            connection = sqlite3.connect(Members.SourceDB)
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Members WHERE MemberID = ?", (account.MemberID,))
                connection.commit()
            except Exception as e:
                print(f"An error occurred while deleting the account: {e}")
                connection.rollback()
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")
        finally:
            if connection:
                connection.close()
        EncryptNew().ChangeTable("Members")


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
        
        print("Choose an option to update (1-9) or anything else to go back: ")
        option = input("> ")
        fields = ["FirstName", "LastName", "Age", "Gender", "Weight", "Address", "City", "Email", "PhoneNumb"]
        os.system('cls')
        if option in [str(i) for i in range(1, 10)]:
            field = fields[int(option) - 1]
            print(f"What would you like to change {field} to: ")
            new_value = input("> ")
            AccountManager.UpdateMemberData(account.MemberID, field, new_value)
            Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Changing account details", f"Changed {field} to {new_value} ofr {account.Username}",False)
            print(f"{field} has been updated.")
        else:
            print("Going back")


    def UpdateMemberData(MemberID, field, new_value):
        # Decrypt(Members.EncryptedDB, Members.HardCodePassword, Members.SourceDB)
        EncryptNew().DecryptAll("Members")
        with sqlite3.connect(Members.SourceDB) as conn:
            cur = conn.cursor()
            query = f"UPDATE Members SET {field} = ? WHERE MemberID = ?"
            cur.execute(query, (new_value, MemberID))
            conn.commit()
        # Encrypt(Members.SourceDB, Members.HardCodePassword)
        EncryptNew().ChangeTable("Members")

    def ChangeAccount(LoggedinAccount):
        print("Enter account detail: ")
        AccountToFind = input("> ")
        Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Searching for user", f"Looking up {AccountToFind}",False)
        member = AccountManager.SearchAccount(AccountToFind, LoggedinAccount)
        if member != None:
            loop = True
            if loop:
                if LoggedinAccount.Type.lower() == "superadmin" or LoggedinAccount.Type.lower() == "admin":
                    AccountManager.ChoiceAdmin(member, LoggedinAccount, loop)
                elif LoggedinAccount.Type.lower() == "consultant":
                    AccountManager.ChoiceConsultant(member, LoggedinAccount, loop)
            else:
                print("Press Enter to continue")
                input()
        else:
            print("Press Enter to continue")
            input()
    
    def ChoiceAdmin(member, LoggedinAccount, loop):
        while loop:
            print()
            print("Found account:")
            member.Print()
            print("1. Return")
            print("2. Edit account")
            print("3. Delete account")
            print("4. Reset password")
            print("Enter your choice: ")
            choice2 = input("> ")
            os.system('cls')
            if choice2 == "1":
                loop = False
            elif choice2 == "2":
                Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Editing account details", f"Editing user: {member.Username}",False)
                loop = False
                AccountManager.EditAccount(member)
            elif choice2 == "3":
                Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Editing account details", f"Deleting {member.Username}",False)
                AccountManager.DeleteAccount(member)
                print("Account succesfully deleted!")                
                loop = False
            elif choice2 == "4":
                Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Editing account details", f"Reseting password for: {member.Username}",False)
                AccountManager.ResetPassword(member)
                loop = False
            else:
                print("Invalid input")
                print()

    def ChoiceConsultant(member, LoggedinAccount, loop):
        while loop:
            print("Found account:")
            member.Print()
            print("1. Return")
            print("2. Edit account")
            print("Enter your choice: ")
            choice2 = input("> ")
            os.system('cls')
            if choice2 == "1":
                loop = False
                return
            elif choice2 == "2":
                Database.LogAction(LoggedinAccount.Username if LoggedinAccount != None else None,"Changing account details", f"Editing user: {member.Username}",False)
                loop = False
                AccountManager.EditAccount(member)
            else:
                print()
                print("Invalid input")
                print()

    def LogIn(Username, Password):
        result = None
        message = None

        
        if AccountManager.UnblockTime <= datetime.now():
            if isinstance(Username, str) and isinstance(Password, str): 
                EncryptNew().DecryptAll("Members")
                # if AccountManager.UsernameCheck(Username) and AccountManager.Is_Valid_Password(Password): 
                rows = Database.SelectFromDatabase("* FROM Decrypted WHERE Username = ?", False, (Username,))
                if(rows is not None and bcrypt.checkpw(Password.encode("utf-8"),rows[1])):    
                    account = Account(rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6], rows[7], rows[8], rows[9], rows[10], rows[11], rows[12], rows[13])
                    LoggedInAccount.CurrentLoggedInAccount = account
                    Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount is not None else None, "Logging in.", "Logged in.", False)
                    result = True
                    message = "Logged in."
                    AccountManager.FailedLogInCounter = 0
                    AccountManager.CurrentTimeCooldownSeconds = AccountManager.StandardTimeCooldownSeconds
                    EncryptNew().DeleteDecrypted()
                    return result, message
        else:
            timedif = AccountManager.UnblockTime - datetime.now()
            message = "Too many failed attempts. try again in "+str(timedif).split(".")[0]+" seconds."   
            result = False
            return result, message
        
        result = False
        if (message is None):
            message = "Login credentials are incorrect." 
        AccountManager.FailedLogInCounter += 1 

        if AccountManager.FailedLogInCounter >= AccountManager.MaxLogInFails:
            AccountManager.UnblockTime = datetime.now() + timedelta(seconds=AccountManager.CurrentTimeCooldownSeconds)
            timedif = AccountManager.UnblockTime - datetime.now()
            Database.LogAction(LoggedInAccount.CurrentLoggedInAccount.Username if LoggedInAccount.CurrentLoggedInAccount != None else None,"Logging in", "Too many failed attempts. "+str(timedif).split(".")[0]+" seconds cooldown.",True)
            message += " Too many failed attempts. try again in "+str(timedif).split(".")[0]+" seconds."
            AccountManager.FailedLogInCounter -= 1
            AccountManager.CurrentTimeCooldownSeconds *= 2

        EncryptNew().DeleteDecrypted()
        return result, message

    def LogInInput():
        print("What is your username?")
        username = input("> ")
        print("What is your password?")
        password = input("> ")
        LoggedIn, message = AccountManager.LogIn(username, password)
        print(message)
        print()
        if not LoggedIn:
            AccountManager.LogInInput()